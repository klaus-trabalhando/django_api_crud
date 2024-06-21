# Generated by Django 5.0.6 on 2024-06-21 15:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_team_teammember_teammember_unique_team_member'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamInvitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', max_length=10)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_invitations', to='myapp.team')),
            ],
        ),
        migrations.AddConstraint(
            model_name='teaminvitation',
            constraint=models.UniqueConstraint(fields=('team_id', 'email'), name='unique_invitation'),
        ),
    ]
