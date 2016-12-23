from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
import logging
from rest_framework.filters import (SearchFilter,
                                    OrderingFilter,
                                    DjangoFilterBackend,)
from datetime import datetime
from itertools import chain
from django.db.models import Q
from django.db.models import Case, When
from advert_engine.api.serializers import *
from advert_engine.models import *


logger = logging.getLogger('custom')
logger.setLevel(logging.DEBUG)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer


class AdvertListViewSet(viewsets.ModelViewSet):
    queryset = Advert.objects.all().order_by('-creation_date')
    serializer_class = AdvertSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    ordering_fields = ('price', 'title')
    filter_fields = ('price', 'category')

    # def create(self, request, *args, **kwargs):
    #     pass

    def get_queryset(self):
        not_empty_preview = Advert.objects.exclude(galleries=None).order_by(
            '-creation_date').values_list('id', flat=True)
        empty_preview = Advert.objects.filter(galleries=None).order_by(
            '-creation_date').values_list('id', flat=True)
        pk_list = list(chain(not_empty_preview, empty_preview))
        preserved = Case(
            *[When(pk=pk, then=pos) for pos, pk in enumerate(pk_list)])
        queryset = Advert.objects.filter(pk__in=pk_list).order_by(preserved)
        return queryset

    def list(self, request, *args, **kwargs):
        for item in self.queryset:
            if item.publish_date.date() == datetime.now().date() and \
                            item.status == 'created':
                Advert.objects.filter(id=item.id).update(status='published')
        return super(AdvertListViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, pk=None, *args, **kwargs):
        advert = get_object_or_404(Advert, pk=pk)
        Advert.objects.filter(pk=pk).update(
            number_of_views=advert.number_of_views + 1)
        logger.info('Advertisement with id "%s" has been viewed.' % advert.id)
        serializer = AdvertSerializer(advert)
        return Response(serializer.data)


class GalleryViewSet(viewsets.ModelViewSet):
    queryset = Gallery.objects.all().order_by('-date')
    serializer_class = GallerySerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    ordering_fields = ('name', 'date')
    filter_fields = ('name', 'date')
