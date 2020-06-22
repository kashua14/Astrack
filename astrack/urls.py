from django.conf.urls import url
from . import views

app_name = 'astrack'
urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^upload_csv/', views.upload_csv, name = 'upload_csv'),
    url(r'^download/', views.download_rar, name = 'download')
    # url(r'^(?P<task_id>[\w-]+)/$', views.get_progress, name='task_status'),
]
