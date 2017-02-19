from django.conf.urls import url, include
from . import views
app_name = 'index'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^introduction$', views.introduction, name='introduction'),
    url(r'^notice$', views.noticeIndex, name='notice'),
    url(r'^rule$', views.rule, name='rule'),
    url(r'^download', views.download, name='download'),
]
