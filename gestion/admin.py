from django.contrib import admin
from gestion.models import ValorTipo,Producto,DivPolitica
from django import forms
# Register your models here.


class ValorTipoInline(admin.TabularInline):
    model = ValorTipo
    extra = 1

class ValorTipoAdmin(admin.ModelAdmin):
    list_display = ('id','nombre', 'activo')
    #list_filter = ('padre','activo')
    search_fields=('nombre',)
    exclude = ('padre','activo')
    inlines = [ValorTipoInline]
    list_display_links = ('id','nombre')
    def get_queryset(self, request):
        qs = super(ValorTipoAdmin, self).get_queryset(request)
        return qs.filter(padre=None)

class DivPoliticaAdmin(admin.ModelAdmin):
    list_display = ('id','codigo','nombre', 'descripcion')
    #list_filter = ('padre','activo')
    search_fields=('nombre','codigo')
    list_display_links = ('id','nombre')

class ProductoAdminForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(ProductoAdminForm, self).__init__(*args, **kwargs)
		# access object through self.instance...
		self.fields['tipoCategoria'].queryset = ValorTipo.objects.filter(padre=1)
		self.fields['tipoMarca'].queryset = ValorTipo.objects.filter(padre=4)

class ProductoAdmin(admin.ModelAdmin):
    form = ProductoAdminForm
    search_fields=('nombre','codigo')
    list_display = ('codigo','nombre','tipoCategoria','valorCompra','valorVenta','ivaPorcentaje')
    list_per_page=10

admin.site.register(ValorTipo,ValorTipoAdmin)
admin.site.register(DivPolitica,DivPoliticaAdmin)
admin.site.register(Producto,ProductoAdmin)

'''class ProductoInline(admin.TabularInline):
    model = Producto
    extra = 1

class TipoAdmin(admin.ModelAdmin):
	list_display = ('nombre','descripcion','padre','activo')
	search_fields=('nombre',)
	inlines = [ProductoInline]'''

'''class ProductoAdmin(admin.ModelAdmin):
	list_display = ('nombre','Marca','precio','valorVenta','iva','descripcion','foto')
	search_fields=('nombre',)
	#file = forms.FileField()'''



'''#admin.site.register(ValorTipo,TipoAdmin)
admin.site.register(Producto,ProductoAdmin)'''
