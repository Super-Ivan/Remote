

# 数据结构sample


# 新的数据桥梁
sensors_data = {
    13: {
        'rawSensor': 'Sensor13',
        'realSensor': 'T13',
        'id': 'sensor13',
        'rawId': 13,
        'name': '室内测温',
        'type': '温度',
        'val': None,
        'sum': 0,
        'cnt': 0,
        'time': None,
        'safe': 1,
    },
}

template = {
    'name': '',
    'type': '',
    'id': '',
    'val': 0,
    'time': '',
    'safe': 1,
}
i = []
sensor_for_display = {}
for sensor in sensors_data:
    for attr in template:
        sensor_for_display[attr] = sensors_data[sensor][attr]
    i.append(sensor_for_display)





# data.views中打包封装的设备信息
# 也即是前端js实时更新数据时获得的items数据
items = [
    {
        'name': "室内测温",
        'type': "温度",
        'id': "sensor1",
        'val': "25℃",
        'time': "08:13 PM, Mar 11",
        'safe': 1,
    },
    {
        'name': "室外测温",
        'type': "温度",
        'id': "sensor2",
        'val': "30℃",
        'time': "08:13 PM, Mar 11",
        'safe': 1,
    },
    {
        'name': "压力测试",
        'type': "压力",
        'id': "sensor3",
        'val': "100kap",
        'time': "08:13 PM, Mar 11",
        'safe': 1,
    },
]


# data.views中，用于更新、临时记录设备实时数据值的字典:
sensors_val = {
    13: {
        'current': None,
        'sum': 0,
        'cnt': 0,
        'time': None,
    },
    14: {
        'current': 40,
        'sum': 500,
        'cnt': 10,
        'time': "08:14 PM, Mar 11",
    },
    15: {
        'current': 50,
        'sum': 500,
        'cnt': 10,
        'time': "08:15 PM, Mar 11",
    },
}
# 其中，当传感设备通过接口提交实时数据时，更新字典大概如下：
# sensors_val['sensor13']['current'] = 37


# view.views中，用于渲染模板所需的记录设备信息的字典:
ctx = {
    'sensors': [
        {
            'type': "温度",
            'items': [
                {
                    'name': "室内测温",
                    'id': "sensor1",
                    'safetyCond': "小于40℃",
                },
                {
                    'name': "室外测温",
                    'id': "sensor2",
                    'safetyCond': "小于50℃",
                }
            ]
        },
        {
            'type': "压力",
            'items': [
                {
                    'name': "压力测试",
                    'id': "sensor3",
                    'safetyCond': "小于10千帕",
                },
                {
                    'name': "压强监控",
                    'id': "sensor4",
                    'safetyCond': "小于200千帕",
                },
            ]
        },
    ]
}



sensors_data = [{'sensor':sensor1,'val':123,'time':123},{'sensor':sensor2,.....}]

sensors_data = {'sensor1':[{'val':123,'time':123},{'val':123,'time':123},{'val':123,'time':123}],
                'sensor2':[{'val':123,'time':123},{'val':123,'time':123},{'val':123,'time':123}],
                'num':6}



一、提交之后的数据何时记录的问题

# 第一种方案：结合sensor_data长度以及查询错误或数据未更新时。初步决定放弃这个方案
# 第一个记录数据的条件：
if sensors_data['num'] >= 20:
    record()
# 第二个条件：get items时查询到数据未更新时

# 第二种方案；长度+时间
if sensors_data['num'] >= 50 or datetime.datetime.second % 3 == 0:

二、记录数据时的颗粒度问题
# 每五个数据取样记录一次
for sensor in sensors_data:
    # step=5(or1) 以一定的颗粒度进行记录
    for i in sensors_data[sensor][::5]:
#       t = Temper()
#       t.val=sensors_data[sensor][i]['val']
#       t.time=sensors_data[sensor][i]['time']
        for cla in classes:
            if cla.__class__.name == sensor.type:
                s = cla()
                s.val = .....

三、不同传感器记录数值时数据结构不同的问题
# 湿度传感器有多种value：相对湿度和绝对湿度





# 第二种思路
# 字典里直接存放sensor_value object的实例
sensors_data = {1:[sensor1(真实的sensor object), T(t.val=123,t.time=123...),T(),T()...],
                2:[sensor2(真实的sensor object), P(p.val=123,p.time=123...),P(),P()...],
                'num':8}
# submit时，先确保该id和实例在这个临时字典中
if not sensors_data[sensorId]:
    sensor = Sensors.get(id=sensorId)
    sensors_data[sensorId] = [sensor]
# 接着找到对应的数据结构类型
for cla in classes:
    if cla.__name__ == sensors_data[sensorId][0].type:
        v = cla()
        v.sensor = sensors_data[sensorId][0]
        v.value = val
        v........
        break

# 记录record
for sensor in sensors_data:
    # from index 1,and the step is 5(or 1)
    values =  sensors_data[sensor][1:5]
    for v in values:
        v.save()


if sensors_data['num'] >= 20 or datetime.datetime.now().second % 5 == 0:
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