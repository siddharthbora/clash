# Generated by Django 3.1 on 2020-10-19 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0018_register_flashblind'),
    ]

    operations = [
        migrations.AddField(
            model_name='register',
            name='spincount',
            field=models.IntegerField(default=2),
        ),
    ]
