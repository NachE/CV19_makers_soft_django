from django.contrib.gis import admin
from .models import (
    Region,
    Resource,
    Inventory,
    Producer,
    Consumer,
    Shipping,
)

admin.site.register(Region, admin.GeoModelAdmin)
admin.site.register(Resource, admin.GeoModelAdmin)
admin.site.register(Inventory, admin.GeoModelAdmin)
admin.site.register(Producer, admin.GeoModelAdmin)
admin.site.register(Consumer, admin.GeoModelAdmin)
admin.site.register(Shipping, admin.GeoModelAdmin)
