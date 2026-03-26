# Generated migration to add latitude and longitude to SoilScan

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soil', '0004_userprofile_terms_accepted_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='soilscan',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='soilscan',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
