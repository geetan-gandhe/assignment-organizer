# Generated by Django 3.2.7 on 2021-11-30 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizer', '0028_merge_0027_auto_20211130_1412_0027_auto_20211130_2041'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='days',
            field=models.CharField(default='Monday/Wednesday/Friday', max_length=100),
        ),
        migrations.AddField(
            model_name='class',
            name='timing',
            field=models.CharField(default='11:00-12:15', max_length=100),
        ),
    ]
