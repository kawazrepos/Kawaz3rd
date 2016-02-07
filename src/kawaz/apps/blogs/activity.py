from activities.mediator import ActivityMediator
from django_comments.models import Comment


class EntryActivityMediator(ActivityMediator):
    def alter(self, instance, activity, **kwargs):
        # 状態がdraftの場合は通知しない
        if activity and instance.pub_state == 'draft':
            return None
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
                if (getattr(previous, 'pub_state') == 'draft' and
                    getattr(instance, 'pub_state') != 'draft'):
                    # 前回下書きで今回は下書きじゃない
                    remarks.append('published')
                attributes = (
                    'title',
                    'body',
                    'category',
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
            else:
                # 前回存在してなくて、いきなりupdateのとき
                activity.remarks = 'published'
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
        return context
