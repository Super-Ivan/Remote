from django.conf.urls import url
from data import views


urlpatterns = [
    url(r'items/', views.items),
    url(r'create/', views.create),
    url(r'deletesensor/', views.deleteSensor),
    url(r'safetycon/', views.safetyCon),
    url(r'submit/', views.submit),
    url(r'toradar/', views.toRadar),
    url(r'hisdata/', views.hisData),
    url(r'prtSc/', views.prtSc),
    url(r'datasender/', views.dataSender),
]
