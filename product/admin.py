from django.contrib import admin

from .models import Product, ProductImage, ProductStock

admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductStock)
