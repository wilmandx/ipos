from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from gestion.models import ValorTipo

# Create your views here.

@login_required
def venta_desktop(request):
    context = {'message':'ok'}
    return render(request, 'venta.html',context)


@login_required
def venta_mobile(request):
	list_categories=ValorTipo.objects.filter(padre=1)
	context = {'message':'ok','list_categories':list_categories}
	return render(request, 'mobile/venta.html',context)