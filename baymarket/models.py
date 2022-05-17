from datetime import date
from threading import activeCount
from django.db import models
from slugify import slugify
from django_resized import ResizedImageField
from control.models import Account, Company
import random 
import string




def random_id():
    id = ""
    for i in range(8):
        id += random.choice(string.hexdigits)
    return id

class Category(models.Model): 
    img = ResizedImageField(size=[600,600], quality=100, upload_to="baymarket/categories/")
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    slug = models.CharField(max_length=250)
    priority = models.IntegerField(default=0)

    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title_ru)
        super(Category, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.title_ru}"

    class Meta: 
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ('priority',)


    @property
    def total_products(self):
        products = Product.objects.filter(drop=False, category=self).count()
        return products

    @property
    def total_subcategories(self): 
        subcategories = SubCategory.objects.filter(category=self).count()
        return subcategories




class SubCategory(models.Model): 
    img = ResizedImageField(size=[600,600], quality=100, upload_to="baymarket/categories/")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    priority = models.IntegerField()
    slug = models.CharField(max_length=255)

    
    def __str__(self) -> str:
        return f"{self.title_ru} ({self.category.title_ru})"

    
    @property
    def total_products(self):
        products = Product.objects.filter(drop=False, subcategory=self).count()
        return products


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title_ru)
        super(SubCategory, self).save(*args, **kwargs)


    class Meta: 
        verbose_name = "ПодКатегория"
        verbose_name_plural = "ПодКатегории"
        ordering = ('priority',)



class Product(models.Model): 
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True, related_name="baymarket_product_account")
    category  = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT, null=True, blank=True)
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    description_uz = models.TextField()
    description_ru = models.TextField(null=True, blank=True)
    slug = models.CharField(max_length=255, null=True, blank=True)
    priority = models.IntegerField()
    price = models.IntegerField()
    fix_price = models.IntegerField(default=0)
    available = models.BooleanField(default=True)
    drop = models.BooleanField(default=False)
    img_min = ResizedImageField(size=[300,300], quality=100, upload_to="web/products/300x300/")
    img_full = ResizedImageField(size=[600,600], quality=100, upload_to="web/products/600x600/")
    date_created = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    not_verified = models.BooleanField(default=False)
    not_verified_message = models.TextField(null=True, blank=True)
    moderation = models.BooleanField(default=True)  
    similar=  models.CharField(max_length=255, null=True, blank=True)
    

    def __str__(self):
        return f"{self.title_ru} ({self.category.title_ru}): {self.price} UZS"
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title_ru)
        super(Product, self).save(*args, **kwargs)


    class Meta: 
        verbose_name = "Наименование"
        verbose_name_plural = "Наименовании"
        ordering = ('priority',)



class ProductImage(models.Model): 
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="baymarket_product_productimage")
    img_min = ResizedImageField(size=[300,300], quality=100, upload_to="web/products/300x300/")
    img_full = ResizedImageField(size=[600,600], quality=100, upload_to="web/products/600x600/")


    def __str__(self):
        return f"Фото: {self.product.title_ru}"


    class Meta: 
        verbose_name = "Фото продукт"
        verbose_name_plural = "Фото продукты"

class Slider(models.Model):
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    content_uz = models.CharField(max_length=255)
    content_ru = models.CharField(max_length=255)
    description_uz = models.TextField()
    description_ru = models.TextField(null=True, blank=True)
    img_min = ResizedImageField(size=[300, 300], quality=100, upload_to=f"web/sliders/700x300/",  null=True, blank=True)
    img_full = ResizedImageField(size=[1200, 500], quality=100, upload_to=f"web/sliders/1200x500/", null=True, blank=True)
    priority = models.IntegerField()
    slug = models.CharField(max_length=255, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.title_ru}"

    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title_ru)
        super(Slider, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Слайд"
        verbose_name_plural = "Слайды"
        
class Blog(models.Model): 
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255, null=True, blank=True)
    description_uz = models.TextField()
    description_ru = models.TextField(null=True, blank=True)
    img_full = ResizedImageField(size=[600, 600], quality=100, upload_to="blogs/", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"{self.title_ru}"

    class Meta:
        verbose_name = "Блог"
        verbose_name_plural = "Блог"


class Room(models.Model):
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="baymarket_room_sender")
    reader = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="baymarket_room_reader")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_create = models.DateTimeField(auto_now_add=True)


class Message(models.Model): 
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="baymarket_message_sender")
    message = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)


class Wishlist(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="baymarket_wishist_account")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="baymarket_wishlist_product")

    def __str__(self):
        return str(self.product.title_ru)