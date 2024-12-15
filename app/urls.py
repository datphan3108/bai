from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register', views.register, name="register"), #dangki
    path('login/', views.loginPage, name="login"), #dangnhap
    path('category/', views.category, name="category"), #danhmuc
    path('detail/', views.detail, name="detail"), # chi tiet
    path('search/', views.search, name="search"), #tim kiem
    path('logout/', views.logoutPage, name="logout"), #dang xuat
    path('cart/', views.cart, name="cart"), #thanh toan
    path('checkout/', views.checkout, name="checkout"), #thanh toán
    path('update_item/', views.updateItem, name="update_item"), #update
]
