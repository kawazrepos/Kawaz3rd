# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/7/19
#

__author__ = 'giginet'
from rest_framework import status
from rest_framework.response import Response
from kawaz.api import mixins
from kawaz.api.views import KawazGenericViewSet
from .serializers import CategorySerializer
from ..models import Category


class CategoryViewSet(mixins.CreateModelMixin,
                      KawazGenericViewSet):
    """
    ブログカテゴリを作成するためのAPIエンドポイント
    """
    model = Category
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    author_field_name = 'author'

    def create(self, request, *args, **kwargs):
        # FIX ME!!!
        label = request.data['label']
        author = request.user
        try:
            category = Category.objects.create(label=label, author=author)
            serializer = self.get_serializer(instance=category)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except:
            serializer = self.get_serializer(data=request.data)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, headers=headers)
