from django.conf.urls import patterns, url

from ventas import views

urlpatterns = patterns('',
    url(r'^$', views.venta_desktop, name='venta_desktop'),
    url(r'^mobile/$', views.venta_mobile, name='venta_mobile'),
    url(r'^listar/$', views.listar, name='listar'),
)