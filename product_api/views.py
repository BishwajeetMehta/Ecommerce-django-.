from django.shortcuts import render,redirect
from rest_framework.viewsets import ReadOnlyModelViewSet,ModelViewSet
from Product.models import Categories,products
from .serializers import CategorySerializer,ProductSerializer,SystemsettingSerializer,OrderSerializer,CartSerializer,UserSerializer
from .filters import ProductFilter
import django_filters.rest_framework
from rest_framework.response import Response
from rest_framework.decorators import action
from Product.models import Categories,products,System_setting,Order,Cart_item,Cart_Table
from Custom_Auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

# Create your views here.
class CategoryViewset(ReadOnlyModelViewSet):
    queryset = Categories.objects.filter(status=True)
    serializer_class = CategorySerializer

class ProductViewset(ReadOnlyModelViewSet):
    queryset = products.objects.filter(status= True)
    serializer_class = ProductSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = ProductFilter
    
    @action(detail=True, methods=['get'])
    def get_products_by_category(self, request, pk=None):
            category = Categories.objects.get(pk=pk)
            product = products.objects.filter(Category=category)
            serializer = ProductSerializer(product, many=True)
            return Response(serializer.data)
    
class SystemSettingViewset(ReadOnlyModelViewSet):
     queryset = System_setting.objects.all()
     serializer_class = SystemsettingSerializer


class OrderViewset(ModelViewSet):
      queryset = Order.objects.all()
      serializer = OrderSerializer
      permission_classes = [IsAuthenticated]

      def retrieve(self, request, pk=None):
        order = Order.objects.filter(user=pk)
        if order.exists():
            serializer = OrderSerializer(order, many=True)
            return Response(serializer.data)
        else:
             return Response({"message": " You do not placed any orders yet."})
        
    #   @action(methods=['post'],permission_classes=[IsAuthenticated])
      def cancelorder (self, request, pk=None):
           order = Order.objects.get(id= pk)
           product = order.product
           product.stock += order.quantity
           product.save()
    # Mark order as canceled in order table
           order.status = 'Cancelled'
           order.save()
           return Response({"message": "your order cancelled sucessfully"})
      
  
      def place_order(self,request):

           request.data["user"] = request.user.id
           serializer = OrderSerializer(data=request.data)
           if serializer.is_valid():
               product = products.objects.get(id = serializer.validated_data['product'].id)
               quantity = serializer.validated_data['quantity']

               if quantity > product.stock :
                    return Response({'msg': 'Please check the number of stocks available'})
               else:
                     product.stock -= quantity
                     product.save()
                     serializer.save()
                     return Response(serializer.data, status=status.HTTP_201_CREATED)
              
           return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

           

          
class CartViewset(ModelViewSet):
     queryset = Cart_item.objects.all()
     serializer_class = CartSerializer
     permission_classes = [IsAuthenticated]

     def retrieve(self, request, pk=None):
          user = Cart_Table.objects.filter(user= pk)
        
          if user.exists():
               cart_id_existance = Cart_Table.objects.get(user=pk)
               cartlist = Cart_item.objects.filter(cart_id=cart_id_existance)

               if cartlist.exists():
                serializer = CartSerializer(cartlist, many= True)
                return Response(serializer.data)
               
               else:
                     return Response({'message':'No cart item'})
               
          else:
               return Response({'message':'you do not have cart space'})
    
              
    #  @action(detail=True, methods=['delete'])
     def destroy(self, request, pk):
        cartitem = Cart_item.objects.get(id=pk)
        cartitem.delete()
        return Response({'message':'Cart item deleted sucessfully'})
     
     
     def add_to_cart(self,request):

          serializer = CartSerializer(data=request.data)

          if serializer.is_valid():
               cart_owner, created = Cart_Table.objects.get_or_create(user=request.user)
               cart_items_table = Cart_item()
               cart_items_table.cart_id = cart_owner
               cart_items_table.product = serializer.validated_data["product"]
               cart_items_table.quantity = serializer.validated_data["quantity"]
               cart_items_table.save() 
               return Response({'message': 'Added to cart sucessfully'})
               
          return Response({'message': 'something went wrong'})

class UserViewset(ModelViewSet):
     queryset = User.objects.all()
     serializer_class = UserSerializer
     permission_classes = [IsAuthenticated]

     def retrieve(self, request, pk):
          user = User.objects.get(id=pk)
          serializer = UserSerializer(user)
          return Response(serializer.data)
     
     def  update(self, request, pk):
          user = User.objects.get(id = pk)
          serializer = UserSerializer(user, request.data, partial= True)
          if serializer.is_valid():
               return Response(serializer.data,status=status.HTTP_200_OK)
     
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

          

          



          
         

         