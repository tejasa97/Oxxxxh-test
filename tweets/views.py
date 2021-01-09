from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rest_framework import exceptions as drf_exceptions

from users.permissions import IsAdminUser, IsSuperAdminUser
from .models import Tweet, TweetModRequest
from .serializers import TweetSerializer, TweetModRequestSerializer

import logging
logger = logging.getLogger("django")


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
            logger.error(str(e))
            raise drf_exceptions.APIException('Internal server error', 'error')

        serialized_data = TweetSerializer(tweet).data
        return Response(serialized_data, status=201)


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
            logger.error(str(e))
            raise drf_exceptions.APIException('Internal server error', 'error')

        serialized_data = TweetSerializer(tweet).data
        return Response(serialized_data, status=200)


class GetAllTweets(APIView):
    """Gets all tweets for a User
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, ** kwargs):

        try:
            tweets = Tweet.get_all_tweets(user=request.user)

        except Exception as e:
            logger.error(str(e))
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
            logger.error(str(e))
            raise drf_exceptions.APIException('Internal server error', 'error')

        return Response(status=200)


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
            logger.error(str(e))
            raise drf_exceptions.APIException('Internal server error', 'error')

        return Response(status=200)


class NewTweetUpdateRequest(UpdateTweet):
    """Adds a Tweet `Update` request
    """

    permission_classes = (IsAuthenticated, IsAdminUser)

    def post(self, request, *args, tweet_id, **kwargs):

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tweet_data = serializer.validated_data['data']

        try:
            tweet_mod_request = TweetModRequest.new_update_request(
                admin_user=request.user, tweet_id=tweet_id, tweet_data=tweet_data)

        except Tweet.DoesNotExist:
            raise drf_exceptions.NotFound('Invalid tweet id', 'not_found')
        except Exception as e:
            logger.error(str(e))
            raise drf_exceptions.APIException('Internal server error', 'error')

        serialized_data = TweetModRequestSerializer(tweet_mod_request).data
        return Response(serialized_data, status=201)


class NewTweetDeleteRequest(UpdateTweet):
    """Adds a Tweet `Delete` request
    """

    permission_classes = (IsAuthenticated, IsAdminUser)

    def delete(self, request, *args, tweet_id, **kwargs):

        try:
            tweet_mod_request = TweetModRequest.new_delete_request(
                admin_user=request.user, tweet_id=tweet_id)

        except Tweet.DoesNotExist:
            raise drf_exceptions.NotFound('Invalid tweet id', 'not_found')
        except Exception as e:
            logger.error(str(e))
            raise drf_exceptions.APIException('Internal server error', 'error')

        serialized_data = TweetModRequestSerializer(tweet_mod_request).data
        return Response(serialized_data, status=201)


class TweetModRequestAction(UpdateTweet):
    """View to allow a Super Admin approve/reject a Tweet modification request
    """

    permission_classes = (IsAuthenticated, IsSuperAdminUser)

    class InputSerializer(serializers.Serializer):

        action = serializers.CharField()

        def validate_action(self, action):

            if action not in ['approve', 'reject']:
                raise serializers.ValidationError('Invalid action provided')

            return action

    def post(self, request, *args, tweet_mod_request_id, **kwargs):

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        action = serializer.validated_data['action']

        try:
            tweet_mod_request = TweetModRequest.mod_request_action(
                super_admin_user=request.user, mod_request_id=tweet_mod_request_id, action=action)

        except TweetModRequest.DoesNotExist:
            raise drf_exceptions.NotFound('Invalid tweet modification request id', 'not_found')
        except Exception as e:
            logger.error(str(e))
            raise drf_exceptions.APIException('Internal server error', 'error')

        serialized_data = TweetModRequestSerializer(tweet_mod_request).data
        return Response(serialized_data, status=201)


""" SUPERADMIN INSIGHTS """


class TweetFrequencyInsights(APIView):
    """View to allow a Super Admin get the Tweet frequency for a user within a certain date range
    """

    permission_classes = (IsAuthenticated, IsSuperAdminUser)

    class InputSerializer(serializers.Serializer):

        start_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M")
        end_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M")

    def post(self, request, *args, user_id, **kwargs):

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            tweet_frequency = Tweet.get_tweet_frequency(
                user_id=user_id, **serializer.validated_data)

        except Exception as e:
            logger.error(str(e))
            raise drf_exceptions.APIException('Internal server error', 'error')

        response = {
            'user_id': user_id,
            'tweet_frequency': tweet_frequency
        }
        return Response(response, status=200)


class AdminRequestInsights(APIView):
    """View to allow a Super Admin to get the number of changes requested by an Admin
    """

    permission_classes = (IsAuthenticated, IsSuperAdminUser)

    class InputSerializer(serializers.Serializer):

        start_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M")
        end_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M")

    def post(self, request, *args, admin_user_id, **kwargs):

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            mod_requests_count = TweetModRequest.get_admin_mod_requests_count(
                admin_user_id=admin_user_id, **serializer.validated_data)

        except Exception as e:
            logger.error(str(e))
            raise drf_exceptions.APIException('Internal server error', 'error')

        response = {
            'admin_user_id': admin_user_id,
            'mod_requests_count': mod_requests_count
        }
        return Response(response, status=200)
