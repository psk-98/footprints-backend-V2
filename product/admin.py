from django.contrib import admin

from .models import Product, ProductImage, ProductStock
from django import forms


class ProductForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Product
        exclude = ['',]

    
class ImagesInline(admin.TabularInline):
    model = ProductImage

class StockInline(admin.TabularInline):
    model = ProductStock

class ProductFormAdmin(admin.ModelAdmin):
    form = ProductForm
    inlines = [ImagesInline, StockInline]
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Product, ProductFormAdmin)
# admin.site.register(ProductImage)
# admin.site.register(ProductStock)
