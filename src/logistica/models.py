from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings
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

    class Meta:
        verbose_name_plural = _('regions')

    def __str__(self):
        return self.name


class Resource(BaseModel):
    name = models.CharField(
        max_length=250,
        null=False,
        blank=False,
        verbose_name='Name',
    )

    class Meta:
        verbose_name_plural = _('resources')

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

    class Meta:
        verbose_name_plural = _('inventories')

    def __str__(self):
        return f"{self.quantity} {self.resource.name}"


class Request(BaseModel):
    consumer = models.ForeignKey(
        'Consumer',
        null=True,
        related_name='requests',
        blank=True,
        on_delete=models.PROTECT,
    )
    resource = models.ForeignKey(
        'Resource',
        null=False,
        related_name='requests',
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
    done = models.BooleanField(
        default=False,
        verbose_name="Necesidad satisfecha",
    )

    class Meta:
        verbose_name_plural = _('requests')

    def __str__(self):
        done_str = ''
        if self.done:
            done_str = ' | Satisfecha | '
        return f"{self.quantity} {done_str} {self.resource.name}"


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
    telegram_nick = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        verbose_name='Telegram nick',
    )
    telegram_id = models.BigIntegerField(
        null=True,
        blank=True,
        verbose_name='Telegram id',
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
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        related_name='producers',
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
        verbose_name="Usuario real asociado",
    )

    class Meta:
        verbose_name_plural = _('producers')

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

    class Meta:
        verbose_name_plural = _('consumers')

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

    class Meta:
        verbose_name_plural = _('intermediaries')

    def __str__(self):
        return self.name


class Carrier(BaseModel):
    region = models.ForeignKey(
        'Region',
        null=False,
        related_name='carrier_points',
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

    class Meta:
        verbose_name_plural = _('carriers')

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
    record_date = models.DateTimeField(
        db_index=True,
        null=True,
        blank=True,
        default=timezone.now,
        verbose_name='Fecha de evento',
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

    class Meta:
        verbose_name_plural = _('tracking')

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
            date_string = self.record_date.strftime('%Y-%m-%d %H:%M')
        except AttributeError:
            date_string = 'DATE?'

        try:
            return f"{date_string} {result[0].name} -> {dict(self.STATUS_CHOICES).get(self.status)}"
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
    carrier = models.ForeignKey(
        'Carrier',
        null=True,
        related_name='shipping',
        blank=True,
        on_delete=models.PROTECT,
        verbose_name='Transportista',
    )
    quantity = models.IntegerField(
        null=False,
        blank=False,
        default=0,
        verbose_name='Cantidad',
    )

    class Meta:
        verbose_name_plural = _('shippings')

    def __str__(self):
        return f"{self.resource.name} -> {self.consumer.name}"
