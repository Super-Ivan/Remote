# -*- coding: utf-8 -*-
import datetime
import random
from django.http import JsonResponse
from django.shortcuts import render
# from django.shortcuts import redirect
from Remote.settings import STATICFILES_DIRS
from data.models import *


value_models = {Temperature.__name__: Temperature,
                Pressure.__name__: Pressure,
                Illuminance.__name__: Illuminance,
                Humidity.__name__: Humidity,
                Voltage.__name__: Voltage,
                Custom.__name__: Custom,
                }
sensors_data = {'num': 0}


def getRandomCode(lens=8):
    code = ''
    libs = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for _ in range(lens):
        code += random.choice(libs)
    return code


def prtSc(request):
    try:
        from PIL import ImageGrab
        im = ImageGrab.grab()
        imgName = '{0}.jpg'.format(getRandomCode())
        saveName = '{0}/img/scrSht/{1}'.format(
            STATICFILES_DIRS[0].replace('\\', '/'), imgName)
        im.save(saveName)
        url = '/static/img/scrSht/' + imgName
        data = {'result': 'success',
                'imgUrl': url,
                'time': datetime.datetime.now().strftime('%Y-%m-%d, %H:%M')}
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse(
            {'msg': '截图失败，可能是Linux系统下不支持该截图方式。具体原因:' + str(e)})


def items(request):
    ctx = {'sensors_data': [],
           'radar_data': []}
    sensors = Sensors.objects.all()
    for sensor in sensors:
        sensor_for_display = {
            'name': sensor.name,
            'type': sensor.type,
            'id': 'sensor' + str(sensor.id),
            'val': None,
            'time': None,
            'safe': 1}
        try:
            v = getattr(sensor, sensor.type).latest('createTime')
            sensor_for_display['val'] = '%s %s' % (str(v.value), v.unit)
            sensor_for_display['time'] = v.createTime.strftime(
                '%Y-%m-%d, %H:%M')
            sensor_for_display['safe'] = v.safe
        except:
            pass
        ctx['sensors_data'].append(sensor_for_display)
    # radar: append the value of radar
    for r in RadarChart.objects.all():
        try:
            val = getattr(r.sensor, r.sensor.type).latest('createTime').value
        except:
            val = None
        ctx['radar_data'].append(val)
    ctx['result'] = 'success'
    return JsonResponse(ctx)


def submit(request):
    global sensors_data
    try:
        sensorId = int(request.GET['id'].split('sensor')[1])
        token = request.GET['token']
        val = int(request.GET['val'])
        step = int(request.GET['step'])
        if sensorId not in sensors_data:
            sensor = Sensors.objects.get(id=sensorId)
            sensors_data[sensorId] = [sensor]
        if token == Token.objects.get(sensorId=sensorId).token:
            # find the value model
            v = getattr(
                sensors_data[sensorId][0], sensors_data[sensorId][0].type).model()
            v.sensor = sensors_data[sensorId][0]
            v.value = val
            v.createTime = datetime.datetime.now()
            if request.GET['unit']:
                v.unit = request.GET['unit']
            # safe or not
            if sensors_data[sensorId][0].safety_max and\
                    sensors_data[sensorId][0].safety_min:
                if val > sensors_data[sensorId][0].safety_max or\
                        val < sensors_data[sensorId][0].safety_min:
                    v.safe = False
            elif sensors_data[sensorId][0].safety_max:
                if val > sensors_data[sensorId][0].safety_max:
                    v.safe = False
            elif sensors_data[sensorId][0].safety_min:
                if val < sensors_data[sensorId][0].safety_min:
                    v.safe = False
            # append the value object
            sensors_data[sensorId].append(v)
            sensors_data['num'] += 1
            # record all values
            if sensors_data['num'] >= 10 or\
                    datetime.datetime.now().second % 3 == 0:
                for sensor in sensors_data:
                    try:
                        values = sensors_data[sensor][1::step]
                        # whether sensor exit now
                        if Sensors.objects.get(id=sensor):
                            for v in values:
                                v.save()
                    except:
                        pass
                sensors_data = {'num': 0}
            return JsonResponse({'action': 'submit data',
                                 'result': 'success'})
        else:
            msg = 'token error'
        return JsonResponse({'action': 'submit data',
                             'result': 'failed',
                             'msg': msg})
    except Exception as e:
        return JsonResponse(
            {'action': 'submit data',
             'result': 'failed',
             'msg': str(e)})


