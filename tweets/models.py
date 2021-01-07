from django.db import models


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

    @classmethod
    def create_new_tweet(cls, user, tweet):
        """Creates a new tweet for a user
        """

        tweet = cls.objects.create(user=user, data=tweet)
        return tweet

    @classmethod
    def get_tweet(cls, user, tweet_id):
        """Gets a tweet

        :raises: Tweet.DoesNotExist if no tweet exists
        """

        return cls.objects.get(id=tweet_id, user=user)

    @classmethod
    def get_all_tweets(cls, user):
        """Gets all tweets
        """

        return cls.objects.filter(user=user).all()

    @classmethod
    def update_tweet(cls, user, tweet_id, data):
        """Updates a tweet
        """

        tweet = cls.objects.get(user=user, id=tweet_id)
        tweet.data = data
        tweet.save()

    @classmethod
    def delete_tweet(cls, user, tweet_id):
        """Deletes a tweet
        """

        tweet = cls.objects.get(id=tweet_id, user=user)
        tweet.delete()

    def serialize(self):
        """[summary]

        :raises NotImplementedError: [description]
        """

        return {
            'id': self.id,
            'data': self.data,
            'created_date': self.created_date,
            'modified_date': self.modified_date
        }

    class Meta:
        ordering = ['-created_date']


class TweetModRequest(BaseModel):
    """Class that represents an Admin initiated Tweet modification (CRUD) request
    """

    CREATE = 1
    UPDATE = 2
    DELETE = 3

    MOD_CHOICES = (
        (CREATE, 'create'),
        (UPDATE, 'update'),
        (DELETE, 'delete'),
    )
    mod_type = models.PositiveSmallIntegerField(choices=MOD_CHOICES, null=False)

    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='modification_tickets')
    tweet_data = models.CharField(max_length=280)

    requester = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='modification_requests')
    approver = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='approvals')

    approved = models.BooleanField(default=False)
    approval_date = models.DateTimeField(null=True)

    def create_modification_request(self, tweet_id, tweet_data):
        """[summary]

        :param tweet_id: [description]
        :type tweet_id: [type]
        :param data: [description]
        :type data: [type]
        """

        raise NotImplementedError
