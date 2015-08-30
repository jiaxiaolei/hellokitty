from django.db import models


# Create your models here.
class Rootport(models.Model):
    title = models.TextField(unique=True)
    link = models.TextField(unique=True)
    status = models.BooleanField(default=False)
    page_num = models.IntegerField(null=True)

    def __unicode__(self):
        return str(self.id)


class Resources(models.Model):
    title = models.TextField(unique=True)
    link = models.TextField(unique=True)
    status = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.id)
