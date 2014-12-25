# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.contenttypes.models import ContentType
from .models import HistoryWallTestModelA as ModelA
from .models import HistoryWallTestModelB as ModelB
from .models import HistoryWallTestModelC as ModelC
from ..models import Wall, History


class HistoryWallModelsWallModel(TestCase):
    def setUp(self):
        self.models = (
            ModelA.objects.create(text='a'),
            ModelA.objects.create(text='a'),
            ModelA.objects.create(text='a'),
            ModelB.objects.create(text='b'),
            ModelB.objects.create(text='b'),
            ModelC.objects.create(text='c'),
        )

    def test_content_object_uniqueness(self):
        """Wall instance is unique to content_object"""
        Wall.objects.create(content_object=self.models[0])
        self.assertRaises(IntegrityError,
                          Wall.objects.create,
                          content_object=self.models[0])

    def test_index_ordering(self):
        wall1 = Wall.objects.create(content_object=self.models[0])
        wall2 = Wall.objects.create(content_object=self.models[1])
        wall3 = Wall.objects.create(content_object=self.models[2])

        # newest first
        self.assertQuerysetEqual(Wall.objects.all(),
                                 map(repr, (wall3, wall2, wall1)))
        # change the order
        wall1.save()
        self.assertQuerysetEqual(Wall.objects.all(),
                                 map(repr, (wall1, wall3, wall2)))

    def test_index_auto_maximize(self):
        wall1 = Wall.objects.create(content_object=self.models[0])
        wall2 = Wall.objects.create(content_object=self.models[1])

        # creating new instances will increase index
        self.assertEqual(wall1._index+1, wall2._index)

        # adding a new history will regulate the index to maximum
        History.objects.create(wall=wall1, status='created')
        wall1 = Wall.objects.get(pk=wall1.pk)
        self.assertEqual(
            wall1._index, Wall._get_max_index(), (
                'Adding a new history instance to the wall should '
                'increase _index value'
            ))

        # adding a new history to different wall won't regulate index
        previous_index = wall1._index
        History.objects.create(wall=wall2, status='created')
        wall1 = Wall.objects.get(pk=wall1.pk)
        self.assertNotEqual(
            wall1._index, Wall._get_max_index(), (
                'Adding a new history instance to a different wall '
                'should not increase _index value'
            ))
        self.assertEqual(
            wall1._index, previous_index, (
                'Adding a new history instance to a different wall '
                'should not increase _index value'
            ))


class HistoryWallModelsHistoryModel(TestCase):
    def setUp(self):
        self.models = (
            ModelA.objects.create(text='a'),
            ModelA.objects.create(text='a'),
            ModelA.objects.create(text='a'),
            ModelB.objects.create(text='b'),
            ModelB.objects.create(text='b'),
            ModelC.objects.create(text='c'),
        )
        self.walls = (
            Wall.objects.create(content_object=self.models[0]),
            Wall.objects.create(content_object=self.models[1]),
            Wall.objects.create(content_object=self.models[2]),
        )

    def test_save_update_wall_index(self):
        """wall._index should be automatically updated by history creation"""

        # creating an history instance should automatically update wall._index
        previous_index = self.walls[0]._index
        history = History.objects.create(wall=self.walls[0],
                                         status='created')
        wall = Wall.objects.get(pk=self.walls[0].pk)
        self.assertNotEqual(wall._index, previous_index)
        self.assertEqual(wall._index, Wall._get_max_index())

        # updating an history instance shouldn't update wall._index
        previous_index = self.walls[0]._index
        history.status = 'updated'
        history.save()
        wall = Wall.objects.get(pk=self.walls[0].pk)
        self.assertEqual(wall._index, previous_index)
