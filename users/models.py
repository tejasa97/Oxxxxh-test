from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    REGULAR = 1
    ADMIN = 2
    SUPER_ADMIN = 3

    ROLE_CHOICES = (
        (REGULAR, 'regular'),
        (ADMIN, 'admin'),
        (SUPER_ADMIN, 'super-admin'),
    )

    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=REGULAR)


class Admin(User):
    """[summary]

    :param User: [description]
    :type User: [type]
    """

    def edit_user_details(self, user, details):
        """[summary]

        :param user: [description]
        :type user: [type]
        :param details: [description]
        :type details: [type]
        """

        raise NotImplementedError

    def update_user_tweet(self, tweet_id):
        """[summary]

        :param tweet_id: [description]
        :type tweet_id: [type]
        """

        raise NotImplementedError

    class Meta:
        abstract = True
