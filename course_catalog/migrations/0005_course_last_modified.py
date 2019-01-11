# Generated by Django 2.0.8 on 2019-01-11 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_catalog', '0004_make_short_description_nullable_20190110_2018'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='last_modified',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='instructors',
            field=models.ManyToManyField(blank=True, related_name='courses', to='course_catalog.CourseInstructor'),
        ),
        migrations.AlterField(
            model_name='course',
            name='prices',
            field=models.ManyToManyField(blank=True, related_name='courses', to='course_catalog.CoursePrice'),
        ),
        migrations.AlterField(
            model_name='course',
            name='topics',
            field=models.ManyToManyField(blank=True, related_name='courses', to='course_catalog.CourseTopic'),
        ),
    ]
