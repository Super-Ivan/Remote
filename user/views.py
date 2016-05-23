# -*-coding:utf-8-*-
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User, Permission


permissions = {'data.add_sensors': u'添加传感设备',
               'data.delete_sensors': u'删除传感设备',
               'data.change_sensors': u'修改传感设备安全范围',
               'data.add_radarchart': u'将设备添加至雷达监控',
               }


def index(request):
    if request.user.is_authenticated():
        return render(request, 'user.html')
    else:
        return redirect('/user/login/')


def login(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            if 'remember' not in request.POST:
                request.session.set_expiry(0)
            auth.login(request, user)
            return redirect('/user/')
        else:
            return HttpResponse(u'<p>登录失败</p>')
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/view/')


def setPassword(request):
    try:
        user_id = request.POST['user_id']
        newPassword = request.POST['newPassword']
        user = User.objects.get(id=user_id)
        user.set_password(newPassword)
        user.save()
        return HttpResponse(u'修改成功.<p><a href="/user/">点击此处重新登录</a></p>')
    except Exception as e:
        raise e


def manage(request):
    if request.user.is_superuser:
        ctx = {'user_not_staff': User.objects.filter(is_staff=False),
               'user_is_staff': User.objects.filter(is_staff=True)}
        return render(request, 'userManage.html', ctx)
    else:
        return HttpResponse(u'只有超级管理员才可以进行用户授权管理')


def toBeStaff(request):
    if request.user.is_superuser:
        users = request.POST.getlist('users_selected', [])
        for u in users:
            user = User.objects.get(id=u)
            user.is_staff = True
            user.save()
        return redirect('/user/manage/')
    else:
        return HttpResponse(u'只有超级管理员才可以进行用户授权管理')


def clearPower(request):
    if request.user.is_superuser:
        users = request.POST.getlist('users_selected', [])
        for u in users:
            user = User.objects.get(id=u)
            user.user_permissions.clear()
        return redirect('/user/manage/')
    else:
        return HttpResponse(u'只有超级管理员才可以进行用户授权管理')


def empower(request):
    if request.method == 'GET':
        try:
            user_id = request.GET['id']
            user = User.objects.get(id=user_id, is_staff=True)
            ctx = {'perms': [],
                   'user_info': {'username': user.username,
                                 'id': user.id}
                   }
            user_perms = user.get_all_permissions()
            for p in permissions:
                perm = {'name': permissions[p],
                        'codename': p,
                        'has_perm': 0}
                if p in user_perms:
                    perm['has_perm'] = 1
                ctx['perms'].append(perm)
            return render(request, 'empower.html', ctx)
        except:
            return HttpResponse(
                u'未能找到目标用户。请确认该用户存在并且已经过认证。<p><a href="/user/">点击此处返回，继续进行用户管理</a></p>')
    if request.method == 'POST':
        try:
            perms = request.POST.getlist('selected', [])
            user_id = request.POST['user_id']
            user = User.objects.get(id=user_id, is_staff=True)
            user.user_permissions.clear()
            for p in perms:
                codename = p.split('.')[1]
                perm = Permission.objects.get(codename=codename)
                user.user_permissions.add(perm)
            return HttpResponse(
                u'提交成功！<p><a href="/user/manage/">点击此处返回，继续进行用户管理</a></p>')
        except:
            return HttpResponse(
                u'提交失败。<p><a href="/user/manage/">点击此处返回，继续进行用户管理</a></p>')
