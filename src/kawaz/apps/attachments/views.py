import os
import mimetypes
from django.conf import settings
from django.views.generic.detail import BaseDetailView
from django.http.response import HttpResponse, HttpResponseNotFound

from .models import Material

class MaterialDetailView(BaseDetailView):
    model = Material
    slug_field = 'slug'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            name = self.object.content_file.name
            mime_type_guess = mimetypes.guess_type(name)
            path = os.path.join(settings.MEDIA_ROOT, object.content_file.path)
            with open(path, 'r') as file:
                response = HttpResponse(file, mimetype=mime_type_guess[0])
                response['Content-Disposition'] = 'attachment; filename={}'.format(name)
        except:
            pass
        return HttpResponseNotFound()