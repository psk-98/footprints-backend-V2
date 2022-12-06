from django.urls import path, include

from product import views

urlpatterns = [
    path('products/', views.ProductsView.as_view()),
    path('product/', views.ProductView.as_view()),
    path('createproduct/', views.CreateProduct.as_view()),
    path('createstock/', views.upload_stock),
    path('productstock/', views.StockView.as_view()),
]