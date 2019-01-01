from django.db import models


class TimeStampMixin(models.Model):
    created = models.DateTimeField(
        auto_now_add=True,
    )
    edited = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        abstract = True
