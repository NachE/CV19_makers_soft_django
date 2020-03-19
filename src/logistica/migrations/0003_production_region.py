# Generated by Django 2.2.11 on 2020-03-19 20:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('logistica', '0002_production_region'),
    ]

    operations = [
        migrations.AddField(
            model_name='production',
            name='region',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, related_name='production_points', to='logistica.Region'),
            preserve_default=False,
        ),
    ]