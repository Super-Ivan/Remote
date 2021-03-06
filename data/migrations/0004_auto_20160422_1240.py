# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-22 12:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0003_custom'),
    ]

    operations = [
        migrations.CreateModel(
            name='Humidity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.CharField(default='%', max_length=15)),
                ('value', models.IntegerField()),
                ('createTime', models.DateTimeField()),
                ('safe', models.BooleanField(default=True)),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Humidity', to='data.Sensors')),
            ],
            options={
                'ordering': ('-createTime',),
            },
        ),
        migrations.CreateModel(
            name='Illuminance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.CharField(default='lx', max_length=15)),
                ('value', models.IntegerField()),
                ('createTime', models.DateTimeField()),
                ('safe', models.BooleanField(default=True)),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Illuminance', to='data.Sensors')),
            ],
            options={
                'ordering': ('-createTime',),
            },
        ),
        migrations.CreateModel(
            name='Supersonicsounding',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.CharField(default='m', max_length=15)),
                ('value', models.IntegerField()),
                ('createTime', models.DateTimeField()),
                ('safe', models.BooleanField(default=True)),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Supersonicsounding', to='data.Sensors')),
            ],
            options={
                'ordering': ('-createTime',),
            },
        ),
        migrations.RemoveField(
            model_name='custom',
            name='valueName',
        ),
    ]
