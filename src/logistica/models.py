from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.gis.db import models


class BaseModel(models.Model):
    created_date = models.DateTimeField(db_index=True, auto_now_add=True)
    last_updated_date = models.DateTimeField(db_index=True, auto_now=True)
    notes = models.TextField(
        null=True,
        blank=True,
        verbose_name='Notas',
    )

    class Meta:
        abstract = True


class Region(BaseModel):
    name = models.CharField(
        max_length=250,
        null=False,
        blank=False,
        verbose_name='Región',
    )

    def __str__(self):
        return self.name


class Resource(BaseModel):
    name = models.CharField(
        max_length=250,
        null=False,
        blank=False,
        verbose_name='Name',
    )

    def __str__(self):
        return self.name


class Inventory(BaseModel):
    resource = models.ForeignKey(
        'Resource',
        null=False,
        related_name='inventories',
        blank=False,
        on_delete=models.PROTECT,
        verbose_name='Recurso',
    )
    producer = models.ForeignKey(
        'Producer',
        null=False,
        related_name='inventories',
        blank=False,
        on_delete=models.PROTECT,
        verbose_name='Punto de producción',
    )
    quantity = models.IntegerField(
        null=False,
        blank=False,
        default=0,
        verbose_name='Cantidad',
    )

    def __str__(self):
        return f"{self.quantity} {self.resource.name}"


class Producer(BaseModel):
    region = models.ForeignKey(
        'Region',
        null=False,
        related_name='producer_points',
        blank=False,
        on_delete=models.PROTECT,
    )
    name = models.CharField(
        max_length=250,
        null=False,
        blank=False,
        verbose_name='Nombre',
    )
    point = models.PointField(
        verbose_name='Geospatial point',
        spatial_index=True,
        # 4326 == WGS84
        # https://en.wikipedia.org/wiki/World_Geodetic_System#WGS84
        srid=4326,
    )
    production_capacity = models.IntegerField(
        default=1,
        verbose_name='Capacidad de producción',
    )
    logistics_need = models.BooleanField(
        default=False,
        verbose_name="Necesidad logística",
    )

    def __str__(self):
        return self.name


class Consumer(BaseModel):
    region = models.ForeignKey(
        'Region',
        null=False,
        related_name='consumer_points',
        blank=False,
        on_delete=models.PROTECT,
    )
    name = models.CharField(
        max_length=250,
        null=False,
        blank=False,
        verbose_name='Nombre',
    )
    address = models.CharField(
        max_length=250,
        null=False,
        blank=False,
        verbose_name='Dirección',
    )
    phone = models.CharField(
        max_length=250,
        null=False,
        blank=False,
        verbose_name='Teléfono',
    )
    point = models.PointField(
        verbose_name='Geospatial point',
        spatial_index=True,
        # 4326 == WGS84
        # https://en.wikipedia.org/wiki/World_Geodetic_System#WGS84
        srid=4326,
    )

    def __str__(self):
        return self.name


class Intermediary(BaseModel):
    region = models.ForeignKey(
        'Region',
        null=False,
        related_name='intermediary_points',
        blank=False,
        on_delete=models.PROTECT,
    )
    name = models.CharField(
        max_length=250,
        null=False,
        blank=False,
        verbose_name='Nombre',
    )
    address = models.CharField(
        max_length=250,
        null=False,
        blank=False,
        verbose_name='Dirección',
    )
    phone = models.CharField(
        max_length=250,
        null=False,
        blank=False,
        verbose_name='Teléfono',
    )
    point = models.PointField(
        verbose_name='Geospatial point',
        spatial_index=True,
        # 4326 == WGS84
        # https://en.wikipedia.org/wiki/World_Geodetic_System#WGS84
        srid=4326,
    )

    def __str__(self):
        return self.name


class Tracking(BaseModel):
    STATUS_AWAITING = 0
    STATUS_SENT = 1
    STATUS_RECEIVED = 2
    STATUS_SCHEDULED = 3

    STATUS_CHOICES = (
        (STATUS_AWAITING, 'Esperando'),
        (STATUS_SENT, 'Enviado'),
        (STATUS_RECEIVED, 'Recibido'),
        (STATUS_SCHEDULED, 'Programado'),
    )

    status = models.IntegerField(
        default=STATUS_AWAITING,
        choices=STATUS_CHOICES,
        verbose_name='Estado',
    )
    scheduled_date = models.DateTimeField(
        db_index=True,
        null=True,
        blank=True,
        default=None,
        verbose_name='Programado',
    )
    consumer = models.ForeignKey(
        'Consumer',
        null=True,
        related_name='tracking',
        blank=True,
        on_delete=models.PROTECT,
    )
    producer = models.ForeignKey(
        'Producer',
        null=True,
        related_name='tracking',
        blank=True,
        on_delete=models.PROTECT,
    )
    intermediary = models.ForeignKey(
        'Intermediary',
        null=True,
        related_name='tracking',
        blank=True,
        on_delete=models.PROTECT,
    )
    shipping = models.ForeignKey(
        'Shipping',
        null=False,
        related_name='tracking',
        blank=False,
        on_delete=models.CASCADE,
    )

    def clean(self):
        # Allow set only one of consumer, producer or intermediary
        if [self.consumer, self.producer,
                self.intermediary].count(None) in [3, 1]:
            raise ValidationError(
                _('Please, set consumer or producer or intermediary (only one)'
                  ))

    def __str__(self):
        places = [self.consumer, self.producer, self.intermediary]
        result = [place for place in places if place is not None]
        try:
            return f"{self.last_updated_date.strftime('%Y-%m-%d %H:%M')} {result[0].name} -> {dict(self.STATUS_CHOICES).get(self.status)}"
        except IndexError:
            return 'UNKNOWN'


class Shipping(BaseModel):
    STATUS_AWAITING = 0
    STATUS_SENT = 1
    STATUS_RECEIVED = 2
    STATUS_SCHEDULED = 3

    STATUS_CHOICES = (
        (STATUS_AWAITING, 'Esperando'),
        (STATUS_SENT, 'Enviado'),
        (STATUS_RECEIVED, 'Recibido'),
        (STATUS_SCHEDULED, 'Programado'),
    )

    status = models.IntegerField(
        default=STATUS_AWAITING,
        choices=STATUS_CHOICES,
        verbose_name='Estado',
    )
    consumer = models.ForeignKey(
        'Consumer',
        null=False,
        related_name='shipping',
        blank=False,
        on_delete=models.PROTECT,
    )
    producer = models.ForeignKey(
        'Producer',
        null=True,
        related_name='shipping',
        blank=True,
        on_delete=models.PROTECT,
    )
    resource = models.ForeignKey(
        'Resource',
        null=False,
        related_name='shipping',
        blank=False,
        on_delete=models.PROTECT,
        verbose_name='Recurso',
    )
    quantity = models.IntegerField(
        null=False,
        blank=False,
        default=0,
        verbose_name='Cantidad',
    )

    def __str__(self):
        return f"{self.resource.name} -> {self.consumer.name}"
