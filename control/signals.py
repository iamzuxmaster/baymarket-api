import string
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Account
import random

def uuid(): 
    random_al = ''
    random_al_1 = ''
    random_num = ''
    for i in range(0, 2):
        random_al += random.choice('AB')
    for i in range(0, 1):
        random_al_1 += random.choice('ABCDEFGIJKLMNOPQRSTUVWXYZ')
    for i in range(0, 8):
        random_num += random.choice("123456789")
        
    id = f"{random_al}{random_al_1}{random_num}"
    return id

def token():
    token = ''
    for i in range(0, 32): 
        token +=  random.choice(string.hexdigits)
    return token

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance, balance_id=uuid(), mobile_token=token())

