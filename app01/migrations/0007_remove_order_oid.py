# Generated by Django 2.2 on 2022-04-05 11:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0006_auto_20220405_1053'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='oid',
        ),
    ]