from django.shortcuts import render,get_object_or_404,redirect
from . models import Categories,System_setting,products,Order,Comment,Cart_Table,Cart_item
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

# from django.core.serializers import serialize

# Create your views
# def Prod_list(request):
#     products = Product.objects.all()
#     return HttpResponse(render(request,"home.html",{"product":products}))


def Home(request):
    
    categories = Categories.objects.filter(status=True)
    category_products = {}
    for category in categories:
        product = products.objects.filter(Category=category) 
        # here the product existance is checked
        if product.exists():
            product_status = product.filter(status= True)
            product_stock= product_status.filter(stock__gt=0) #slice here to limit content
            category_products[category] = product_stock[:3]
        else:
                category.status = False
                category.save()
        # system settings stored in session 
    system_settings =list (System_setting.objects.all().values())
    category_session =list (Categories.objects.filter(status=True).values())
    request.session['system_data'] =system_settings
    request.session['categories']=category_session
    
    return HttpResponse(render(request,"home.html",{'categories_products':category_products}))

#function for each product description
def description(request,id):
    product_detail = products.objects.get(id=id)
    return HttpResponse(render(request,"description.html",{'product':product_detail}))

#function for each Category and its related Products
def Category_page(request,id):
    category_list =get_object_or_404(Categories,id=id)
    product_list = products.objects.filter(Category = category_list)
    status = product_list.filter(status= True)
    Availabitlity = status.filter(stock__gt=0)
    return HttpResponse(render(request,"category_page.html",{"product_list":Availabitlity,'category_list':category_list}))


#function to return order page for selected product
def OrderView(request,id ):
    product_detail = products.objects.get(id=id)
    return HttpResponse(render(request,"order.html",{'product':product_detail}))
 
# function for Ordering 
@login_required
def PlaceOrder(request,id):
    product_detail = products.objects.get(id=id)
    if request.method == "POST" :
        
        data=request.POST
        ordertable = Order()
        ordertable.user=request.user
        ordertable.product = product_detail
        ordertable.quantity = int (data.get("quantity"))
        ordertable.delivery_address = data.get("delivery_address")
        ordertable.save()
        product_detail.stock -= ordertable.quantity
        product_detail.save()
        return redirect("order_list", id=request.user.id)
    return HttpResponse("hello")


# Function for Commenting 
@login_required
def comment(request,id):
    product_detail = products.objects.get(id=id)
    if request.method == "POST" :
        data =request.POST
        comment_table = Comment()
        comment_table.user = request.user
        comment_table.product = product_detail
        comment_table.comment =data.get("comment")
        comment_table.save()
        return redirect("decsription", id=product_detail.id)

@login_required
def profile(request):
    return HttpResponse(render(request,"profile.html"))



def cartView(request,id ):
    product_detail = products.objects.get(id=id)
    return HttpResponse(render(request,"cart.html",{'product':product_detail}))

def createcartidForm(request):
    return HttpResponse(render(request,"createcart.html"))    

@login_required
def createCartId(request):
    if request.method =="POST":
        data = request.POST
        carttable = Cart_Table()
        if Cart_Table.objects.filter(user=request.user).exists():
            raise ValidationError("Cart space already exists for you")
        carttable.user=request.user
        carttable.save() 
        #flash msg and redirect
        return HttpResponse("cart id created sucessfully")
        
    return redirect("index")

@login_required
def addToCart (request,id):
    product_detail = products.objects.get(id=id)
    if request.method == "POST" :
        data = request.POST
        cart_item_table = Cart_item()
       
        if Cart_Table.objects.filter(user=request.user).exists():
            cart_id_existance = Cart_Table.objects.get(user=request.user)
            cart_item_table.cart_id = cart_id_existance
            cart_item_table.product = product_detail
            cart_item_table.quantity = data.get("quantity")
            cart_item_table.save()
            return HttpResponse("Sucessfuly added to cart ") # return cart list here of that user
        return redirect("createCartIdForm")
    return redirect("Cartform",id=product_detail.id)
            

def search(request):
    search = request.GET.get("search","")
    product_status = products.objects.filter(status= True)
    product_stock= product_status.filter(stock__gt=0) 
    result =product_stock.filter(
            Q(name__icontains=search)|Q(description__icontains=search)|
            Q(price__icontains =search)|Q(brand__icontains = search)|Q(Category__name__icontains = search)
             ) 
    print(result)
    return HttpResponse(render(request,"search.html",{'products':result}))

@login_required
def order_list (request,id):
    orders = Order.objects.filter(user=id)
    return HttpResponse (render(request,"order_list.html",{"orders":orders}))