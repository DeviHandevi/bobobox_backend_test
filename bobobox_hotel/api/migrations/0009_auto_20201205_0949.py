# Generated by Django 3.1.4 on 2020-12-05 02:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20201204_1847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='promo_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='api.promo'),
        ),
    ]
