# Generated by Django 2.2.11 on 2020-03-21 11:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('logistica', '0008_auto_20200320_1959'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='consumer',
            options={'verbose_name_plural': 'consumers'},
        ),
        migrations.AlterModelOptions(
            name='intermediary',
            options={'verbose_name_plural': 'intermediaries'},
        ),
        migrations.AlterModelOptions(
            name='inventory',
            options={'verbose_name_plural': 'inventories'},
        ),
        migrations.AlterModelOptions(
            name='producer',
            options={'verbose_name_plural': 'producers'},
        ),
        migrations.AlterModelOptions(
            name='region',
            options={'verbose_name_plural': 'regions'},
        ),
        migrations.AlterModelOptions(
            name='resource',
            options={'verbose_name_plural': 'resources'},
        ),
        migrations.AlterModelOptions(
            name='shipping',
            options={'verbose_name_plural': 'shippings'},
        ),
        migrations.AlterModelOptions(
            name='tracking',
            options={'verbose_name_plural': 'tracking'},
        ),
        migrations.AddField(
            model_name='producer',
            name='telegram_id',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='Telegram id'),
        ),
        migrations.AddField(
            model_name='producer',
            name='telegram_nick',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Telegram nick'),
        ),
        migrations.AddField(
            model_name='producer',
            name='user',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='producers', to=settings.AUTH_USER_MODEL, verbose_name='Usuario real asociado'),
        ),
        migrations.AddField(
            model_name='tracking',
            name='record_date',
            field=models.DateTimeField(blank=True, db_index=True, default=django.utils.timezone.now, null=True, verbose_name='Fecha de evento'),
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('last_updated_date', models.DateTimeField(auto_now=True, db_index=True)),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notas')),
                ('quantity', models.IntegerField(default=0, verbose_name='Cantidad')),
                ('done', models.BooleanField(default=False, verbose_name='Necesidad satisfecha')),
                ('consumer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='requests', to='logistica.Consumer')),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='requests', to='logistica.Resource', verbose_name='Recurso')),
            ],
            options={
                'verbose_name_plural': 'requests',
            },
        ),
        migrations.CreateModel(
            name='Carrier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('last_updated_date', models.DateTimeField(auto_now=True, db_index=True)),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notas')),
                ('name', models.CharField(max_length=250, verbose_name='Nombre')),
                ('address', models.CharField(max_length=250, verbose_name='Dirección')),
                ('phone', models.CharField(max_length=250, verbose_name='Teléfono')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='carrier_points', to='logistica.Region')),
            ],
            options={
                'verbose_name_plural': 'carriers',
            },
        ),
        migrations.AddField(
            model_name='shipping',
            name='carrier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='shipping', to='logistica.Carrier', verbose_name='Transportista'),
        ),
    ]
