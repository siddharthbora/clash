# Generated by Django 3.1 on 2020-09-03 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_auto_20200902_2305'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='register',
            name='que',
        ),
        migrations.AddField(
            model_name='register',
            name='quelist',
            field=models.CharField(default=0, max_length=255),
            preserve_default=False,
        ),
    ]
