# Generated by Django 2.0.8 on 2019-01-11 18:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course_catalog', '0007_alters_created_on_field_20190111_1755'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='last_updated',
            new_name='updated_on',
        ),
        migrations.RenameField(
            model_name='courseinstructor',
            old_name='last_updated',
            new_name='updated_on',
        ),
        migrations.RenameField(
            model_name='courseprice',
            old_name='last_updated',
            new_name='updated_on',
        ),
        migrations.RenameField(
            model_name='coursetopic',
            old_name='last_updated',
            new_name='updated_on',
        ),
    ]
