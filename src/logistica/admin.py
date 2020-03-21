from django.contrib.gis import admin
from django.utils.safestring import mark_safe
from django.contrib.admin.filters import SimpleListFilter
from .models import (
    Region,
    Resource,
    Inventory,
    Producer,
    Consumer,
    Shipping,
    Tracking,
    Intermediary,
    Request,
    Carrier,
)

admin.site.register(Region, admin.GeoModelAdmin)
admin.site.register(Resource, admin.GeoModelAdmin)
admin.site.register(Inventory, admin.GeoModelAdmin)


class TrackingInline(admin.TabularInline):
    model = Tracking
    fieldsets = (
        (None, {
            'fields': ('status', 'scheduled_date', 'record_date')
        }),
        ('Actor en este evento (setea sólo uno)', {
            'fields': ('consumer', 'producer', 'intermediary')
        }),
    )

    extra = 0


class ShippingStatusFilter(SimpleListFilter):
    title = 'status'
    parameter_name = 'status'
    default_value = None

    def lookups(self, request, model_admin):
        return Shipping.STATUS_CHOICES

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status=self.value())
        return queryset


class ShippingResourceFilter(SimpleListFilter):
    title = 'resource'
    parameter_name = 'resource'
    default_value = None

    def lookups(self, request, model_admin):
        list_of_resources = []
        queryset = Resource.objects.all()
        for resource in queryset:
            list_of_resources.append((str(resource.id), resource.name))
        return sorted(list_of_resources, key=lambda tp: tp[1])

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(resource__pk=self.value())
        return queryset


class RegionFilter(SimpleListFilter):
    title = 'region'
    parameter_name = 'region'
    default_value = None

    def lookups(self, request, model_admin):
        list_of_regions = []
        queryset = Region.objects.all()
        for region in queryset:
            list_of_regions.append((str(region.id), region.name))
        return sorted(list_of_regions, key=lambda tp: tp[1])

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(region__pk=self.value())
        return queryset


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
        'carrier',
        'status',
        'quantity',
        'get_tracking',
    )
    list_filter = (
        ShippingStatusFilter,
        ShippingResourceFilter,
    )
    inlines = (TrackingInline, )

    def get_tracking(self, obj):
        tracking_list = list()
        for tracking in obj.tracking.all().order_by('-record_date'):
            tracking_list.append(str(tracking))
        return mark_safe("<br />".join(tracking_list))

    get_tracking.allow_tags = True
    get_tracking.short_description = 'Tracking'


class InventoryInline(admin.TabularInline):
    model = Inventory
    fields = (
        'resource',
        'producer',
        'quantity',
    )
    extra = 0


class RequestInline(admin.TabularInline):
    model = Request
    fields = (
        'consumer',
        'resource',
        'quantity',
        'done',
    )
    extra = 0


class ConsumerRequestAttentionFilter(SimpleListFilter):
    title = 'request attention'
    parameter_name = 'request_attention'
    default_value = None

    def lookups(self, request, model_admin):
        return ((False, 'Necesita material'), )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(requests__done=self.value()).distinct()
        return queryset


class RequestAttentionFilter(SimpleListFilter):
    title = 'request attention'
    parameter_name = 'request_attention'
    default_value = None

    def lookups(self, request, model_admin):
        return (
            (True, 'Necesidad satisfecha'),
            (False, 'Necesidad'),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(done=self.value()).distinct()
        return queryset


@admin.register(Consumer)
class ConsumerAdmin(admin.GeoModelAdmin):
    search_fields = (
        'id',
        'name',
    )
    list_display = (
        'name',
        'pk',
        'region',
        'point',
        'get_request_attention',
    )
    inlines = (RequestInline, )
    list_filter = (
        RegionFilter,
        ConsumerRequestAttentionFilter,
    )

    def get_request_attention(self, obj):

        request_list = list()
        for request in obj.requests.filter(done=False):
            request_list.append(str(request))
        return mark_safe("<br />".join(request_list))

    get_request_attention.short_description = 'Necesides'


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
        'region',
        'point',
        'production_capacity',
        'logistics_need',
    )
    list_filter = (RegionFilter, )
    inlines = (InventoryInline, )


@admin.register(Intermediary)
class IntermediaryAdmin(admin.GeoModelAdmin):
    search_fields = (
        'id',
        'name',
    )
    list_display = (
        'name',
        'pk',
        'region',
        'point',
    )
    list_filter = (RegionFilter, )


@admin.register(Carrier)
class CarrierAdmin(admin.GeoModelAdmin):
    search_fields = (
        'id',
        'name',
        'address',
        'phone',
    )
    list_display = (
        'name',
        'pk',
        'region',
        'address',
        'phone',
    )


@admin.register(Request)
class RequestAdmin(admin.GeoModelAdmin):
    search_fields = (
        'id',
        'consumer__name',
        'resource__name',
    )
    list_display = (
        'consumer',
        'pk',
        'resource',
        'quantity',
        'done',
    )
    list_filter = (RequestAttentionFilter, )
