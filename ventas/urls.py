from django.conf.urls import patterns, url

from ventas import viewsInforme,viewsPedido

urlpatterns = patterns('',
    url(r'^$', viewsPedido.venta_desktop, name='venta_desktop'),
    url(r'^fac/', viewsPedido.venta_desktop, name='venta_desktop1'),
    url(r'^mobile/$', viewsPedido.venta_mobile, name='venta_mobile'),
    url(r'^listar/$', viewsInforme.listar, name='listar'),
    url(r'^clientes/', viewsPedido.clientes, name='clientes'),
    url(r'^vendedores/', viewsPedido.vendedores, name='vendedores'),
    url(r'^codproducto/', viewsPedido.codproducto, name='codproducto'),
    url(r'^nomproducto/', viewsPedido.nomproducto, name='nomproducto'),
    url(r'^save/$', viewsPedido.savePedido, name='save'),
    url(r'^save/(?P<anyway>\w+)/$', viewsPedido.savePedido, name='save'),
    url(r'^saveDetalle/$', viewsPedido.saveDetalle, name='saveDetalle'),
    url(r'^deleteDetalle/(?P<id>\d+)/$', viewsPedido.deleteDetalle, name='deleteDetalle'), 
    url(r'^pagar/$', viewsPedido.pagarPedido, name='pagarPedido'),
)