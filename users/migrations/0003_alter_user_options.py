# Generated by Django 5.0.2 on 2024-02-25 08:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_share'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'کاربر', 'verbose_name_plural': 'Users'},
        ),
    ]