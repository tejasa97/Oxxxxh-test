from rest_framework import serializers
from .models import Tweet, TweetModRequest


class TweetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tweet
        fields = ('id', 'data', 'created_date')


class TweetModRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = TweetModRequest
        fields = ('id', 'created_date', 'requester_id')
