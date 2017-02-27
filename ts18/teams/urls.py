from django.conf.urls import url
from . import views


app_name = 'teams'

urlpatterns = [
    url(r'^index$', views.index, name='index'),
    url(r'^myteam$', views.myteam, name='myteam'),
    url(r'^new$', views.create, name='create'),
    url(r'^dismiss$', views.dismiss, name='dismiss'),
]
