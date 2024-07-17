from django.urls import path,include
from .views import CategoryViewset,ProductViewset,SystemSettingViewset,OrderViewset,CartViewset,UserViewset
from rest_framework_simplejwt.views import ( TokenObtainPairView,TokenRefreshView)

urlpatterns = [
    path('category',CategoryViewset.as_view({'get':'list'}), name= 'api_categories'),
    path('category/<int:pk>/',CategoryViewset.as_view({'get': 'retrieve'}), name= 'api_category'),
    path('product',ProductViewset.as_view({'get':'list'}), name= 'api_products'),
    path('product/<int:pk>/',ProductViewset.as_view({'get': 'retrieve'}), name= 'api_product'),
    path('category/<int:pk>/products/',ProductViewset.as_view({'get': 'get_products_by_category'})),
    path('systemdata/',SystemSettingViewset.as_view({'get':'list'}), name='systemdata'),
    path('order',OrderViewset.as_view({'post':'place_order'})),
    path('order/<int:pk>/',OrderViewset.as_view({'get': 'retrieve','post':'cancelorder'})),
    path('cart/<int:pk>/',CartViewset.as_view({'get':'retrieve','delete': 'destroy'}),name='api_my_cart'),
    path('cart',CartViewset.as_view({'post':'add_to_cart'}), name= 'add_to_cart'),
    path('user/<int:pk>/',UserViewset.as_view({'get':'retrieve','put':'update'})),
    
   
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
