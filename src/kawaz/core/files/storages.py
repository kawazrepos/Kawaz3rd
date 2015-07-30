import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings



# http://stackoverflow.com/questions/4394194/replacing-a-django-image-doesnt-delete-original
class OverwriteStorage(FileSystemStorage):
    def _save(self, name, content):
        if self.exists(name):
            self.delete(name)
        return super(OverwriteStorage, self)._save(name, content)

    def get_available_name(self, name):
        return name
