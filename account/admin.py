from django.contrib import admin

# Register your models here.
from account.models import User, Purchase

admin.site.register(User)
admin.site.register(Purchase)
