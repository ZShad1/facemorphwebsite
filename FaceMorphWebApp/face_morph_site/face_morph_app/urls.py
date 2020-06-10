from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('result/', views.result, name='result'),
]

urlpatterns += staticfiles_urlpatterns()
