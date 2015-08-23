from django.db import models

# Create your models here.
class Rootport(models.Model):
    title = models.TextField()
    link = models.TextField()
    status = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.id)