# Generated by Django 4.1.13 on 2024-09-29 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0004_gameentry_exposuretime_gameentry_lookawaytime_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameentry',
            name='report',
            field=models.TextField(blank=True, null=True),
        ),
    ]
