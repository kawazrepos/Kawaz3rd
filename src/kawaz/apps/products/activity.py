from django.contrib.contenttypes.models import ContentType
from django_comments import Comment
from django.conf import settings
from kawaz.apps.products.models import AbstractRelease, Screenshot
from activities.mediator import ActivityMediator


class ProductActivityMediator(ActivityMediator):
    notifiers = settings.ACTIVITIES_DEFAULT_NOTIFIERS + ('twitter_kawaz_official')

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
        elif activity.status == 'comment_added':
            # コメントが付いたとき、remarksにcommentのpkが入ってるはずなので
            # 取得してcontextに渡す
            try:
                comment = Comment.objects.get(pk=int(activity.remarks))
                context['comment'] = comment
            except:
                pass
        elif activity.status == 'release_added':
            # releaseをcontextに加える
            try:
                app_label, model, pk = activity.remarks.split(',')
                ct = ContentType.objects.get_by_natural_key(app_label, model)
                release_class = ct.model_class()
                release = release_class.objects.get(pk=pk)
                context['release'] = release
            except:
                pass
        elif activity.status == 'screenshot_added':
            # コメントが付いたとき、remarksにscreenshotのpkが入ってるはずなので
            # 取得してcontextに渡す
            try:
                ss = Screenshot.objects.get(pk=int(activity.remarks))
                context['screenshot'] = ss
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
            activity.status = 'release_added'
            # URLRelease, PackageRelease、どちらにも対応できるように付いた
            # リリースのCTを <app_label>,<model>,<pk>の書式で入れている
            release_ct = ContentType.objects.get_for_model(type(instance))
            activity.remarks = ','.join((release_ct.app_label,
                                         release_ct.model, str(instance.pk)))
            return activity
        return None


class ScreenshotActivityMediator(ActivityMediator):

    def alter(self, instance, activity, **kwargs):
        if activity and activity.status == 'created':
            target = instance.product
            # スクリーンショットが作成されたとき、対象オブジェクトを書き換える
            ct = ContentType.objects.get_for_model(type(target))
            pk = target.pk
            activity.content_type = ct
            activity.object_id = pk
            activity.status = 'screenshot_added'
            # Screenshotのpkをremarksに入れる
            activity.remarks = str(instance.pk)
            return activity
        return None
