from django.contrib.gis import admin
from .models import (
    Region,
    Resource,
    Inventory,
    Producer,
    Consumer,
    Shipping,
    Tracking,
    Intermediary,
)

admin.site.register(Region, admin.GeoModelAdmin)
admin.site.register(Resource, admin.GeoModelAdmin)
admin.site.register(Inventory, admin.GeoModelAdmin)
admin.site.register(Consumer, admin.GeoModelAdmin)
admin.site.register(Intermediary, admin.GeoModelAdmin)


class TrackingInline(admin.StackedInline):
    model = Tracking
    fieldsets = (
        (None, {
            'fields': ('status', 'scheduled_date')
        }),
        ('Actor en este evento (setea sólo uno)', {
            'fields': ('consumer', 'producer', 'intermediary')
        }),
    )

    extra = 0


@admin.register(Shipping)
class ShippingAdmin(admin.GeoModelAdmin):
    search_fields = (
        'id',
        'consumer__name',
        'producer__name',
    )
    list_display = (
        'consumer',
        'pk',
        'producer',
        'resource',
        'quantity',
        'get_tracking',
    )
    inlines = (TrackingInline, )

    def get_tracking(self, obj):
        tracking_str = ""
        for tracking in obj.tracking.all():
            tracking_str = tracking_str + " | " + str(tracking)
        return tracking_str

    get_tracking.short_description = 'Tracking'


class InventoryInline(admin.StackedInline):
    model = Inventory
    fields = (
        'resource',
        'producer',
        'quantity',
    )
    extra = 0


@admin.register(Producer)
class ProducerAdmin(admin.GeoModelAdmin):
    search_fields = (
        'id',
        'name',
        'inventories__resource__name',
    )
    list_display = (
        'name',
        'pk',
        'point',
        'production_capacity',
        'logistics_need',
    )
    inlines = (InventoryInline, )
