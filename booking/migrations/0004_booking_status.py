# Generated by Django 5.1.1 on 2024-10-26 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_remove_booking_menu_items_booking_menu_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('waiting', 'Waiting'), ('approved', 'Approved')], default='waiting', max_length=20),
        ),
    ]
