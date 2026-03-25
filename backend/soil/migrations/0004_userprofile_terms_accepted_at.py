# Generated migration to add terms_accepted_at to UserProfile

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soil', '0003_soilscan_user_alter_soilscan_crop_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='terms_accepted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
