# Generated by Django 2.2 on 2022-03-24 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='adminid',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='user',
            name='adminid',
            field=models.IntegerField(),
        ),
    ]