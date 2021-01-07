from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rest_framework import exceptions as drf_exceptions

from users.permissions import IsAdminUser
from .models import Tweet
from .serializers import TweetSerializer


class CreateTweet(APIView):
    """Creates a new Tweet
    """

    permission_classes = (IsAuthenticated,)

    class InputSerializer(serializers.Serializer):

        data = serializers.CharField()

    def post(self, request, *args,  **kwargs):

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tweet_data = serializer.validated_data['data']
        try:
            tweet = Tweet.create_new_tweet(request.user, tweet_data)
        except Exception as e:
            print(e)
            raise drf_exceptions.APIException('Internal server error', 'error')

        return Response(status=201)


class GetTweet(APIView):
    """Gets a Tweet by it's ID
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, tweet_id, ** kwargs):

        try:
            tweet = Tweet.get_tweet(tweet_id=tweet_id, user=request.user)

        except Tweet.DoesNotExist:
            raise drf_exceptions.NotFound('Invalid tweet id', 'not_found')

        except Exception as e:
            print(e)
            raise drf_exceptions.APIException('Internal server error', 'error')

        return Response(tweet.serialize(), status=200)


class GetAllTweets(APIView):
    """Gets all tweets for a User
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, ** kwargs):

        try:
            tweets = Tweet.get_all_tweets(user=request.user)

        except Exception as e:
            print(e)
            raise drf_exceptions.APIException('Internal server error', 'error')

        serialized_tweets = TweetSerializer(tweets, many=True)
        return Response(serialized_tweets.data, status=200)


class UpdateTweet(APIView):
    """Updates a Tweet by it's ID
    """

    permission_classes = (IsAuthenticated,)

    class InputSerializer(serializers.Serializer):

        data = serializers.CharField()

    def post(self, request, *args, tweet_id, **kwargs):

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tweet_data = serializer.validated_data['data']

        try:
            tweet = Tweet.update_tweet(request.user, tweet_id, tweet_data)

        except Tweet.DoesNotExist:
            raise drf_exceptions.NotFound('Invalid tweet id', 'not_found')
        except Exception as e:
            print(e)
            raise drf_exceptions.APIException('Internal server error', 'error')

        return Response(status=201)


class DeleteTweet(APIView):
    """Deletes a tweet by the Tweet's ID
    """

    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, tweet_id, **kwargs):

        try:
            Tweet.delete_tweet(user=request.user, tweet_id=tweet_id)

        except Tweet.DoesNotExist:
            raise drf_exceptions.NotFound('Invalid tweet id', 'not_found')
        except Exception as e:
            print(e)
            raise drf_exceptions.APIException('Internal server error', 'error')

        return Response(status=200)
