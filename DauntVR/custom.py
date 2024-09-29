from djongo import models
from django.db import migrations

def update_exposure_time(apps, schema_editor):
    GameEntry = apps.get_model('Dashboard', 'GameEntry')
    db = schema_editor.connection.alias
    GameEntry.objects.using(db).update(exposureTime=models.FloatField(default=0.0))

class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(update_exposure_time),
    ]