# Generated by Django 3.2.7 on 2021-11-08 19:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizer', '0008_auto_20211108_1913'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reviews',
            old_name='c',
            new_name='course',
        ),
    ]
