# Generated by Django 4.1.13 on 2024-09-28 21:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0002_alter_gameentry_exposuretime_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gameentry',
            name='exposureTime',
        ),
        migrations.RemoveField(
            model_name='gameentry',
            name='lookAwayTime',
        ),
        migrations.RemoveField(
            model_name='gameentry',
            name='overcomeTime',
        ),
        migrations.RemoveField(
            model_name='gameentry',
            name='sustainTime',
        ),
        migrations.RemoveField(
            model_name='gameentry',
            name='totalTime',
        ),
    ]
