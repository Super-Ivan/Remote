# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from data.models import *


classes = [Temperature, Pressure, Illuminance,
           Humidity, Voltage, Custom]


def getSensors():
    num = 0
    sensors = []
    for cla in classes:
        cla_dict = {'type': cla.valueName}
        cla_dict.setdefault('items', [])
        for sensor in Sensors.objects.filter(type=cla.__name__):
            if sensor.safety_min and sensor.safety_max:
                condition = u'介于 %s 至 %s 之间' % (
                    sensor.safety_min, sensor.safety_max)
            elif sensor.safety_min:
                condition = u'大于 %s' % sensor.safety_min
            elif sensor.safety_max:
                condition = u'小于 %s' % sensor.safety_max
            else:
                condition = '---'
            t = Token.objects.get(sensorId=sensor.id)
            sensor_dict = {'name': sensor.name,
                           'id': 'sensor' + str(sensor.id),
                           'safety_min': sensor.safety_min,
                           'safety_max': sensor.safety_max,
                           'safetyCond': condition,
                           'submitUrl': '/api/submit/?id=sensor%s&token=%s&step=10&unit=&val=' % (
                               t.sensorId, t.token)
                           }
            cla_dict['items'].append(sensor_dict)
            num += 1
        sensors.append(cla_dict)
    if num == 0:
        sensors = []
    return sensors, num


def index(request):
    ctx = {'radarSensors': [],
           'sensors': [],
           'cnt': 0}
    for r in RadarChart.objects.all():
        r_dict = {'name': r.sensor.name}
        ctx['radarSensors'].append(r_dict)
    ctx['sensors'], ctx['cnt'] = getSensors()
    return render(request, 'view.html', ctx)


def device(request):
    if not request.user.is_staff:
        return HttpResponse('<p>请先联系管理员，通过专业用户验证</p>')
    ctx = {'classes': [],
           'sensors': []}
    for cla in classes:
        cla_add = {'name': cla.valueName,
                   'value': cla.__name__}
        ctx['classes'].append(cla_add)
    ctx['sensors'] = getSensors()[0]
    return render(request, 'device.html', ctx)
