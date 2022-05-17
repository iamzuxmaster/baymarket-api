from django.db import models
from slugify import slugify
from django_resized import ResizedImageField
from django.contrib.auth.models import User
import random
import string


def random_id():
    id = ""
    for i in range(8):
        id += random.choice(string.hexdigits)
    return id

class Social(models.Model):
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255)


class Account(models.Model): 
    user = models.OneToOneField(User,  on_delete=models.CASCADE)
    phone = models.CharField(max_length=255,null=True, blank=True)
    roles = [
        ("client", "Client"),
        ("moderator", "Moderator-Admin"),
        ("admin", "Controller"),
        ("superadmin", "SuperAdmin"),
        ("dev", "Developer"),
    ]
    role = models.CharField(max_length=255, choices=roles, default="client")
    verified = models.BooleanField(default=False)
    block = models.BooleanField(default=False)
    block_end = models.DateTimeField(null=True, blank=True)
    legal = models.BooleanField(default=False)
    balance_id = models.CharField(null=True, blank=True, default=0, max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    mobile_token = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self): 
        return f"{self.user.username}"

    class Meta: 
        verbose_name = "Аккаунт"
        verbose_name_plural = "Аккаунты"

class AccountTemp(models.Model):
    phone = models.CharField(max_length=255)
    code = models.CharField(max_length=255, null=True, blank=True)
    verified = models.BooleanField(default=False)

    

class Region(models.Model):
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    code = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.title_ru}"
    
    class Meta: 
        verbose_name = "Страна"
        verbose_name_plural = "Страны"


class District(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)    
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    code = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title_ru} ({self.region.title_ru})"


    class Meta: 
        verbose_name = "Город"
        verbose_name_plural = "Городы"


class Company(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    logo = ResizedImageField(size=[600, 600], quality=100, upload_to="companies/")
    title = models.CharField(max_length=255)
    description = models.TextField()
    verified = models.BooleanField(default=False)
    address = models.TextField()
    phone = models.IntegerField(null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_vierfied = models.DateTimeField(null=True, blank=True)
    slug = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.account.user.first_name})"

    class Meta: 
        verbose_name = "Компание"
        verbose_name_plural = "Компании"


class CompanyPhone(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    phone = models.IntegerField()


class CompanyEmail(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    email = models.CharField(max_length=255)


class CompanySocial(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    social = models.ForeignKey(Social, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=255)


class Transaction(models.Model): 
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=255)
    types = [
        ("in", "Prixod"),
        ("out", "Rasxod"),
    ]
    type = models.CharField(max_length=255, choices=types)
    sum = models.IntegerField()
    pay_options = [
        ("click", "Click"),
        ("payme", "PayMe")
    ]
    pay_option = models.CharField(max_length=255, choices=pay_options)
    pay_option_key = models.CharField(max_length=500, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)

class Room(models.Model): 
    uuid = models.CharField(max_length=255, null=True, blank=True)
    account_a = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name='control_room_accounta')
    account_b = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name='control_room_accountb')

    def __str__(self) -> str:
        return f"{self.account_a.user.username}"

    def messages(self):
        return Message.objects.filter(room=self)

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    read = models.BooleanField(default=False)
    