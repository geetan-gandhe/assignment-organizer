# Generated by Django 3.2.7 on 2021-11-07 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizer', '0003_reviews'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviews',
            name='review_text',
            field=models.TextField(default='Great class!', max_length=100),
        ),
    ]