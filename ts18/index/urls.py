from django.conf.urls import url, include
from . import views
app_name = 'index'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^intro$', views.intro, name='intro'),
    url(r'^rule$', views.rule, name='rule'),
]
