from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
# Create your views here.
def detail (request):
    if request.user.is_authenticated:
        customer = request.user
        order, created= Order.objects.get_or_create(customer= customer,complete=False)
        items= order.order_nhanvien_set.all()
        user_not_login ="hidden"
        user_login ="show"
    else:
        items=[]    
        order={'get_cart_items':0,'get_cart_total':0} 
        user_not_login ="show"
        user_login ="hidden"
    id =request.GET.get('id','')
    nhanviens =Nhanvien.objects.filter(id=id)
    context= {'items':items,'order':order,'user_not_login':user_not_login, 'user_login':user_login, 'nhanviens': nhanviens}
    return render(request, 'app/detail.html', context)
def category(request):
    categories = Category.objects.filter(is_sub=False)
    active_category = request.GET.get('category', '')
    nhanviens = []  
    if active_category:
        nhanviens = Nhanvien.objects.filter(category__slug=active_category)
    context = {'categories': categories,'nhanviens': nhanviens,'active_category': active_category,}
    return render(request,'app/category.html',context)

def search(request):
    if request.method =="POST":
        searched = request.POST["searched"]
        keys = Nhanvien.objects.filter(name__contains = searched)
    if request.user.is_authenticated:
        customer = request.user
        order, created= Order.objects.get_or_create(customer= customer,complete=False)
        items= order.order_nhanvien_set.all()
        cartItems= order.get_cart_items
    else:
        items=[]    
        order={'get_cart_items':0,'get_cart_total':0}
        cartItems= order['get_cart_items']
    nhanviens = Nhanvien.objects.all()
    return render(request,'app/search.html',{"searched":searched,"keys":keys,'nhanviens': nhanviens})
def register(request):#đăng kí
    form = CreateUserForm
    if request.method =="POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    contex = {'form':form}
    return render(request,'app/register.html',contex)
def loginPage(request): #đang nhap
    if request.user.is_authenticated:
        return redirect('home')
    if request.method =="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username =username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else: 
            messages.info(request,'Tên đăng nhập hoặc tài khoản sai!')
    contex = {}
    return render(request,'app/login.html',contex)
def logoutPage(request): #đăng xuất
    logout(request)
    return redirect('login')
def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created= Order.objects.get_or_create(customer= customer,complete=False)
        items= order.order_nhanvien_set.all()
        cartItems= order.get_cart_items
        user_not_login ="hidden"
        user_login ="show"
    else:
        items=[]    
        order={'get_cart_items':0,'get_cart_total':0}
        cartItems= order['get_cart_items']
        user_not_login ="show"
        user_login ="hidden"
    categories = Category.objects.filter(is_sub =False)
    nhanviens = Nhanvien.objects.all()
    context= {'nhanviens': nhanviens ,'user_not_login':user_not_login, 'user_login':user_login,'categories':categories}
    return render(request, 'app/home.html', context)
def cart(request): #gio hang
    if request.user.is_authenticated:
        customer = request.user
        order, created= Order.objects.get_or_create(customer= customer,complete=False)
        items= order.order_nhanvien_set.all()
        user_not_login ="hidden"
        user_login ="show"
    else:
        items=[]    
        order={'get_cart_items':0,'get_cart_total':0} 
        user_not_login ="show"
        user_login ="hidden"
    context= {'items':items,'order':order,'user_not_login':user_not_login, 'user_login':user_login}
    return render(request, 'app/cart.html', context)
def checkout(request):#thanh toan
    if request.user.is_authenticated:
        customer = request.user
        order, created= Order.objects.get_or_create(customer= customer,complete=False)
        items= order.order_nhanvien_set.all()
        user_not_login ="hidden"
        user_login ="show"
    else:
        items=[]    
        order={'get_cart_items':0,'get_cart_total':0}
        user_not_login ="show"
        user_login ="hidden" 
    context= {'items':items,'order':order, 'user_not_login':user_not_login, 'user_login':user_login}
    return render(request, 'app/checkout.html', context)
from django.http import JsonResponse
import json

def updateItem(request): #giohang
    data = json.loads(request.body)
    nhanvienId = data['nhanvienId']
    action = data['action']

    customer = request.user
    nhanvien = Nhanvien.objects.get(id=nhanvienId)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderNhanvien, created = Order_nhanvien.objects.get_or_create(order=order, nhanvien=nhanvien)

    # Cập nhật diện tích
    if action == 'add':
        orderNhanvien.dientich += 1
    elif action == 'remove':
        orderNhanvien.dientich -= 1

    # Lưu lại sau khi cập nhật
    orderNhanvien.save()

    # Nếu diện tích <= 0, xóa bản ghi
    if orderNhanvien.dientich <= 0:
        orderNhanvien.delete()

    return JsonResponse('Item updated successfully', safe=False)