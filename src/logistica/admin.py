from django.contrib.gis import admin
from .models import Production, Region

admin.site.register(Production, admin.GeoModelAdmin)
admin.site.register(Region, admin.GeoModelAdmin)
