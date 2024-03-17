from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
import datetime
from django.db.models import *

# Create your models here.
class Slider(models.Model):
    DISCOUNT_DEAL = (("HOT DEALS", "HOT DEALS"), ("NEW ARRIVALS", "NEW ARRIVALS"))
    Image = models.ImageField(upload_to = "media/slider_imgs")
    Discount_deal = models.CharField(choices = DISCOUNT_DEAL , max_length=100)
    Sale = models.IntegerField()
    Brand_name = models.CharField(max_length=200)
    Discount = models.IntegerField()
    Link = models.CharField( max_length=200)
    
    def __str__(self):
        return self.Brand_name
    
class Banner_area(models.Model):
    Image = models.ImageField(upload_to = "media/banner_imgs")
    Discount_deal = models.CharField( max_length=100)
    Quote = models.CharField(max_length=200)
    Discount = models.IntegerField()
    Link = models.CharField( max_length=200, null = True)
    
    def __str__(self):
        return self.Quote
    
class Main_category(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
class Category(models.Model):
    main_category = models.ForeignKey(Main_category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name + " -- " + self.main_category.name

class Sub_category(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.category.main_category.name + " -- " + self.category.name + " -- " +  self.name  
      
class Section(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Color(models.Model):
    code = models.CharField( max_length=100)
    
    def __str__(self):
        return self.code

class Brand(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    total_quantity = models.IntegerField()
    availability = models.IntegerField()
    featured_image = models.CharField(max_length=500)
    product_name = models.CharField(max_length=500)
    
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null = True)
    
    price = models.IntegerField()
    Discount = models.IntegerField()
    
    tax = models.IntegerField(null = True) 
    packing_cost = models.IntegerField(null = True)
    
    Product_information = RichTextField()
    model_name = models.CharField(max_length=200)
    Categories = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null = True)
    
    Tags = models.CharField( max_length=200)
    Description = RichTextField()
    section = models.ForeignKey(Section, on_delete=models.DO_NOTHING, null=True,blank=True)
    
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)
    
    def __str__(self):
        return self.product_name
   
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("product_detail", kwargs={'slug': self.slug})
    
   
    class Meta:
        db_table = "app_Product"

def create_slug(instance, new_slug=None):
    slug = slugify(instance.product_name)
    if new_slug is not None:
        slug = new_slug
    qs = Product.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, Product)


class Coupon_code(models.Model):
    code = models.CharField( max_length=100) 
    discount = models.IntegerField()
    
    def __str__(self):
        return self.code
       
    
class Product_image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    image_url = models.CharField(max_length=500)
    
class Additional_info(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    specification = models.CharField( max_length=300)
    detail = models.CharField( max_length=300)     
  
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    firstname = models.CharField( max_length=200)
    lastname = models.CharField( max_length=200)
    country = models.CharField( max_length=200)
    address = models.TextField()
    city = models.CharField( max_length=200)
    state = models.CharField( max_length=200)
    postalcode = models.IntegerField()
    phone = models.IntegerField()
    email = models.EmailField( max_length=200)
    additional_info = models.TextField(blank = True)
    amount = models.CharField(max_length=100)
    payment_id = models.CharField( max_length=500, null = True, blank = True)
    paid = models.BooleanField(default = False, null = True)
    date = models.DateTimeField(default=datetime.datetime.now)
    

    def __str__(self):
        return self.user.username


   
class Order_item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.CharField(max_length=200)
    image = models.CharField(max_length=500)
    quantity = models.CharField( max_length=100)
    price = models.CharField( max_length=100)
    total = models.CharField( max_length=100)
    
    def __str__(self):
        return self.order.user.username
    
    
    
class Contact_us(models.Model):
    name = models.CharField( max_length=200)
    email = models.EmailField( max_length=200)
    subject = models.CharField( max_length=300)
    message = models.TextField()
    date = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.email
    
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
     
    def __str__(self):
        return self.user.username


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField(max_length = 500)
    rate = models.IntegerField(default = 0, null = True)
    created_at = models.DateTimeField(default=datetime.datetime.now)

     
    def __str__(self):
        return self.user.username
    
    