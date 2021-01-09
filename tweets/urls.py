from django.urls import path, include
from .views import CreateTweet, GetTweet, GetAllTweets, DeleteTweet, UpdateTweet, \
    NewTweetUpdateRequest, NewTweetDeleteRequest, \
    TweetModRequestAction, \
    TweetFrequencyInsights, AdminRequestInsights

urlpatterns = [
    # regular users
    path('tweet/create', CreateTweet.as_view(), name='create_tweet'),
    path('tweet/get_all', GetAllTweets.as_view(), name='get_all_tweets'),
    path('tweet/get/<int:tweet_id>', GetTweet.as_view(), name='get_tweet'),
    path('tweet/update/<int:tweet_id>', UpdateTweet.as_view(), name='update_tweet'),
    path('tweet/delete/<int:tweet_id>', DeleteTweet.as_view(), name='delete_tweet'),

    # admins
    path('tweet/admin/update/<int:tweet_id>',
         NewTweetUpdateRequest.as_view(), name='new_tweet_update_request'),
    path('tweet/admin/delete/<int:tweet_id>',
         NewTweetDeleteRequest.as_view(), name='new_tweet_delete_request'),

    # superadmins mod request action
    path('tweet/superadmin/action/<int:tweet_mod_request_id>',
         TweetModRequestAction.as_view(), name='tweet_modification_action'),

    # superadmins insights
    path('tweet/insights/user_freq/<int:user_id>',
         TweetFrequencyInsights.as_view(), name='user_freq_insights'),
    path('tweet/insights/admin_count/<int:admin_user_id>',
         AdminRequestInsights.as_view(), name='admin_user_count_insights'),
]
