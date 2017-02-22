from django.conf.urls import url
from . import views
app_name = 'forum'

urlpatterns = [
    url(r'^forum_create$',views.forum_create,name='forum_create'),
    url(r'^forum_index$',views.forum_index,name='forum_index'),
    url(r'^forum_index?page=([0-9]+)$',views.forum_index,name='forum_index'),
    url(r'^forum_index_tongzhi$',views.forum_index_tongzhi,name='forum_index_tongzhi'),
    url(r'^forum_index_tongzhi?page=([0-9]+)$',views.forum_index_tongzhi,name='forum_index_tongzhi'),
    url(r'^forum_index_jishu$',views.forum_index_jishu,name='forum_index_jishu'),
    url(r'^forum_index_jishu?page=([0-9]+)$',views.forum_index_jishu,name='forum_index_jishu'),
    url(r'^forum_index_bug$',views.forum_index_bug,name='forum_index_bug'),
    url(r'^forum_index_bug?page=([0-9]+)$',views.forum_index_bug,name='forum_index_bug'),
    url(r'^forum_index_mypost$',views.forum_index_mypost,name='forum_index_mypost'),
    url(r'^forum_index_mypost?page=([0-9]+)$',views.forum_index_mypost,name='forum_index_mypost'),
    url(r'^forum_content/(?P<id>[0-9]+)',views.forum_content),
]
# Create your views here.

# Create your views here.
