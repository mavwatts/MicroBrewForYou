from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from microbrewforyou_app.models import CustomUser, Posts, Breweries, BrewTypes

# Register your models here.
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Posts)
admin.site.register(Breweries)
admin.site.register(BrewTypes)
