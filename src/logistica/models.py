from django.contrib.gis.db import models


class BaseModel(models.Model):
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
        related_name='Inventories',
        blank=False,
        on_delete=models.PROTECT,
        verbose_name='Recurso',
    )
    producer = models.ForeignKey(
        'Producer',
        null=False,
        related_name='Inventories',
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


class Shipping(BaseModel):
    STATUS_LOOKINGFOR_PRODUCER = 0
    STATUS_SENT = 1
    STATUS_RECEIVED = 2
    STATUS_CHOICES = (
        (STATUS_LOOKINGFOR_PRODUCER, 'Buscando productor'),
        (STATUS_SENT, 'Enviado'),
        (STATUS_RECEIVED, 'Recibido'),
    )

    status = models.IntegerField(
        default=STATUS_LOOKINGFOR_PRODUCER,
        choices=STATUS_CHOICES,
        verbose_name='Authorization status',
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
