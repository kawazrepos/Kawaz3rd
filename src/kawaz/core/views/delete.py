# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/10/9
#
from django.contrib import messages

__author__ = 'giginet'

from django.views.generic.edit import DeleteView

class DeleteNotificationView(DeleteView):
    """
    削除時に、削除通知を出すDeleteView
    SuccessMessageMixinはDeleteViewには使えないので、自前で実装している

    Ref : http://stackoverflow.com/questions/24822509/success-message-in-deleteview-not-shown
    """
    success_message = ""

    def delete(self, request, *args, **kwargs):
        success_message = self.get_success_message()
        if success_message:
            messages.success(self.request, success_message)
        return super(DeleteNotificationView, self).delete(request, *args, **kwargs)

    def get_success_message(self):
        return self.success_message