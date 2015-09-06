from django.db import models
# from django.db.models import Q

# Create your models here.


class Rootport(models.Model):
    title = models.TextField()
    link = models.TextField()
    status = models.BooleanField(default=False)
    page_num = models.IntegerField(null=True)

    def __unicode__(self):
        return str(self.id)

    # def save(self, *args, **kwargs):
    #     if not Rootport.objects.filter(Q(link=self.link) | Q(title=self.title)):
    #         super(self.__class__, self).save(*args, **kwargs)


class Resources(models.Model):
    title = models.TextField()
    link = models.TextField()
    status = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.id)

    # def save(self, *args, **kwargs):
    #     if not Rootport.objects.filter(Q(link=self.link) | Q(title=self.title)):
    #         super(self.__class__, self).save(*args, **kwargs)
