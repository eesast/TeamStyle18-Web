from django.conf.urls import url
from . import views
app_name = 'fight'

urlpatterns = [
    url(r'^fight_index$',views.index,name='index'),
    url(r'^fight_myself$',views.myself,name='myself'),
    url(r'^fight_rank$',views.rank,name='rank'),
    url(r'^download', views.download, name='download'),
]
# Create your views here.

# Create your views here.
