# Generated by Django 3.2.7 on 2021-11-08 01:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizer', '0005_reviews_class_prof'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviews',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews_set', to='organizer.class'),
        ),
    ]
