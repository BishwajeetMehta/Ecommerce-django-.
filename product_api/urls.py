from django.urls import path,include
from .views import CategoryViewset,ProductViewset,SystemSettingViewset,OrderViewset


urlpatterns = [
    path('category',CategoryViewset.as_view({'get':'list'}), name= 'api_categories'),
    path('category/<int:pk>/',CategoryViewset.as_view({'get': 'retrieve'}), name= 'api_category'),
    path('product',ProductViewset.as_view({'get':'list'}), name= 'api_products'),
    path('product/<int:pk>/',ProductViewset.as_view({'get': 'retrieve'}), name= 'api_product'),
    path('category/<int:pk>/products/',ProductViewset.as_view({'get': 'get_products_by_category'})),
    path('systemdata/',SystemSettingViewset.as_view({'get':'list'}), name='systemdata'),
    path('order/<int:pk>/',OrderViewset.as_view({'get': 'retrieve','post':'cancelorder'})),
    # path('cancelorder/<int:id>',OrderViewset.as_view({}))
   
   
]
