from django.contrib import admin

from .models import CustomUser

from oauth2_provider.models import Application
from django.contrib.admin import site

admin.site.unregister(Application)

#  Регистрируем с кастомным ModelAdmin
@admin.register(Application)
class CustomApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'client_type', 'authorization_grant_type', 'client_id', 'client_secret')

admin.site.register(CustomUser)
