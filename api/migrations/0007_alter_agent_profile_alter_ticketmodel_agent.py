# Generated by Django 4.2.20 on 2025-05-23 14:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_agent_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='profile',
            field=models.CharField(choices=[('administrator', 'administrator'), ('attendant', 'attendant')], max_length=50),
        ),
        migrations.AlterField(
            model_name='ticketmodel',
            name='agent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tickets', to='api.agent'),
        ),
    ]