def create(request):
    if not request.user.has_perm('data.add_sensors'):
        return JsonResponse({'action': 'create a new sensor',
                             'result': 'failed',
                             'msg': u"缺乏权限。请联系管理员，获取更高权限。",
                             })
    try:
        deviceType = request.POST['deviceType']
        deviceName = request.POST['deviceName']
        if deviceType not in value_models:
            msg = 'bad type of device'
            return JsonResponse({'action': 'create a new sensor',
                                 'result': 'failed',
                                 'msg': msg})
        new = Sensors()
        new.type = deviceType
        new.name = deviceName
        try:
            new.safety_min = int(request.POST['safety_min'])
        except:
            pass
        try:
            new.safety_max = int(request.POST['safety_max'])
        except:
            pass
        new.save()
        # create token
        t = Token(sensorId=new.id, token=getRandomCode())
        t.save()
        return JsonResponse({'action': 'create a new sensor',
                             'result': 'success',
                             'sensorName': deviceName,
                             'submitUrl': '/api/submit/?id=sensor%s&token=%s&step=10&val=' % (
                                 new.id, t.token)
                             })
    except Exception as e:
        return JsonResponse({'action': 'create a new sensor',
                             'result': 'failed',
                             'msg': str(e)})


def deleteSensor(request):
    if not request.user.has_perm('data.delete_sensors'):
        return JsonResponse({'action': 'delete a sensor',
                             'result': 'failed',
                             'msg': u"缺乏权限。请联系管理员，获取更高权限。",
                             })
    try:
        sensorId = int(request.GET['id'].split('sensor')[1])
        Sensors.objects.get(id=sensorId).delete()
        return JsonResponse({'action': 'delete sensor' + str(sensorId),
                             'result': 'success'})
    except Exception as e:
        return JsonResponse({'action': 'delete a sensor',
                             'result': 'failed',
                             'msg': str(e)})


def safetyCon(request):
    if not request.user.has_perm('data.change_sensors'):
        return JsonResponse({'action': 'modify the safety condition',
                             'result': 'failed',
                             'msg': u"缺乏权限。请联系管理员，获取更高权限。",
                             })
    try:
        sensorId = int(request.POST['sensorId'].split('sensor')[1])
        sensor = Sensors.objects.get(id=sensorId)
        try:
            sensor.safety_min = int(
                request.POST['safety_min'])
        except:
            sensor.safety_min = None
        try:
            sensor.safety_max = int(
                request.POST['safety_max'])
        except:
            sensor.safety_max = None
        sensor.save()
        return JsonResponse({'action': 'modify the safety condition',
                             'result': 'success'})
    except Exception as e:
        return JsonResponse({'action': 'modify the safety condition',
                             'result': 'failed',
                             'msg': str(e)})


def toRadar(request):
    if not request.user.has_perm('data.add_radarchart'):
        return JsonResponse({'action': 'add sensor to RadarChart',
                             'result': 'failed',
                             'msg': u"缺乏权限。请联系管理员，获取更高权限。",
                             })
    try:
        sensorId = int(request.GET['id'].split('sensor')[1])
        sensor = Sensors.objects.get(id=sensorId)
        RadarChart(sensor=sensor).save()
        return JsonResponse({'action': 'add to radar',
                             'result': 'success'})
    except Exception as e:
        return JsonResponse({'action': 'add to radar',
                             'result': 'failed',
                             'msg': str(e)})


def hisData(request):
    ctx = {'data': []}
    try:
        sensorId = int(request.POST['sensorId'].split('sensor')[1])
        starTime = datetime.datetime.strptime(
            request.POST['starTime'], '%H:%M,%Y-%m-%d')
        endTime = datetime.datetime.strptime(
            request.POST['endTime'], '%H:%M,%Y-%m-%d')
        sensor = Sensors.objects.get(id=sensorId)
        rec = getattr(sensor, sensor.type).filter(
            createTime__range=(starTime, endTime)).order_by('createTime')
        ctx['result'] = 'success'
        if len(rec) > 20:
            step = int(len(rec) / 20)
            rec = rec[::step]
        elif len(rec) <= 0:
            ctx['result'] = 'failed'
            ctx['msg'] = u'未找到符合条件的记录。请注意查询时间正确'
        for i in rec:
            ctx['data'].append(
                [i.createTime.strftime('%H:%M'), i.value])
        return JsonResponse(ctx)
    except Exception as e:
        ctx['result'] = 'failed'
        ctx['msg'] = str(e)
        return JsonResponse(ctx)


def dataSender(request):
    return render(request, 'dataSender.html')
