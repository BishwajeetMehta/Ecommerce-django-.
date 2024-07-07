from django.contrib import admin

# Register your models here.
from . models import Categories,products,System_setting,Order, Comment,Cart_Table,Cart_item,Subscriber


# @admin.register(Product)
# class product (admin.ModelAdmin):
#     list_display = ("name","price","description","image","created_at")

@admin.register(Categories)
class Cateory(admin.ModelAdmin):
    list_display = ("id","name","image","status")

@admin.register(products)
class Products(admin.ModelAdmin):
    list_display = ("id","name","Category","description","price","discount","brand","image","stock","status")

@admin.register(System_setting)
class Settings(admin.ModelAdmin):
    list_display = ("id","name","email","phone","location","logo")

@admin.register(Order)
class Orders(admin.ModelAdmin):
    list_display =("id","user","product","quantity","status","total_amount","order_date")

@admin.register(Comment)
class Comment(admin.ModelAdmin):
    list_display = ("id","user","product","comment","comment_date")

@admin.register(Cart_Table)
class Cart_Table(admin.ModelAdmin):
    list_display = ("id","user")


@admin.register(Cart_item)
class Cart_item (admin.ModelAdmin):
    list_display = ("id","cart_id","product","quantity","added_date")

@admin.register(Subscriber)
class Subscriber(admin.ModelAdmin):
    list_display = ("id","name","email")