# Generated by Django 3.1 on 2020-10-19 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0019_register_spincount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register',
            name='freezetimestart',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
