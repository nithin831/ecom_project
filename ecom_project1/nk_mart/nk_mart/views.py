'''
note:
    > in template folder we have registration folder, where the same should be given for it and even files within it has to be given a same name.
    > it will be used for built-in django action for login, password, change, ect.
    > path for account related activity, which has default login, logout and others is 
         path('accounts/', include('django.contrib.auth.urls')), and it takes the name = (the file name in registration folder)
    '''
from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string

# used for filter of price
from django.db.models import Max, Min, Sum, Avg

from django.shortcuts import render, redirect, reverse

from core.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail

from django.views import generic

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# cart imports
from django.contrib.auth.decorators import login_required
from cart.cart import Cart

from django.views.decorators.csrf import csrf_exempt
import razorpay




# Create your views here.
def base(request):
    return render(request, "base.html")
    
def home(request):
    slider = Slider.objects.all().order_by("-id")[0:3]
    banner_area = Banner_area.objects.all().order_by("-id")[0:3]
    main_category = Main_category.objects.all()
    product = Product.objects.filter(section__name = "Top Deals of The Day")
    
    context = {"slider" : slider, "banner_area" : banner_area, "main_category" : main_category, "product" : product} 
    
    return render(request, "main/home.html", context)

def Product_detail(request, slug):
    product = Product.objects.filter(slug = slug)
    review = Review.objects.filter(product__slug = slug).order_by("-created_at")
    review_count = Review.objects.filter(product__slug = slug).count()
    if product.exists():
        product = Product.objects.get(slug = slug)
    else:
        return redirect("404")
        
    page_no = request.GET.get('page')
    page_nk = Paginator(review, 5)
    try:
        review = page_nk.page(page_no)
    except PageNotAnInteger:
        review = page_nk.page(1)
    except EmptyPage:
        review = page_nk.page(page_nk.num_pages)
    context = {"product" : product,"review":review, "review_count":review_count}
    return render(request, "product/product_detail.html", context)

def review(request, id):
    
    if request.method == "POST":
        
        product = Product.objects.get(id = id)
        user = request.user
        review = Review.objects.create(
            user = user,
            product = product,
            comment = request.POST.get("comment"),
            rate = request.POST.get("rate")
        )
    return redirect("product_detail", slug=product.slug)

def error404(request):
    return render(request, "errors/404.html")

# def my_account(request):
#     return render(request, "account/my_account.html")

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        if User.objects.filter(username = username).exists():
            messages.error(request, "Username already exists ")
            return redirect("login") # here "login" is present in path('accounts/', include('django.contrib.auth.urls')) and it goes to login.html
        
        if User.objects.filter(email = email).exists():
            messages.error(request, "Email id already exists!!! ")
            return redirect("login")
        
        user = User(username = username, email = email)
        user.set_password(password)
        user.save()
        msg = "Dear {}, \nThank you for registering on NK Market. Enjoy shoping \n\n\nRegards,\nNK Market Team".format(user)
        send_mail("Confirm Your Registration on NK Market", msg,"nkisnithinkumar@gmail.com",[user.email])
        return redirect("login")
    

def Login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Email and Password are Invalid")
            return redirect("login")
  
            
@login_required(login_url = '/accounts/login/')
def profile(request):
    return render(request, "profile/profile.html")
        
@login_required(login_url = '/accounts/login/')
def profile_update(request):
    if request.method =="POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_id = request.user.id
        user = User.objects.get(id=user_id)

        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        
        if password != None and password != "":
            user.set_password(password)
        user.save()
        messages.success(request, "Profile Updated Sucessfully !")
        return redirect('profile')

def about(request):
    return render(request, "main/about.html")


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        contact = Contact_us(name = name,email = email,subject = subject,message = message)
        
        subject = subject
        message = message + ", sent by \n" + email
        email_form = settings.EMAIL_HOST_USER
        try:
            send_mail(subject, message, email_form,["nkisnithinkumar@gmail.com"])
            contact.save()
            return redirect("home")
        except:
            return redirect("contact")
        
    return render(request, "main/contact.html")

