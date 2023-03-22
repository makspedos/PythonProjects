from django.urls import path
from . import views
from .views import Index
from django.urls import include, re_path
app_name = 'myShop'
urlpatterns = [
    re_path(r'^$', Index.as_view(), name='homepage'),
    re_path(r'^home$', views.home, name='home'),
    re_path(r'^product/(?P<id>\w+)/$', views.product, name='product'),
    re_path(r'^official', views.official, name='official'),
    re_path(r'^basket/$', views.basket, name='basket'),
    re_path(r'^checkout/$', views.checkout , name='checkout'),
]