from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ipos.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^ventas/', include('ventas.urls',namespace="ventas")),
    url(r'^gastos/', include('gastos.urls',namespace="gastos")),
    url(r'^$', 'ipos.views.home', name='home'),
)
