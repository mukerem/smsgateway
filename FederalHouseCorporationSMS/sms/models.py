from django.db import models
from django.utils.timezone import now


class SMS(models.Model):
    text = models.CharField(max_length=255)
    smsc = models.CharField(max_length=48)
    ts = models.CharField(max_length=48)
    destination = models.CharField(max_length=48)
    source = models.CharField(max_length=48)
    service = models.CharField(max_length=48)
    url = models.CharField(max_length=48)
    mask = models.PositiveIntegerField()
    status = models.PositiveIntegerField()
    boxc = models.CharField(max_length=48)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.destination
