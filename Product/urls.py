from django.urls import path
from .import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
   
    path("description/<int:id>",views.description,name="decsription"),
    path('category/<int:id>',views.Category_page,name="category"),
    path ("prodOderView/<int:id>",views.OrderView,name="Order"), # url for page that requires order details 
    path('placeOrder/<int:id>',views.PlaceOrder,name="placeorder"), # order save
    path('canclorder/<int:id>',views.CancelOrder,name='cancle_order'), # cancel Oredr
    path('orders/<int:id>',views.order_list,name="order_list"), # orders of a particular customer
    path("comment/<int:id>",views.comment,name="comment"), #coment save 
    path("cartview/<int:id>",views.cartView,name="Cartform"),  #url for page that requires cart details 
    path("createcartidform",views.createcartidForm,name="createCartIdForm"), # view to create cart space for user 
    path('createcartid',views.createCartId,name="createcartid"),  #create cart id 
    path("addtocart/<int:id>",views.addToCart,name="addToCart"),  # save to cart
    path('mycarts',views.Cart_list,name='my_cart'), # carts of a particular user
    path('deletecart/<int:id>',views.Delete_cart,name="Delete_cart"), # delete cart item
    path('profile',views.profile,name="profile"), # user profile
    path('search',views.search,name="search"),# seaarch 
   

]
