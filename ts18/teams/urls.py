from django.conf.urls import url
from . import views


app_name = 'teams'

urlpatterns = [
    url(r'^teams_index$', views.index, name='index'),
]
