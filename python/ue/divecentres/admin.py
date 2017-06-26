from django.contrib import admin

# Register your models here.
from .models import DiveCentre, Location, DiveSite

admin.site.register(DiveCentre)
admin.site.register(Location)
admin.site.register(DiveSite)