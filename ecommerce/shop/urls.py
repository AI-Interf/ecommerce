from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop, name='shop'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('updateItem/', views.updateItem, name='updateItem'),
    path('process/', views.process, name='process'),

]