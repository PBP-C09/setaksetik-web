# Generated by Django 5.1.2 on 2024-10-27 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('explore', '0010_alter_menu_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]