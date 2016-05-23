# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-22 09:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pressure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.CharField(default='Pa', max_length=15)),
                ('value', models.IntegerField()),
                ('createTime', models.DateTimeField()),
                ('safe', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('-createTime',),
            },
        ),
        migrations.CreateModel(
            name='RadarChart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Sensors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15, unique=True)),
                ('type', models.CharField(max_length=15)),
                ('safety_min', models.IntegerField(blank=True, null=True)),
                ('safety_max', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Temperature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.CharField(default='℃', max_length=15)),
                ('value', models.IntegerField()),
                ('createTime', models.DateTimeField()),
                ('safe', models.BooleanField(default=True)),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Temperature', to='data.Sensors')),
            ],
            options={
                'ordering': ('-createTime',),
            },
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sensorId', models.IntegerField()),
                ('token', models.CharField(max_length=15)),
            ],
        ),
        migrations.AddField(
            model_name='radarchart',
            name='sensor',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='data.Sensors'),
        ),
        migrations.AddField(
            model_name='pressure',
            name='sensor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Pressure', to='data.Sensors'),
        ),
    ]
