import os
from django.views.generic.detail import BaseDetailView
from django.http.response import HttpResponse, HttpResponseNotFound

from .models import Material

class MaterialDetailView(BaseDetailView):
    model = Material
    slug_field = 'slug'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            name = self.object.filename
            path = self.object.content_file.path
            mimetype = self.object.mimetype
            # withをすると、変なタイミングでcloseされてしまって正常にアクセスできない
            f = open(path, 'rb')
            response = HttpResponse(f.read(), content_type=mimetype)
            response['Content-Length'] = os.fstat(f.fileno()).st_size
            response['Content-Disposition'] = (
                'attachment; filename={}'.format(name)
            )
            return response
        except FileNotFoundError:
            # もし、レコードには存在するが、ファイルがなかったり、読み込めなかったとき
            self.object.delete() # DBと不整合なため、レコードを削除する
            return HttpResponseNotFound()
