from rest_framework import serializers
from .models import Tweet


class TweetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tweet
        fields = ('id', 'data', 'created_date', 'modified_date')
