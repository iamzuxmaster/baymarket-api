from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Account)
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(AccountTemp)