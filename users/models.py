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

    @property
    def is_admin(self):

        return self.role == User.ADMIN

    @property
    def is_super_admin(self):

        return self.role == User.SUPER_ADMIN

    def __str__(self):

        return f"<User: {self.first_name}>"
