from . import views
from django.urls import include, re_path
app_name = 'myShop'
urlpatterns = [
    re_path(r'^home$', views.home, name='home'),
    re_path(r'^product/(?P<id>\w+)/$', views.product, name='product'),
    re_path(r'^basket/$', views.basket, name='basket'),
    re_path(r'^checkout/$', views.checkout , name='checkout'),
    re_path(r'^filter/$', views.filter , name='filter'),
    re_path(r'^pdf/$', views.generate_pdf , name='generate_pdf'),
]