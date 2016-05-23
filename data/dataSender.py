# -*- coding: utf-8 -*-
import requests
import random
import time
import queue
import threading


urls = [
        'http://remoteviewer.applinzi.com/api/submit/?id=sensor5&token=pAaqdoSQ&step=10&unit=&val=',
        'http://remoteviewer.applinzi.com/api/submit/?id=sensor6&token=gYZOlgeQ&step=10&unit=&val=',
        'http://remoteviewer.applinzi.com/api/submit/?id=sensor4&token=naWfydQa&step=10&unit=&val=',
        'http://remoteviewer.applinzi.com/api/submit/?id=sensor7&token=GUnFmzDK&step=10&unit=&val=',
        'http://remoteviewer.applinzi.com/api/submit/?id=sensor11&token=AwNLHvly&step=10&unit=&val=',
        'http://remoteviewer.applinzi.com/api/submit/?id=sensor16&token=fFzusKYX&step=10&unit=&val=',
        'http://remoteviewer.applinzi.com/api/submit/?id=sensor12&token=qbbDdolz&step=10&unit=&val=',
        'http://remoteviewer.applinzi.com/api/submit/?id=sensor10&token=dtcPblNH&step=10&unit=m/s²&val=',
        ]
s = requests.session()
que = queue.Queue()


def doWork():
    while True:
        try:
            cmd = que.get_nowait()
            if cmd == 'q':
                print("It is time to break abd quit")
                break
        except:
            pass
        print('spider is still running:')
        for url in urls:
            val = random.randint(0, 100)
            url += str(val)
            print(url)
            s.get(url)
        time.sleep(0.2)


t = threading.Thread(target=doWork)
t.setDaemon(True)
t.start()

cmd = input()
que.put(cmd)
t.join()
