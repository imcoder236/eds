# Generated by Django 2.2.5 on 2020-05-22 06:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eds_app', '0010_auto_20200522_0627'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users_type_permission',
            name='user_id',
        ),
        migrations.DeleteModel(
            name='user_report',
        ),
        migrations.DeleteModel(
            name='users_type_permission',
        ),
    ]
