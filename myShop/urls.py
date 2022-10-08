from django.urls import path
from . import views
from django.urls import include, re_path
app_name = 'myShop'
urlpatterns = [
    re_path(r'^$', views.home, name='home'),
    re_path(r'^register', views.register, name='register'),
    re_path(r'^login', views.login, name='login'),
    re_path(r'^product/(?P<id>\w+)/$', views.product, name='product'),
    re_path(r'^official', views.official, name='official'),
    re_path(r'^basket/$', views.basket, name='basket'),
    re_path(r'^checkout/$', views.checkout , name='checkout'),
]