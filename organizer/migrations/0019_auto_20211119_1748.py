# Generated by Django 3.1.13 on 2021-11-19 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizer', '0018_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todolist',
            name='created',
            field=models.DateField(default='2021-11-19'),
        ),
        migrations.AlterField(
            model_name='todolist',
            name='due_date',
            field=models.DateField(default='2021-11-19'),
        ),
    ]
