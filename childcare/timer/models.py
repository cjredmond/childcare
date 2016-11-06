from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from datetime import datetime, timedelta, timezone

PROFILE_TYPE = [('p', 'parent'), ('f', 'faculty')]
class Profile(models.Model):
    user = models.OneToOneField('auth.User')
    profile_type = models.CharField(max_length=1, choices=PROFILE_TYPE)
    def __str__(self):
        return str(self.user.username)

@receiver(post_save, sender=User)
def create(**kwargs):
    created = kwargs['created']
    instance = kwargs['instance']
    if created:
        Profile.objects.create(user=instance, profile_type='p')



class Child(models.Model):
    parent = models.ForeignKey(Profile)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    code = models.IntegerField()

    def __str__(self):
        return self.first_name + " " + self.last_name
    @property
    def total_time(self):
        stays = self.stay_set.all()
        x = []
        for stay in stays:
            #if stay.active == True:
                #x.append(datetime.now() - stay.in_time)
            x.append(stay.str_dif())

        return round(sum(x),3)

class Stay(models.Model):
    child = models.ForeignKey(Child)
    in_time = models.DateTimeField(auto_now_add=True)
    out_time = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    notes = models.TextField(null=True, blank=True)

    @property
    def time_dif(self):
        return self.out_time - self.in_time

    def day(self):
        return self.in_time.strftime('%a, %b %d')

    # def str_in(self):
    #     return self.in_time.strftime('%')

    def str_dif(self):
        seconds = self.time_dif.total_seconds()
        hours = seconds/3600
        return round(hours, 3)
