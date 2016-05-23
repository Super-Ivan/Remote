from django.conf.urls import url
from view import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'device/', views.device),
]
