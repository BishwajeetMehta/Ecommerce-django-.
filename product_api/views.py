from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet,ViewSet,ModelViewSet
from Product.models import Categories,products
from .serializers import CategorySerializer,ProductSerializer,SystemsettingSerializer,OrderSerializer
from .filters import ProductFilter
import django_filters.rest_framework
from rest_framework.response import Response
from rest_framework.decorators import action
from Product.models import Categories,products,System_setting,Order
from Custom_Auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

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
     queryset = System_setting.objects.all()[0]
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
        
    #   @action(methods=['get'],permission_classes=[IsAuthenticated])
      def cancelorder (self, request, pk=None):
           order = Order.objects.get(id= pk)
           product = order.product
           product.stock += order.quantity
           product.save()
    # Mark order as canceled in order table
           order.status = 'Cancelled'
           order.save()
           return Response({"message": "your order cancelled sucessfully"})

          
        