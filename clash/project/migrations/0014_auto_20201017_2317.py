# Generated by Django 3.1 on 2020-10-17 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0013_register_time_rem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='register',
            name='bool',
        ),
        migrations.AddField(
            model_name='register',
            name='checkpoint',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='register',
            name='flags',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='register',
            name='marks',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='register',
            name='queflist',
            field=models.TextField(default='[]', max_length=255),
        ),
        migrations.AddField(
            model_name='register',
            name='spin_wheel',
            field=models.BooleanField(default=False),
        ),
    ]
