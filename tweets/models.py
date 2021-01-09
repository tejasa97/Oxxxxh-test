from django.db import models
from django.utils import timezone
from .managers import OnlyActiveManager
import logging

action_logger = logging.getLogger('action')
audit_logger = logging.getLogger('audit')
access_logger = logging.getLogger('access')


class BaseModel(models.Model):
    """Base model with `created_date` and `modified_date` fields
    """

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Tweet(BaseModel):
    """Class that represents a Tweet
    """

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='tweets')
    data = models.CharField(max_length=280)

    objects = OnlyActiveManager()
    naive_objects = models.Manager()

    active = models.BooleanField(default=True)

    @classmethod
    def create_new_tweet(cls, user, tweet):
        """Creates a new tweet for a user

        :raises: Exception if any DB error
        """

        tweet = cls.objects.create(user=user, data=tweet)

        action_logger.info(f"User {user} created a new tweet {tweet}")

        return tweet

    @classmethod
    def get_tweet(cls, user, tweet_id):
        """Gets a tweet

        :raises: Tweet.DoesNotExist if no tweet exists
        """

        tweet = cls.objects.get(id=tweet_id, user=user)
        access_logger.info(f"User {user} accessed tweet {tweet}")

        return tweet

    @classmethod
    def get_all_tweets(cls, user):
        """Gets all tweets

        :raises: Exception if any DB error
        """

        tweets = cls.objects.filter(user=user).all()
        access_logger.info(f"User {user} accessed all tweets")

        return tweets

    @classmethod
    def update_tweet(cls, user, tweet_id, data):
        """Updates a tweet

        :raises: Tweet.DoesNotExist if no tweet exists
        :raises: Exception if any DB error while updating
        """

        tweet = cls.objects.get(user=user, id=tweet_id)
        tweet.data = data
        tweet.save()

        action_logger.info(f"User {user} updated tweet {tweet}")

    @classmethod
    def delete_tweet(cls, user, tweet_id):
        """Deletes a tweet (make inactive)

        :raises: Tweet.DoesNotExist if no tweet exists
        :raises: Exception if any DB error while updating state
        """

        tweet = cls.objects.get(id=tweet_id, user=user)
        tweet.active = False
        tweet.save()

        action_logger.info(f"User {user} deleted tweet {tweet}")

    def update_tweet_data(self, new_data):
        """Updates a tweet

        :raises: Exception if any DB error while updating
        """

        self.data = new_data
        self.save()

    def make_inactive(self):
        """Makes tweet inactive

        :raises: Exception if any DB error while updating
        """

        self.active = False
        self.save()

    """ INSIGHTS """
    @classmethod
    def get_tweet_frequency(cls, user_id, start_date, end_date):
        """Gets the tweet frequency for a User within a `start_date` and `end_date` range
        """

        return Tweet.objects.filter(user__id=user_id, created_date__range=[start_date, end_date]).count()

    def __str__(self):

        return f"<Tweet[ID: {self.id},DATA: {self.data[:10]}>"

    class Meta:
        ordering = ['-created_date']


class TweetModRequest(BaseModel):
    """Class that represents a Tweet modification (CRUD) request initiated by an Admin
    """

    UPDATE = 1
    DELETE = 2

    MOD_CHOICES = (
        (UPDATE, 'update'),
        (DELETE, 'delete'),
    )
    mod_type = models.PositiveSmallIntegerField(choices=MOD_CHOICES, null=False)

    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE,
                              related_name='modification_tickets', null=True)

    old_tweet_data = models.CharField(max_length=280, null=True)
    tweet_data = models.CharField(max_length=280, null=True)

    requester = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='modification_requests')
    approver = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='approvals', null=True)

    approved = models.BooleanField(null=True)
    approval_date = models.DateTimeField(null=True)

    @classmethod
    def new_update_request(cls, admin_user, tweet_id, tweet_data):
        """Creates a new Update modification request

        :param admin_user: Admin `User` object
        :param tweet_id: `Tweet` ID
        :type tweet_id: int
        :param data: Tweet data
        :type data: str
        """

        tweet = Tweet.objects.get(id=tweet_id)
        old_tweet_data = tweet.data

        tweet_mod_request = cls.objects.create(
            requester=admin_user, mod_type=cls.UPDATE, tweet=tweet, old_tweet_data=old_tweet_data, tweet_data=tweet_data)

        action_logger.info(f"Admin {admin_user} created new UPDATE request {tweet_mod_request}")
        return tweet_mod_request

    @classmethod
    def new_delete_request(cls, admin_user, tweet_id):
        """Creates a new Delete modification request

        :param admin_user: Admin `User` object
        :param tweet_id: Tweet ID
        :type tweet_id: int
        """

        tweet = Tweet.objects.get(id=tweet_id)
        tweet_mod_request = cls.objects.create(
            requester=admin_user, mod_type=cls.DELETE, tweet=tweet, old_tweet_data=None, tweet_data=None)

        action_logger.info(f"Admin {admin_user} created new DELETE request {tweet_mod_request}")
        return tweet_mod_request

    @classmethod
    def mod_request_action(cls, super_admin_user, mod_request_id, action):
        """Applies a SuperAdmin's action to a TweetModificationRequest

        :param super_admin: SuperAdmin `User` object
        :param mod_request_id: `TweetModRequest` object ID
        :type mod_request_id: int
        :param action: ("approve" / "reject")
        :type action: str
        """

        action_options = {
            'approve': True,
            'reject': False
        }

        tweet_mod_request = cls.objects.get(id=mod_request_id)
        tweet_mod_request.apply_approval_action(
            action_options[action])  # do the approval (approve, reject)

        tweet_mod_request.approved = action_options[action]
        tweet_mod_request.approval_date = timezone.now()
        tweet_mod_request.approver = super_admin_user
        tweet_mod_request.save()

        audit_logger.info(
            f"SuperAdmin {super_admin_user} invoked action {action.upper()} for tweet modification request {tweet_mod_request}"
        )

    def apply_approval_action(self, approval):
        """Applies a ModRequest action ('approve'/'reject') to a TweetModificationRequest
        Generally only accessible for a SuperAdmin

        :type approval: bool
        """

        if approval == False:
            return

        if self.mod_type == TweetModRequest.UPDATE:
            self.tweet.update_tweet_data(self.tweet_data)

        elif self.mod_type == TweetModRequest.DELETE:
            self.tweet.make_inactive()

    """ INSIGHTS """
    @classmethod
    def get_admin_mod_requests_count(cls, admin_user_id, start_date, end_date):
        """Gets the total number of `modification requests` made by an Admin within a `start_date` and `end_date`
        """

        return cls.objects.filter(requester__id=admin_user_id, created_date__range=[start_date, end_date]).count()

    def __str__(self):

        return f"<TweetModRequest:{self.id}>"
