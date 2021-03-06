# Generated by Django 2.2 on 2022-04-05 02:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_remove_user_userid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oid', models.IntegerField(max_length=128)),
                ('title', models.CharField(max_length=128)),
                ('ordertime', models.DateField()),
                ('state', models.IntegerField(max_length=8)),
                ('orderadmin', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='userorder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordercontent', models.CharField(max_length=256)),
                ('orderid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Order')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.User')),
            ],
        ),
    ]
