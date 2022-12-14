from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from jsonfield import JSONField

# Create your models here.

class Trader(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    positions = JSONField(default={'name': "positions"})

    pastReturns = JSONField(default={'name': "pastReturns"})

    cash = models.IntegerField(default=1_000_000)
    AUM = models.IntegerField(default=1_000_000)

class Transaction(models.Model):
    key= models.AutoField(auto_created = True,primary_key = True,serialize = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type=models.CharField(max_length=5)
    number=models.IntegerField()
    symbol=models.CharField(max_length=50)
    date=models.DateField()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Trader.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.trader.save()
