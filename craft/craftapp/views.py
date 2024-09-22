from django.db.models import Count
from django.shortcuts import render, redirect
from craftapp import urls
from django.views import View
from django.http import HttpResponse
from . models import Cart, Product, Customer, Payment, OrderPlaced
from . forms import CustomerProfileForm, CustomerRegistrationForm
from django.contrib import messages
from django.db.models import Q
import razorpay
from django.conf import settings
from django.contrib.auth import logout

# Create your views here.
def home(request):  #When we fetch data from database then use function
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, "app/home.html",locals())

def about(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, "app/about.html",locals())

def contact(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, "app/contact.html",locals())

# class CategoryView(View):
#     def get(self,request,val):
#         return render(request, "app/category.html", locals())

def category(request,val):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    product = Product.objects.filter(category=val)
    title = Product.objects.filter(category=val).values("title")
    return render(request,"app/category.html", locals())

def categorytitle(request,val):
    product = Product.objects.filter(title=val)
    title = Product.objects.filter(category=product[0].category).values("title")
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,"app/category.html", locals())

class proddetails(View):  # when we have both get and post ,save delete data then use class
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,"app/productdt.html", locals())
    
class CustomerRegistration(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,"app/customerregistration.html", locals())
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations! User Register Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request,"app/customerregistration.html", locals())

class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,"app/profile.html", locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user,name=name,locality=locality,mobile=mobile,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request, "Your Profile Save Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request,"app/profile.html", locals())
    
def address(request):
    add = Customer.objects.filter(user=request.user)  # fetch profile only which customer login
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,"app/address.html", locals())

class updateAddress(View):
    def get(self,request,pk):  #pk is primary key ,we fetch the data from database
        add = Customer.objects.get(pk=pk)   #.get becoz we want only one row not an array
        form = CustomerProfileForm(instance=add)
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,"app/updateaddress.html", locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request," Profile Update Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return redirect("/address")
    

def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id = product_id)
    Cart(user=user,product=product).save()
    return redirect("/cart")

def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/addtocart.html', locals())

class checkout(View):
    def get(self,request):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount + 40
        razorpayamount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = { "amount": razorpayamount , "currency": "INR", "receipt": "order_rcptid_12"}
        payment_response = client.order.create(data=data)
        print(payment_response)
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_payment_status = order_status
            )
            payment.save()
        return render(request, 'app/checkout.html',locals())
    
def payment_done(request):
    order_id=request.GET.get('order_id')
    payment_id=request.GET.get('payment_id')
    cust_id=request.GET.get('cust.id')
    user=request.user
    customer=Customer.objects.get(id=cust_id)
    payment=Payment.objects.get(razorpay_order_id=order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity,payment=payment).save()
        c.delete()
    return redirect("/orders")

def search(request):
    query = request.GET['search']
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    product = Product.objects.filter(Q(title__icontains=query))
    return render(request, "app/search.html",locals())

def orders(request):
    orders_placed=OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', locals())

def user_logout(request):
    logout(request)
    return render (request, "app/login.html")

def update_cart(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('increment_'):
                product_id = int(key.split('_')[1])
                cart_item = Cart.objects.filter(user=request.user, product__id=product_id).first()
                if cart_item:
                    cart_item.quantity += 1
                    cart_item.save()
                    messages.success(request, "Quantity increased successfully.")
                else:
                    messages.error(request, "Cart item not found.")
            elif key.startswith('decrement_'):
                product_id = int(key.split('_')[1])
                
                cart_item = Cart.objects.filter(user=request.user, product__id=product_id).first()
                if cart_item:
                    if cart_item.quantity > 1:
                        cart_item.quantity -= 1
                        cart_item.save()
                        messages.success(request, "Quantity decreased successfully.")
                    else:
                        cart_item.delete()
                        messages.success(request, "Item removed from cart.")
                else:
                    messages.error(request, "Cart item not found.")
    return redirect('cart')

def remove_from_cart(request, product_id):
    cart_item = Cart.objects.filter(user=request.user, product__id=product_id).first()
    if cart_item:
        cart_item.delete()
        messages.success(request, "Item removed from cart.")
    else:
        messages.error(request, "Cart item not found.")
    return redirect('cart')