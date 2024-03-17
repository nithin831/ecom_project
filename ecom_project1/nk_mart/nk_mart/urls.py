"""
URL configuration for nk_mart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views as v


urlpatterns = [
    # path for error
    path("404", v.error404, name = "404"),
    
    # path for account (not built-in)
    # path("account/my_account", v.my_account, name = "my_account"),  # not required any more
    path("account/register", v.register, name = "handel_register"), #name = register is changed to handel_register because handel_register is the default name for register, if we are using django built-in for user account  
    path("account/login", v.Login, name = "handel_login"), #name = login is changed to handel_login because handel_login is the default name for login, if we are using django built-in for user account  
    
    # path for forget password which has default login, logout and others (i.e; instead of path("account/my_account", v.my_account, name = "my_account") path we can use the below path(django built-in))
    path('accounts/', include('django.contrib.auth.urls')),

    # path for profile
    path("account/profile", v.profile, name = "profile"),
    path("account/profile/update", v.profile_update, name = "profile_update"),
    path("about", v.about, name = "about"),
    path("contact", v.contact, name = "contact"),
    path('admin/', admin.site.urls),
    path("base/", v.base, name = "base"),
    path("", v.home, name = "home"),
    
    path("product", v.product, name = "product"),
    # path("review/", v.review, name = "review"),
    
    path('product/filter-data',v.filter_data,name="filter-data"), # for ajax
    
    path("product/<slug:slug>", v.Product_detail, name="product_detail"), # here name = product_detail should be same as in getabsolute_url method in models.py
    
    # cart related path
    path('cart/add/<int:id>/', v.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', v.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/', v.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/', v.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', v.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',v.cart_detail,name='cart_detail'),
    
    # path for checkout
    path("checkout", v.CHECKOUT, name= "checkout"),
    
    #path for place order
    path('checkout/placeorder',v.placeorder,name='placeorder'),
    
    path("success/", v.success, name = "success"),
    path("not_success/", v.not_success, name = "not_success"),
    
    path("your_order/", v.your_order, name = "your_order"),
    
    path("search", v.search, name = "search"),
    
    path("faqs/", v.faqs, name = "faqs"),
     
    path("wishlist/", v.WishlistView.as_view(), name = "wishlist"),
    path("add_wishlist/", v.add_wishlist, name = "add_wishlist"),
    path("delete_wishlist/", v.delete_wishlist, name = "delete_wishlist"),
    
    path("review/<int:id>", v.review, name = "review"),

    
     
] +static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
