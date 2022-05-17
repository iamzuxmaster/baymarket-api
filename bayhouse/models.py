from django.db import models
from slugify import slugify
from django_resized import ResizedImageField
from control.models import *
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


class Material(models.Model): 
    title = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return f"Материал дома: {self.title}"

    class Meta:
        verbose_name =  "Материал"
        verbose_name_plural = "Материалы"
        
    @property
    def total_products(self): 
        count = Product.objects.filter(material = self, drop = False, verified = True).count()
        return count


class Type(models.Model): 
    title = models.CharField(max_length=255, null=True, blank=True)
    slug = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Тип дома: {self.title}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title).lower() + random_id()
        super(Type, self).save(*args, **kwargs)

    class Meta:
        verbose_name =  "Тип дома BayHouse"
        verbose_name_plural = "Типы домы BayHouse"

    @property
    def total_products(self):
        pro = Product.objects.filter(drop = False, verified = True, type = self).count()
        return pro


class Condition(models.Model): 
    title = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return f"Состаяние: {self.title}"

    class Meta:
        verbose_name =  "Состаяние"
        verbose_name_plural = "Состаянии"

    @property
    def total_products(self): 
        count = Product.objects.filter(condition = self, drop = False, verified = True).count()
        return count


class Product(models.Model): 
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True, related_name="bayhouse_product_account")
    category  = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT, null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True, related_name='bayhouse_product_region')
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True, related_name='bayhouse_product_disctrict')
    materials = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True, blank=True)
    condition = models.ForeignKey(Condition, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True, blank=True)
    area = models.IntegerField(null=True, blank=True)
    rooms = models.IntegerField(null=True, blank=True)
    storeys = models.IntegerField(null=True, blank=True)
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    description_uz = models.TextField()
    description_ru = models.TextField(null=True, blank=True)
    slug = models.CharField(max_length=255, null=True, blank=True)
    priority = models.IntegerField()
    price = models.IntegerField()
    fix_price = models.IntegerField(null=True, blank=True)
    available = models.BooleanField(default=True)
    drop = models.BooleanField(default=False)
    img_min = ResizedImageField(size=[300,300], quality=100, upload_to="web/products/300x300/")
    img_full = ResizedImageField(size=[600,600], quality=100, upload_to="web/products/600x600/")
    date_created = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)    


    def __str__(self):
        return f"{self.title_ru} ({self.category.title_ru}): {self.price} UZS"
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title_ru)
        super(Product, self).save(*args, **kwargs)


    class Meta: 
        verbose_name = "Наименование"
        verbose_name_plural = "Наименовании"
        ordering = ('priority',)


class HouseConven(models.Model): 
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    telephone = models.BooleanField(default=False)
    aircondition = models.BooleanField(default=False)
    internet = models.BooleanField(default=False)
    sewer = models.BooleanField(default=False)
    water = models.BooleanField(default=False)
    furniture = models.BooleanField(default=False)
    lift = models.BooleanField(default=False)
    washing = models.BooleanField(default=False)
    camera = models.BooleanField(default=False)
    tv = models.BooleanField(default=False)
    park = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Удобства дома: {self.product.title_uz}"

    class Meta:
        verbose_name =  "Удобства"
        verbose_name_plural = "Удобствы"


class ProductImage(models.Model): 
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    img_min = ResizedImageField(size=[300,300], quality=100, upload_to="web/products/300x300/")
    img_full = ResizedImageField(size=[600,600], quality=100, upload_to="web/products/600x600/")


    def __str__(self):
        return f"Фото: {self.product.title}"


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
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="bayhouse_room_sender")
    reader = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="bayhouse_room_reader")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_create = models.DateTimeField(auto_now_add=True)


class Message(models.Model): 
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="bayhouse_message_sender")
    message = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)


class Wishlist(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="bayhouse_wishlist_account")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="bayhouse_wishlist_product")

    def __str__(self):
        return str(self.product.title_ru)