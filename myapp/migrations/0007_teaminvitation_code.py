# Generated by Django 5.0.6 on 2024-06-21 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_teaminvitation_teaminvitation_unique_invitation'),
    ]

    operations = [
        migrations.AddField(
            model_name='teaminvitation',
            name='code',
            field=models.CharField(default=None, max_length=8),
            preserve_default=False,
        ),
    ]
