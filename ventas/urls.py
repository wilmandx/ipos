from django.conf.urls import patterns, url

from ventas import views

urlpatterns = patterns('',
    url(r'^$', views.venta_desktop, name='venta_desktop'),
    url(r'^fac/', views.venta_desktop, name='venta_desktop1'),
    url(r'^mobile/$', views.venta_mobile, name='venta_mobile'),
    url(r'^listar/$', views.listar, name='listar'),
    url(r'^clientes/', views.clientes, name='clientes'),
    url(r'^codproducto/', views.codproducto, name='codproducto'),
    url(r'^save/$', views.savePedido, name='save'),
    url(r'^saveDetalle/$', views.saveDetalle, name='saveDetalle'),
)