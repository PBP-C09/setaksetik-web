# Generated by Django 5.1.1 on 2024-10-22 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spinthewheel', '0004_alter_spinhistory_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spinhistory',
            name='spin_time',
            field=models.DateField(auto_now_add=True),
        ),
    ]
