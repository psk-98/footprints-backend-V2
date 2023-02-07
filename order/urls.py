from django.urls import path

from order import views

urlpatterns =  [
    path('orders/', views.OrderView.as_view()),
    path('address/', views.AddressView.as_view()),
    path('payment/', views.test_payment),
    path('payment/save-stripe-info/', views.save_stripe_info)
]