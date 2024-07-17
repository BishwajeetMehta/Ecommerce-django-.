from rest_framework import serializers
from Product.models import Categories,products,System_setting,Order,Cart_item
from Custom_Auth.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model= products
        fields = '__all__'

class SystemsettingSerializer(serializers.ModelSerializer):
    class Meta:
        model= System_setting
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    # product = ProductSerializer()
    cart_id = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Cart_item
        fields = ['id','cart_id', 'product', 'quantity']

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id','username','first_name','last_name','email','phone','DoB','image']
        read_only_fields = ['username','id']