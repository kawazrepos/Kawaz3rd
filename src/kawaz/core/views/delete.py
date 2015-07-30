# ! -*- coding: utf-8 -*-
#
#
#
from django.contrib import messages



from django.views.generic.edit import DeleteView

class DeleteSuccessMessageMixin(object):
    """
    削除時に、削除通知を出すMixin
    SuccessMessageMixinはDeleteViewには使えないので、自前で実装している

    Ref : http://stackoverflow.com/questions/24822509/success-message-in-deleteview-not-shown

    Usage:
        class EntryDeleteView(DeleteSuccessMessageMixin, DeleteView):
            success_message = 'Entry successfully deleted.'

    """
    success_message = ""

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        if not response.status_code == 302:
            return response
        success_message = self.get_success_message()
        if success_message:
            messages.success(self.request, success_message)
        return response

    def get_success_message(self):
        return self.success_message
