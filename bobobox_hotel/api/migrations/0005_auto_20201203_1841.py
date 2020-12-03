# Generated by Django 3.1.4 on 2020-12-03 11:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20201203_1648'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stay',
            name='room_id',
        ),
        migrations.AddField(
            model_name='stayroom',
            name='room_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='api.room'),
            preserve_default=False,
        ),
    ]
