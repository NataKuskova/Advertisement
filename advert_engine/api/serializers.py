from rest_framework import serializers
from datetime import datetime, timedelta
from django.utils import timezone
import re
from advert_engine.models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'


class AdvertSerializer(serializers.ModelSerializer):
    remaining_date = serializers.SerializerMethodField()
    preview = GallerySerializer(many=True, source='first_image',
                                read_only=True)

    class Meta:
        model = Advert
        fields = '__all__'
        read_only_fields = [
            'status',
            'number_of_views',
            'remaining_date',
        ]

    def validate(self, data):
        match = re.match(r'(\w|\d|\-|\.|\_|\ )*$', data['title'])
        if not match:
            raise serializers.ValidationError(
                "Title contains invalid characters")
        if data['publish_date'] <= timezone.now():
            raise serializers.ValidationError(
                "Publication date should be a future")
        if data['end_date'] <= data['publish_date']:
            raise serializers.ValidationError(
                "End date must be after publication date")
        return data

    def get_remaining_date(self, obj):
        if obj.status == 'published':
            remaining_days = obj.end_date - timezone.now()
            if remaining_days < timedelta(days=1):
                return str(remaining_days)
            elif remaining_days > timedelta(weeks=2):
                return 'More than two weeks'
            elif remaining_days <= timedelta(weeks=2):
                return remaining_days.days
        return 'Not published'
