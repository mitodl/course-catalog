# Generated by Django 2.0.8 on 2019-01-08 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_catalog', '0002_auto_20181221_1825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='instructors',
            field=models.ManyToManyField(related_name='courses', to='course_catalog.CourseInstructor'),
        ),
        migrations.AlterField(
            model_name='course',
            name='prices',
            field=models.ManyToManyField(related_name='courses', to='course_catalog.CoursePrice'),
        ),
        migrations.AlterField(
            model_name='course',
            name='topics',
            field=models.ManyToManyField(related_name='courses', to='course_catalog.CourseTopic'),
        ),
    ]
