from django.conf.urls import url
from . import views

app_name = 'astrack'
urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^output/', views.return_data, name = 'output'),
    url(r'^upload_csv/', views.upload_csv, name = 'upload_csv'),
]
