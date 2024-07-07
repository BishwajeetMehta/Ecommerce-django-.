from django.shortcuts import render,get_object_or_404,redirect
from . models import Categories,products,Order,Comment,Cart_Table,Cart_item,Subscriber,System_setting
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
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
            product_stock= product_status.filter(stock__gt=0) 
            #dummy price creted
            for prod in product_stock:
                if prod.discount > 0:
                    prod.dummy_price = prod.price * (1 + prod.discount / 100)
                else:
                    prod.dummy_price = prod.price

            category_products[category] = product_stock[:3]            
        else:
                category.status = False
                category.save()
        
    return HttpResponse(render(request,"home.html",{'categories_products':category_products}))

#function for each product description
def description(request,id):
    product_detail = products.objects.get(id=id)
    product_detail.dummy_price = product_detail.price * (1 + product_detail.discount / 100)
    return HttpResponse(render(request,"description.html",{'product':product_detail}))

#function for each Category and its related Products
def Category_page(request,id):
    category_list =get_object_or_404(Categories,id=id)
    product_list = products.objects.filter(Category = category_list)
    status = product_list.filter(status= True)
    Availabitlity = status.filter(stock__gt=0)
    #dummy price calculated
    for prod in Availabitlity:
                if prod.discount > 0:
                    prod.dummy_price = prod.price * (1 + prod.discount / 100)
                else:
                    prod.dummy_price = prod.price

    return HttpResponse(render(request,"category_page.html",{"product_list":Availabitlity,'category_list':category_list}))


#function to return order page for selected product
def OrderView(request,id ):
    product_detail = products.objects.get(id=id)
    return HttpResponse(render(request,"order.html",{'product':product_detail}))
 
# function for Ordering 
@login_required
def PlaceOrder(request,id):
    system_data = System_setting()
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
        #email feature
        subject = f' Order Confirmation '
        message = f"Dear { ordertable.user}, Your Order is Confirmed Sucessfuly !\nProduct name: {ordertable.product}\nQuantity:{ordertable.quantity}\nPrice:{ordertable.total_amount}\n \n \n Thank you for choosing Us as your Shooping Partner !\n{system_data.slogan} "
        from_email = '' #owner Email
        recipient_list = [request.user.email]
        send_mail(subject, message, from_email, recipient_list)
        messages.success(request, "Ordered sucessfully")
        return redirect("Order", id=id)
    return redirect("index")


#function to cancel Order
@login_required
def CancelOrder(request,id):
    system_data = System_setting()
    order = Order.objects.get(id=id)
    #stock updated in product table
    product = order.product
    product.stock += order.quantity
    product.save()
    # Mark order as canceled in order table
    order.status = 'Cancelled'
    order.save()
    #emailing 
    subject = f' Order cancellation '
    message = f"Dear { request.user}, Your Order is Cancelled Sucessfuly !\n \n \n Thank you for choosing Us as your Shooping Partner !\n{system_data.slogan} "
    from_email = '' #OwnerEmail
    recipient_list = [request.user.email]
    send_mail(subject, message, from_email, recipient_list)

    messages.success(request, "Your Order canceled sucessfully")
    return redirect("order_list", id=request.user.id)
   
@login_required
def order_list (request,id):
    orders = Order.objects.filter(user=id)
    return HttpResponse (render(request,"order_list.html",{"orders":orders}))

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
        messages.success(request, "Commented sucessfully !")
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
            messages.success(request, "cart id Already Exits !")
        carttable.user=request.user
        carttable.save() 
        return redirect('my_cart') # return cart list here of that user
        
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
            messages.success(request, "Added to cart sucessfully !")
            return redirect("Cartform",id=product_detail.id ) # return cart list here of that user
        return redirect("createCartIdForm")
    return redirect("Cartform",id=product_detail.id)

@login_required
def cart_list (request):
    if Cart_Table.objects.filter(user=request.user).exists():
        cart_id_existance = Cart_Table.objects.get(user=request.user)
        cart_data = Cart_item.objects.filter(cart_id=cart_id_existance)
        return HttpResponse (render(request,"cart_list.html",{"cartlist":cart_data}))
    return redirect("createCartIdForm")

@login_required
def delete_cart(request,id):
    data = Cart_item.objects.get(id=id)
    data.delete()
    messages.success(request, "Item Deleted from sucessfully !")
    return redirect("my_cart")

@login_required
def subscribers(request):
    if request.method == "POST" :
        data = request.POST
        subscriber_table = Subscriber()
        subscriber_table.name = request.user
        subscriber_table.email = data.get("email")
        subscriber_table.save()
        #emailing feature
        subject = f'Request for Subscription'
        message = f"Name: {subscriber_table.name}\nEmail: {subscriber_table.email}"
        from_email = '' #owneremail
        recipient_list = ['']  #owner email
        send_mail(subject, message, from_email, recipient_list)
        messages.success(request, "Subscribed sucessfully !")
        return redirect('index')



def search(request):
    search = request.GET.get("search","")
    product_status = products.objects.filter(status= True)
    product_stock= product_status.filter(stock__gt=0) 
    result =product_stock.filter(
            Q(name__icontains=search)|Q(description__icontains=search)|
            Q(price__icontains =search)|Q(brand__icontains = search)|Q(Category__name__icontains = search)
             ) 
    return HttpResponse(render(request,"search.html",{'products':result}))

