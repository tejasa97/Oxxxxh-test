from django.urls import path, include
from .views import CreateTweet, GetTweet, GetAllTweets, DeleteTweet, UpdateTweet

urlpatterns = [
    path('tweet/create', CreateTweet.as_view(), name='create_tweet'),
    path('tweet/get_all', GetAllTweets.as_view(), name='get_all_tweets'),
    path('tweet/get/<int:tweet_id>', GetTweet.as_view(), name='get_tweet'),
    path('tweet/update/<int:tweet_id>', UpdateTweet.as_view(), name='delete_tweet'),
    path('tweet/delete/<int:tweet_id>', DeleteTweet.as_view(), name='delete_tweet'),
]
