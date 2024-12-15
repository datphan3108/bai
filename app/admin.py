from django.contrib import admin
from .models import *
admin.site.register(Nhanvien)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Order_nhanvien)
admin.site.register(Address)

# Register your models here.
