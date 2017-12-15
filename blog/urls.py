from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^post/$', views.my_post_new, name='post_new'),
#    url(r'^post/list/(?P<productname>\w{0,50})/$', views.post_shop_list, name='post_list'),
    url(r'^post/name', views.post_shop_list, name='post_list'),

]
