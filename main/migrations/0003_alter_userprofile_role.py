# Generated by Django 5.1.1 on 2024-10-27 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_userprofile_delete_menuitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='role',
            field=models.CharField(choices=[('steak lover', 'Steak Lover'), ('steakhouse owner', 'Steakhouse Owner'), ('admin', 'Admin')], max_length=20),
        ),
    ]
