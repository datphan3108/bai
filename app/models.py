from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# Create your models here.
class Category(models.Model): #danhmuc
    sup_category = models.ForeignKey('self',on_delete=models.CASCADE,related_name='sub_categories',null=True,blank=True)
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=200,null=True)
    slug = models.SlugField(max_length=200,unique=True)
    def __str__(self):
        return self.name
class CreateUserForm(UserCreationForm): #dangnhapdangki
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2']

class Nhanvien(models.Model): #sanpham
     category = models.ManyToManyField(Category, related_name='nhanvien')
     name = models.CharField(max_length=200,null=True)
     price = models.CharField(max_length=200, null=False, default="0")
     image = models.ImageField(null=True,blank=True)
     detail = models.TextField(null=True,blank=True)
     @property
     def imageurl(self):
        try:
            return self.image.url
        except ValueError:
            return ''
     def __str__(self):
        return self.name   
     
        
class Order(models.Model): #t
     customer = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
     date_order = models.DateTimeField(auto_now_add=True)
     complete = models.BooleanField(default=False,null=True,blank=False)
     transaction_id = models.CharField(max_length=200,null=True)

     def __str__(self):
          return str(self.id)
     @property
     def get_cart_items(self):
        order_nhanviens = self.order_nhanvien_set.all()  # Đảm bảo là `order_nhanvien_set` chứ không phải `ordernhanvien_set`
        total_area = sum([item.dientich for item in order_nhanviens])  # Tổng diện tích
        return total_area

     @property
     def get_cart_total(self):
        order_nhanviens = self.order_nhanvien_set.all()  # Đảm bảo là `order_nhanvien_set` chứ không phải `ordernhanvien_set`
        total_value = sum([item.get_total for item in order_nhanviens])  # Tổng giá trị
        return total_value

class Order_nhanvien(models.Model):
     nhanvien = models.ForeignKey(Nhanvien,on_delete=models.SET_NULL,null=True,blank=True)
     order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,blank=True)
     dientich=models.IntegerField(default=0, null=True, blank=True)
     date_added = models.DateTimeField(auto_now_add=True)
     @property
     def get_total(self):
          total = float(self.nhanvien.price) * float(self.dientich)
          return total

class Address(models.Model): #thanhtoan
     customer = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
     order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,blank=True)
     address = models.CharField(max_length=200,null=True)
     city = models.CharField(max_length=200,null=True)
     state = models.CharField(max_length=200,null=True)
     sdt = models.CharField(max_length=11,null=True)
     date_added = models.DateTimeField(auto_now_add=True)
      
     def __str__(self):
          return self.address    
