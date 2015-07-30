# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/9/23
#


import os
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.conf import settings

def get_thumbnail_html(material):
    """
     渡したmaterialのファイルタイプに応じてサムネイル用のHTMLを返します

     Param
        Material material
    """
    def render_template(filename):
        path = os.path.join("attachments", "embed", "{}.html".format(filename))
        template = render_to_string(path, {'material': material})
        return mark_safe(template)

    if material.is_image:
        return render_template("image")
    elif material.is_audio:
        return render_template("audio")
    elif material.is_movie:
        return render_template("movie")
    elif material.is_pdf:
        return render_template("pdf")
    else:
        return render_template("etc")
