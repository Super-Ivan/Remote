# -*-coding:utf-8-*-
from django.conf.urls import url
from user import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'login/', views.login),
    url(r'logout/', views.logout),
    url(r'setpassword/', views.setPassword),
    url(r'manage/', views.manage),
    url(r'empower/', views.empower),
    url(r'tobestaff/', views.toBeStaff),
    url(r'clearpower/', views.clearPower),
]
