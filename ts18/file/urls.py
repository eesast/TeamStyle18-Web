from django.conf.urls import url, include
from . import views
app_name = 'file'

urlpatterns = [
    url(r'^notice$', views.noticeIndex, name='notice'),
    url(r'^download', views.download, name='download'),
]
