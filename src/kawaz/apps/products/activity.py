# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/10/15
#
from django.contrib.contenttypes.models import ContentType
from django_comments import Comment
from kawaz.apps.products.models import AbstractRelease

__author__ = 'giginet'
from activities.mediator import ActivityMediator

class ProductActivityMediator(ActivityMediator):

    def alter(self, instance, activity, **kwargs):
        # 状態がdraftの場合は通知しない
        if activity and activity.status == 'updated':
            if activity.previous:
                # 通知が必要な状態の変更を詳細に記録する
                previous = activity.previous.snapshot
                is_created = lambda x: (
                    not getattr(previous, x) and
                    getattr(instance, x)
                )
                is_updated = lambda x: (
                    getattr(previous, x) and
                    getattr(instance, x) and
                    getattr(previous, x) != getattr(instance, x)
                )
                is_deleted = lambda x: (
                    getattr(previous, x) and
                    not getattr(instance, x)
                )
                remarks = []
                attributes = (
                    'title',
                    'description',
                    'thumbnail',
                    'display_mode',
                    'trailer'
                )
                for attribute in attributes:
                    if is_created(attribute):
                        remarks.append(attribute + '_created')
                    elif is_updated(attribute):
                        remarks.append(attribute + '_updated')
                    elif is_deleted(attribute):
                        remarks.append(attribute + '_deleted')
                if not remarks:
                    # 通知が必要な変更ではないため通知しない
                    return None
                activity.remarks = "\n".join(remarks)
        return activity

    def prepare_context(self, activity, context, typename=None):
        context = super().prepare_context(activity, context, typename)

        if activity.status == 'updated':
            # remarks に保存された変更状態を利便のためフラグ化
            for flag in activity.remarks.split():
                context[flag] = True
        elif activity.status == 'add_comment':
            # コメントが付いたとき、remarksにcommentのpkが入ってるはずなので
            # 取得してcontextに渡す
            try:
                comment = Comment.objects.get(pk=int(activity.remarks))
                context['comment'] = comment
            except:
                pass
        elif activity.status == 'add_release':
            # releaseをcontextに加える
            try:
                ct_pk, pk = activity.remarks.split(',')
                ct = ContentType.objects.get_for_id(ct_pk)
                release_class = ct.model_class()
                release = release_class.objects.get(pk=pk)
                context['release'] = release
            except:
                pass
        return context


class ReleaseActivityMediator(ActivityMediator):

    def alter(self, instance, activity, **kwargs):
        if activity and activity.status == 'created':
            target = instance.product
            # リリースが作成されたとき、対象オブジェクトを書き換える
            ct = ContentType.objects.get_for_model(type(target))
            pk = target.pk
            activity.content_type = ct
            activity.object_id = pk
            activity.status = 'add_release'
            # URLRelease, PackageRelease、どちらにも対応できるように付いたリリースのctを入れている
            release_ct = ContentType.objects.get_for_model(type(instance))
            activity.remarks = '{},{}'.format(str(release_ct.pk), str(instance.pk))
        return activity