from django.db import models
from django.conf import settings
from Custom_Auth.models import User
# Create your models here.
# class Product(models.Model):
#     name = models.CharField(max_length=150)
#     price = models.CharField( max_length=50)
#     description = models.TextField()
#     image = models.ImageField(upload_to='images/')
#     created_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#        return self.name
    

class Categories(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/categories')
    status = models.IntegerField(default="1")

    def __str__(self):
        return self.name
    
class products(models.Model):
    name = models.CharField(max_length=250)
    Category =models.ForeignKey(Categories,on_delete=models. CASCADE)
    description = models.TextField()
    price = models.IntegerField()
    discount = models.IntegerField(null=True)
    brand = models.CharField(max_length=200,default="Unknown")
    image = models.ImageField(upload_to="images/product")
    stock = models.IntegerField(default="1")
    status = models.IntegerField(default="1")



    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,editable=False)
    delivery_address = models.TextField()
    order_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_amount = self.product.price * self.quantity
        super().save(*args, **kwargs)


    def __str__(self):
        return self.product.name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(products, on_delete=models.CASCADE)
    comment = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.user.first_name


class Cart_Table(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.first_name
    

class Cart_item (models.Model):
    cart_id = models.ForeignKey(Cart_Table,on_delete = models.CASCADE)
    product = models.ForeignKey(products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    added_date = models.DateTimeField(auto_now_add=True)
    

    def __str__(self) -> str:
        return self.cart_id.user.first_name



class System_setting(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone =models.CharField(max_length=20)
    location = models.CharField(max_length=150)
    logo = models.ImageField(upload_to="images/system")
    slogan = models.CharField(max_length=250, default='Shop. Save. Smile.')


    def save(self, *args, **kwargs):
        if System_setting.objects.exists():
            System_setting.objects.all().delete()
        super(System_setting, self).save(*args, **kwargs)

    def _str_(self):
        return self.name
    

class Subscriber(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()

    def _str_(self):
        return self.email

