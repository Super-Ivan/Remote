# -*- coding: utf-8 -*-
from django.db import models


class Token(models.Model):

    sensorId = models.IntegerField()
    token = models.CharField(max_length=15)

    def __str__(self):
        return str(self.sensorId)


class Sensors(models.Model):

    name = models.CharField(max_length=15, unique=True)
    type = models.CharField(max_length=15)
    safety_min = models.IntegerField(null=True, blank=True)
    safety_max = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return '%s%s,%s' % (self.type, self.id, self.name)

    def shortname(self):
        if len(self.name > 6):
            return self.name[:5]
        else:
            return self.name


class RadarChart(models.Model):

    sensor = models.OneToOneField(Sensors)

    def __str__(self):
        return self.sensor.name


class Temperature(models.Model):

    valueName = u'温度'
    unit = models.CharField(max_length=15, default='℃')
    sensor = models.ForeignKey(Sensors, related_name='Temperature')
    value = models.IntegerField()
    createTime = models.DateTimeField()
    safe = models.BooleanField(default=True)

    class Meta:
        ordering = ('-createTime', )

    def __str__(self):
        return '%s:%s%s at %s' % (
            self.sensor.name,
            self.value,
            self.unit,
            self.createTime.strftime('%m-%d,%H:%M'))


class Pressure(models.Model):

    valueName = u'压力'
    unit = models.CharField(max_length=15, default='Pa')
    sensor = models.ForeignKey(Sensors, related_name='Pressure')
    value = models.IntegerField()
    createTime = models.DateTimeField()
    safe = models.BooleanField(default=True)

    class Meta:
        ordering = ('-createTime', )

    def __str__(self):
        return '%s:%s%s at %s' % (
            self.sensor.name,
            self.value,
            self.unit,
            self.createTime.strftime('%m-%d,%H:%M'))


class Illuminance(models.Model):

    valueName = u'光照度'
    unit = models.CharField(max_length=15, default='lx')
    sensor = models.ForeignKey(Sensors, related_name='Illuminance')
    value = models.IntegerField()
    createTime = models.DateTimeField()
    safe = models.BooleanField(default=True)

    class Meta:
        ordering = ('-createTime', )

    def __str__(self):
        return '%s:%s%s at %s' % (
            self.sensor.name,
            self.value,
            self.unit,
            self.createTime.strftime('%m-%d,%H:%M'))


class Humidity(models.Model):

    valueName = u'湿度'
    unit = models.CharField(max_length=15, default='%')
    sensor = models.ForeignKey(Sensors, related_name='Humidity')
    value = models.IntegerField()
    createTime = models.DateTimeField()
    safe = models.BooleanField(default=True)

    class Meta:
        ordering = ('-createTime', )

    def __str__(self):
        return '%s:%s%s at %s' % (
            self.sensor.name,
            self.value,
            self.unit,
            self.createTime.strftime('%m-%d,%H:%M'))


class Voltage(models.Model):

    valueName = u'电压'
    unit = models.CharField(max_length=15, default='V')
    sensor = models.ForeignKey(Sensors, related_name='Voltage')
    value = models.IntegerField()
    createTime = models.DateTimeField()
    safe = models.BooleanField(default=True)

    class Meta:
        ordering = ('-createTime', )

    def __str__(self):
        return '%s:%s%s at %s' % (
            self.sensor.name,
            self.value,
            self.unit,
            self.createTime.strftime('%m-%d,%H:%M'))


class Custom(models.Model):

    valueName = u'自定义'
    unit = models.CharField(max_length=15)
    sensor = models.ForeignKey(Sensors, related_name='Custom')
    value = models.IntegerField()
    createTime = models.DateTimeField()
    safe = models.BooleanField(default=True)

    class Meta:
        ordering = ('-createTime', )

    def __str__(self):
        return '%s:%s%s at %s' % (
            self.sensor.name,
            self.value,
            self.unit,
            self.createTime.strftime('%m-%d,%H:%M'))
