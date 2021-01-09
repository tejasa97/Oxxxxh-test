from django.db import models


class OnlyActiveManager(models.Manager):
    def get_queryset(self):
        return super(OnlyActiveManager, self).get_queryset().filter(active=True)
