from django.conf.urls import url
from . import views
app_name = 'fight'

urlpatterns = [
    url(r'^fight_index$',views.index,name='index'),
    url(r'^fight_myself$',views.myself,name='myself'),
    url(r'^logdownload', views.logdownload, name='logdownload'),
    url(r'^aidownload', views.aidownload, name='aidownload'),

]
# Create your views here.

# Create your views here.
