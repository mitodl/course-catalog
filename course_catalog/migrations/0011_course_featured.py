# Generated by Django 2.0.10 on 2019-01-17 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_catalog', '0010_make_fields_nullable_20190114_1947'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='featured',
            field=models.BooleanField(default=False),
        ),
    ]
