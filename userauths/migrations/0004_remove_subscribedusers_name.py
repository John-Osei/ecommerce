# Generated by Django 4.2 on 2023-05-05 11:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0003_subscribedusers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscribedusers',
            name='name',
        ),
    ]
