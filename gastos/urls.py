from django.conf.urls import patterns, url

from gastos import views

urlpatterns = patterns('',
    url(r'^$', views.mostrar, name='mostrar'),
)