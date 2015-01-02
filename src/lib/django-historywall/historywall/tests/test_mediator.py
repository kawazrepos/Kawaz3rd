# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from unittest.mock import MagicMock, patch, call
from django.test import TestCase
from django.db.models import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from .models import HistoryWallTestModelA as ModelA
from .models import HistoryWallTestModelB as ModelB
from .models import HistoryWallTestModelC as ModelC
from ..mediator import ignore_batch_processed, Mediator
from ..utils import get_field


class HistoryWallMediatorIgnoreBatchProcessedTestCase(TestCase):
    def test_without_row(self):
        """decorator should call inner function when 'row' is not specified"""
        fn = MagicMock()
        decorated = ignore_batch_processed(fn)
        decorated()
        fn.assert_called_with()

    def test_with_row_false(self):
        """decorator should call inner function when 'row' is 'False'"""
        fn = MagicMock()
        decorated = ignore_batch_processed(fn)
        decorated(row=False)
        fn.assert_called_with(row=False)

    def test_with_row_true(self):
        """decorator should NOT call inner function when 'row' is 'True'"""
        fn = MagicMock()
        decorated = ignore_batch_processed(fn)
        decorated(row=True)
        self.assertFalse(fn.called)


class HistoryWallMediatorTestCase(TestCase):
    def test_get_m2m_fields_with_m2m_fields_none(self):
        """get_m2m_fields should return all m2m fields when m2m_fields=None"""
        # ModelA have m2m fields from ModelC (without 'related_name')
        mediator = Mediator()
        mediator.model = ModelA
        self.assertEquals(mediator.get_m2m_fields(), (
            # no 'related_name' was given thus a default name was used
            # for reverse relation automatically
            get_field(ModelA, 'historywalltestmodelc_set'),
        ))

        # ModelB have m2m field from ModelC (with 'related_name')
        mediator = Mediator()
        mediator.model = ModelB
        self.assertEquals(mediator.get_m2m_fields(), (
            get_field(ModelB, 'modelcs'),
        ))

        # ModelC has m2m fields to ModelA, ModelB
        mediator = Mediator()
        mediator.model = ModelC
        self.assertEquals(mediator.get_m2m_fields(), (
            get_field(ModelC, 'modelas'),
            get_field(ModelC, 'modelbs'),
        ))

    def test_get_m2m_fields_with_m2m_fields(self):
        """get_m2m_fields should return specified m2m fields"""
        mediator = Mediator()
        mediator.model = ModelC
        mediator.m2m_fields = ('modelas',)
        self.assertEquals(mediator.get_m2m_fields(), (
            get_field(ModelC, 'modelas'),
        ))

    @patch('historywall.mediator.pre_save')
    @patch('historywall.mediator.post_save')
    @patch('historywall.mediator.pre_delete')
    @patch('historywall.mediator.m2m_changed')
    @patch('historywall.mediator.Investigator')
    def test_connect_store_model_informations(self, *args):
        """connect should store model informations"""
        model = MagicMock()

        mediator = Mediator()
        mediator.connect(model)

        self.assertEqual(mediator.model, model)
        self.assertEqual(mediator.app_label, model._meta.app_label)

    @patch('historywall.mediator.pre_save')
    @patch('historywall.mediator.post_save')
    @patch('historywall.mediator.pre_delete')
    @patch('historywall.mediator.m2m_changed')
    @patch('historywall.mediator.Investigator')
    def test_connect_create_investigator(self, Investigator, *args):
        """connect should create a new investigator instance"""
        model = MagicMock()
        investigator = MagicMock()
        Investigator.return_value = investigator

        mediator = Mediator()
        mediator.get_include_fields = MagicMock()
        mediator.get_exclude_fields = MagicMock()
        mediator.connect(model)

        Investigator.assert_called_with(model,
                                        mediator.get_include_fields(),
                                        mediator.get_exclude_fields())
        self.assertEquals(mediator.investigator, investigator)

    @patch('historywall.mediator.pre_save')
    @patch('historywall.mediator.post_save')
    @patch('historywall.mediator.pre_delete')
    @patch('historywall.mediator.m2m_changed')
    @patch('historywall.mediator.Investigator')
    def test_connect_register_receivers(self, Investigator,
                                        m2m_changed,
                                        pre_delete,
                                        post_save,
                                        pre_save):
        """connect should register receivers"""
        model = MagicMock()
        field = MagicMock()

        mediator = Mediator()
        mediator.get_m2m_fields = MagicMock(return_value=(field,))
        mediator.connect(model)

        pre_save.connect.assert_called_with(
            mediator._pre_save_receiver,
            sender=model, weak=False)
        post_save.connect.assert_called_with(
            mediator._post_save_receiver,
            sender=model, weak=False)
        pre_delete.connect.assert_called_with(
            mediator._pre_delete_receiver,
            sender=model, weak=False)
        m2m_changed.connect.assert_called_with(
            mediator._m2m_changed_receiver,
            sender=field.rel.through, weak=False)

    def test__pre_save_receiver(self):
        """_pre_save_receiver should call investigator.prepare"""
        mediator = Mediator()
        mediator.investigator = MagicMock()

        sender = MagicMock()
        instance = MagicMock()
        mediator._pre_save_receiver(sender, instance)

        mediator.investigator.prepare.assert_called_with(instance)

    @patch('historywall.mediator.Wall')
    @patch('historywall.mediator.History')
    def test__post_save_receiver_created(self, History, Wall):
        """_post_save_receiver should create wall but history on created"""
        mediator = Mediator()
        mediator.investigator = MagicMock()

        Wall.return_value = MagicMock()
        History.return_value = MagicMock()

        sender = MagicMock()
        instance = MagicMock()
        mediator._post_save_receiver(sender, instance, created=True)

        # Wall should be created
        Wall.assert_called_with(content_object=instance)
        Wall.return_value.save.assert_called_with()

        # But History
        self.assertFalse(History.called)

    @patch('historywall.mediator.Wall')
    @patch('historywall.mediator.History')
    def test__post_save_receiver_modified(self, History, Wall):
        """_post_save_receiver should create history but wall on modified"""
        mediator = Mediator()
        mediator.investigator = MagicMock()
        mediator.investigator.investigate.return_value = (
            ('foo', None, 'new'),
            ('bar', 'old', None),
            ('hoge', 'old', 'new'),
        )

        wall = MagicMock()
        Wall.objects.get_or_create.return_value = (wall, False)
        History.return_value = MagicMock()

        sender = MagicMock()
        instance = MagicMock()
        mediator._post_save_receiver(sender, instance, created=False)

        # Wall should be created
        self.assertFalse(Wall.called)

        # And History
        calls = (
            call(wall=wall,
                 status='created',
                 extra={
                     'field': 'foo',
                     'old': None,
                     'new': 'new',
                 }),
            call(wall=wall,
                 status='deleted',
                 extra={
                     'field': 'bar',
                     'old': 'old',
                     'new': None,
                 }),
            call(wall=wall,
                 status='updated',
                 extra={
                     'field': 'hoge',
                     'old': 'old',
                     'new': 'new',
                 }),
        )
        History.assert_has_calls(calls)
        self.assertEqual(History.call_count, 3)
        self.assertEqual(History.return_value.save.call_count, 3)

    @patch('historywall.mediator.Wall')
    @patch('historywall.mediator.History')
    def test__post_save_receiver_call_alter_wall(self, History, Wall):
        """_post_save_receiver should call user defined alter_wall"""
        mediator = Mediator()
        mediator.investigator = MagicMock()
        mediator.alter_wall = MagicMock()
        mediator.alter_histories = MagicMock()

        wall = MagicMock()
        Wall.return_value = wall
        History.return_value = MagicMock()

        sender = MagicMock()
        instance = MagicMock()
        mediator._post_save_receiver(sender, instance, created=True)

        mediator.alter_wall.assert_called_with(wall, instance,
                                               'post_save')
        self.assertFalse(mediator.alter_histories.called)

    @patch('historywall.mediator.Wall')
    @patch('historywall.mediator.History')
    def test__post_save_receiver_call_alter_histories(self, History, Wall):
        """_post_save_receiver should call user defined alter_histories"""
        mediator = Mediator()
        mediator.investigator = MagicMock()
        mediator.investigator.investigate.return_value = (
            ('foo', None, 'new'),
            ('bar', 'old', None),
            ('hoge', 'old', 'new'),
        )
        mediator.alter_wall = MagicMock()
        mediator.alter_histories = MagicMock()

        wall = MagicMock()
        Wall.objects.get_or_create.return_value = (wall, False)
        History.return_value = MagicMock()

        sender = MagicMock()
        instance = MagicMock()
        mediator._post_save_receiver(sender, instance, created=False)

        self.assertFalse(mediator.alter_wall.called)
        mediator.alter_histories.assert_called_with(
            [History.return_value]*3,
            wall,
            instance,
            'post_save',
        )

    @patch('historywall.mediator.Wall')
    def test__pre_delete_receiver_set_is_deleted_true(self, Wall):
        wall = MagicMock()
        wall.is_deleted = False
        Wall.objects.get.return_value = wall

        mediator = Mediator()
        mediator.alter_wall = MagicMock(return_value=wall)

        sender = MagicMock()
        instance = MagicMock()
        mediator._pre_delete_receiver(sender, instance)

        Wall.objects.get.assert_called_with(content_object=instance)
        mediator.alter_wall.assert_called_with(wall, instance, 'pre_delete')
        self.assertTrue(wall.is_deleted)
        wall.save.assert_called_with()

    @patch('historywall.mediator.Wall')
    def test__pre_delete_receiver_ignore_exception(self, Wall):
        Wall.objects.get.side_effect = ObjectDoesNotExist
        mediator = Mediator()

        sender = MagicMock()
        instance = MagicMock()
        mediator._pre_delete_receiver(sender, instance)

    #
    # TODO:
    #   Add tests for '_m2m_changed_receiver'
    #
