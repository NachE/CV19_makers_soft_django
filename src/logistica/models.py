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


class Production(BaseModel):
    name = models.ForeignKey(
        'Region',
        null=False,
        related_name='production_points',
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
