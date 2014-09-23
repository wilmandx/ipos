from django.contrib import admin
from gestion.models import Categoria,Producto
# Register your models here.

class ProductoInline(admin.TabularInline):
    model = Producto
    extra = 1

class CategoriaAdmin(admin.ModelAdmin):
	list_display = ('nombre','descripcion')
	search_fields=('nombre',)
	inlines = [ProductoInline]

class ProductoAdmin(admin.ModelAdmin):
	list_display = ('nombre','descripcion','precio',)
	search_fields=('nombre',)



admin.site.register(Categoria,CategoriaAdmin)
admin.site.register(Producto,ProductoAdmin)