def product(request):
    
    category = Category.objects.all()
    product = Product.objects.all()
    color = Color.objects.all()
    brand = Brand.objects.all()
    # filter by price
    min_price = Product.objects.all().aggregate(Min('price'))
    max_price = Product.objects.all().aggregate(Max('price'))
    # print(min_price)
    # print(max_price)

    FilterPrice = request.GET.get('FilterPrice')
    ColorID = request.GET.get("colorID")
    
    ATOZ = request.GET.get('ATOZ')
    ZTOA = request.GET.get('ZTOA')
    PRICE_LOWTOHIGH = request.GET.get('PRICE_LOWTOHIGH')
    PRICE_HIGHTOLOW= request.GET.get('PRICE_HIGHTOLOW')
    
    if FilterPrice:
        Int_FilterPrice = int(FilterPrice)
        product = Product.objects.filter(price__lte = Int_FilterPrice)
    
    elif ColorID:
        product = Product.objects.filter(color= ColorID)
        # if ~product.exists():
        #     product = Product.objects.all()
    
    elif ATOZ:
        product = Product.objects.all().order_by('product_name')
    elif ZTOA:
        product = Product.objects.all().order_by('-product_name')
    elif PRICE_LOWTOHIGH:
        product = Product.objects.all().order_by('price')
    elif PRICE_HIGHTOLOW:
        product = Product.objects.all().order_by('-price')
    else:
        product = Product.objects.all()
    
    page_no = request.GET.get('page')
    page_nk = Paginator(product, 8)
    try:
        product = page_nk.page(page_no)
    except PageNotAnInteger:
        product = page_nk.page(1)
    except EmptyPage:
        product = page_nk.page(page_nk.num_pages)
        
    context = {"category": category, "product" : product, 'min_price':min_price, 'max_price':max_price,'FilterPrice':FilterPrice,"color" : color, "brand" : brand,}
    return render(request, "product/product.html", context)


def filter_data(request):
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')

    allProducts = Product.objects.all().order_by('-id').distinct()
    if len(categories) > 0:
        allProducts = allProducts.filter(Categories__id__in=categories).distinct() # here in Categories__id__in=categories, Categories is the field the name in Product model and categories is this ->(categories = request.GET.getlist('category[]')) 

    if len(brands) > 0:
        allProducts = allProducts.filter(brand__id__in=brands).distinct() # here in brand__id__in = brands, brand is the field the name in Product model and brands is this ->(brands = request.GET.getlist('brand[]')) 


    t = render_to_string('ajax/product.html', {'product': allProducts})

    return JsonResponse({'data': t})





