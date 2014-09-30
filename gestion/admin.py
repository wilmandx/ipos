from django.contrib import admin
from gestion.models import ValorTipo,Producto,DivPolitica
from django import forms
# Register your models here.

admin.site.register(ValorTipo)
admin.site.register(Producto)
admin.site.register(DivPolitica)

'''class ProductoInline(admin.TabularInline):
    model = Producto
    extra = 1

class TipoAdmin(admin.ModelAdmin):
	list_display = ('nombre','descripcion','padre','activo')
	search_fields=('nombre',)
	inlines = [ProductoInline]'''

class ProductoAdmin(admin.ModelAdmin):
	list_display = ('nombre','Marca','precio','valorVenta','iva','descripcion','foto')
	search_fields=('nombre',)
	#file = forms.FileField()



'''#admin.site.register(ValorTipo,TipoAdmin)
admin.site.register(Producto,ProductoAdmin)'''