@login_required(login_url="/accounts/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_detail(request):
    cart = request.session.get("cart")
    packing_cost = sum(i['packing_cost'] for i in cart.values() if i)
    tax = sum(i['tax'] for i in cart.values() if i)
    # print(packing_cost, tax)
    # print(cart)
    
    coupon = None
    valid_coupon = None
    invalid_coupon = None
    if request.method == "GET":
        coupon_code=request.GET.get("coupon_code")
        
        
        if coupon_code:
            try:
                coupon=Coupon_code.objects.get(code=coupon_code)
                
                valid_coupon = " Applicable on Current Order !"
            except:
                invalid_coupon = "Invalid Coupon Code !"
    
    context = {"packing_cost": packing_cost, "tax": tax, "coupon":coupon, "valid_coupon": valid_coupon, "invalid_coupon" : invalid_coupon}
    return render(request, 'cart/cart.html', context)

def CHECKOUT(request):
    
   
    coupon_discount = None
    if request.method == "GET":
        coupon_discount = request.GET.get('coupon_discount')
        total = request.GET.get('total')
        amount_str = request.GET.get('total')
        amount_flt = float(amount_str)  
        amount = int(amount_flt)
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
        payment = client.order.create(dict(amount=amount, currency ="INR", payment_capture="1"))
        order_id = payment['id']
    if coupon_discount == None:
        coupon_discount = "not applicable"
        
    cart = request.session.get('cart')
    
    packing_cost = sum(i['packing_cost'] for i in cart.values() if i) 
    tax = sum(i['tax'] for i in cart.values() if i)
    
    tax_and_packing_cost = (packing_cost + tax)

    context = {'tax_and_packing_cost': tax_and_packing_cost, 'coupon_discount': coupon_discount, "tax":tax, "packing_cost":packing_cost, "total": total, "order_id":order_id,"payment":payment}
    
    return render(request, "checkout/checkout.html", context)


def search(request):
    query = request.GET.get('query') 
    product = Product.objects.filter(product_name__icontains = query) 
    context = {"product":product,}   
    return render(request, "product/search.html",context)


def placeorder(request):
    if request.method == "POST":
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(id = uid)
        
        cart = request.session.get('cart')
        
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        country = request.POST.get('country')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postalcode = request.POST.get('postalcode')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message')
        amount = request.POST.get('amount')
        
        order_id = request.POST.get('order_id')
        payment = request.POST.get('payment')
        
        total_cost = request.POST.get('amount')
        
        
        
        context = {"order_id":order_id, "total_cost":total_cost , "phone": phone, "user":user, "email":email, "payment": payment}
        
        order = Order(user = user, firstname = firstname, lastname = lastname, country = country, address = address,
                      city = city, state = state, postalcode = postalcode, phone = phone, email = email, 
                      additional_info = message, payment_id = order_id, amount = amount)
        order.save()
        
        for i in cart:
            a = int(cart[i]["price"])
            b = int(cart[i]["quantity"])
            total = a*b
            item = Order_item(user = user, order = order, product = cart[i]["product_name"], image = cart[i]["featured_image"],
                              quantity = cart[i]["quantity"], price = cart[i]["price"], total = total)
            item.save()
        return render(request, 'cart/placeorder.html', context)
 

 
@csrf_exempt    
def success(request):
    try:
        if request.method == "POST":
            a = request.POST
        
            order_id = ""
            for key,val in a.items():
                if key == "razorpay_order_id":
                    order_id = val
                    break
        
            user = Order.objects.filter(payment_id = order_id).first()
            
            print(user)
            user.paid = True
            user.save()
            
            msg = "your order will be recieved shortly. \n Thank you and continue shoping"
            send_mail("payment successful", msg,"nkisnithinkumar@gmail.com",[user.email])
    except:
        return redirect("not_success")          
        
    return render(request, 'cart/success.html')


def not_success(request):
    return render(request, "cart/not_sucess.html")

@login_required(login_url="/accounts/login/") 
def your_order(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(id = uid)
    # order = Order.objects.filter(user = user,paid = True)
    order_item = Order_item.objects.filter(user = user,)
    # page_no = request.GET.get('page')
    # page_nk = Paginator(order_item, 10)
    # try:
    #     order_item = page_nk.page(page_no)
    # except PageNotAnInteger:
    #     order_item = page_nk.page(1)
    # except EmptyPage:
    #     order_item = page_nk.page(page_nk.num_pages)
    
    context = {"order_item":order_item }
    return render(request, 'cart/your_order.html', context)



def faqs(request):
    return render(request, "faqs/faqs.html")


from django.utils.decorators import method_decorator


@method_decorator(login_required, name='get')
class WishlistView(generic.View):
    
    def get(self, *args, **kwargs):
        wish_items = Wishlist.objects.filter(user = self.request.user)
        page_no = self.request.GET.get('page')
        page_nk = Paginator(wish_items, 10)
        try:
            wish_items = page_nk.page(page_no)
        except PageNotAnInteger:
            wish_items = page_nk.page(1)
        except EmptyPage:
            wish_items = page_nk.page(page_nk.num_pages)
        context = {"wish_items":wish_items}
    
        return render(self.request, "wishlist/wishlist.html", context)

@csrf_exempt  
@login_required(login_url="/accounts/login/")    
def add_wishlist(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        prod = Product.objects.get(id = product_id)
        try:
            wish_item = Wishlist.objects.get(user = request.user, product = prod)
            if wish_item:
                return redirect("wishlist")
        except:
            Wishlist.objects.create(user = request.user, product = prod)
            
        finally:
            return HttpResponseRedirect(reverse("wishlist"))

@login_required(login_url="/accounts/login/")        
def delete_wishlist(request):
    if request.method == "POST":
        item_id = request.POST.get("item_id")
        Wishlist.objects.filter(id = item_id).delete()
        
        return HttpResponseRedirect(reverse("wishlist"))
            

