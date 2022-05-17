from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI
from ninja import Schema
from baymarket import models as baymarket 
from bayhouse import models as bayhouse
from baycar import models as baycar
from baywork import models as baywork

from control.models import Account

def Category(platform):
    if platform == 'baymarket':
        Category = baymarket.Category
    elif platform == 'bayhouse':
        Category = bayhouse.Category
    elif platform == 'baycar':
        Category = baycar.Category
    elif platform == 'baywork':
        Category = baywork.Category

    else: 
        Category = bayhouse.Category
    return Category

def SubCategory(platform): 
    if platform == 'baymarket': 
        SubCategory = baymarket.SubCategory
    elif platform == 'bayhouse': 
        SubCategory = bayhouse.SubCategory
    elif platform == 'baycar':
        SubCategory = baycar.SubCategory
    elif platform == 'baywork':
        SubCategory = baywork.SubCategory
        
    else: 
        SubCategory = baymarket.SubCategory
    return SubCategory

def Slider(platform):
    if platform == 'baymarket': 
        Slider = baymarket.Slider
    elif platform == 'bayhouse': 
        Slider = bayhouse.Slider
    elif platform == 'baycar':
        Slider = baycar.Slider
    elif platform == 'baywork':
        Slider = baywork.Slider
    else: 
        Slider = baymarket.Slider
    
    return Slider

def Blog(platform):
    if platform == 'baymarket': 
        Blog = baymarket.Blog
    if platform == 'bayhouse': 
        Blog = bayhouse.Blog
    elif platform == 'baycar':
        Blog = baycar.Blog
    elif platform == 'baywork':
        Blog = baywork.Blog
        
    else: 
        Blog = baymarket.Blog
    
    return Blog


class ApiSecretToken(Schema):
    secret_key: str 

class AccountGet(Schema):
    token : str

class Platforms(Schema):
    title : str

class SubcategoryGet(Schema):
    category_id: int


api_secret_token = 'ASN0123456789'


def answer(account: Account, categories=None, subcategories=None, sliders=None, blogs=None):
    answer = {
        "code": 200
        ,
        "account": {
            "id": account.id, 
            "user":{
                "username": account.user.username,
                "fullname": account.user.first_name,
            },
            "verified": account.verified,
            "phone": account.phone,
            "block": {
                "status": account.block,
                "date_end_block": account.block_end
            },
            "legal": account.legal,
            "balance_id": account.balance_id,
            "date_create": account.date_created,
        }
        ,
        "categories": list(map(lambda category: {
            "id": category.id,
            "title_ru": category.title_ru,
            "title_uz": category.title_uz,
            "slug": category.slug,
            "total_products": category.total_products,
        }, categories)) if categories else None
        ,
        "subcategories": list(map(lambda subcategory: {
            "id": subcategory.id,
            "title_ru": subcategory.title_ru,
            "title_uz": subcategory.title_uz,
            "slug": subcategory.slug,
            "category": {
                "id": subcategory.category.id,
                "title_ru": subcategory.category.title_ru,
                "title_uz": subcategory.category.title_uz,
                "slug": subcategory.category.slug,
                "total_products": subcategory.category.total_products
            } if subcategory.category else None,
            "total_products": subcategory.total_products
        }, subcategories)) if subcategories else None
        ,
        "sliders": list(map(lambda slider: {
            "img": slider.img_full.url,
            "title_uz": slider.title_uz,
            "title_ru": slider.title_ru,
            "content_ru": slider.content_ru,
            "content_uz": slider.content_uz, 
            "description_ru": slider.description_ru,
            "description_uz": slider.description_uz,
        }, sliders)) if sliders else None
        ,
        "blogs": list(map(lambda blog: {
            "img": blog.img_full.url,
            "title_uz": blog.title_uz,
            "title_ru": blog.title_ru,
            "description_ru": blog.description_ru,
            "description_uz": blog.description_uz,
        }, blogs)) if blogs else None
        ,

    }
    return answer




def answer_404():
    answer = {
        "code": 404
    }
    return answer


api = NinjaAPI()
@api.post("get/info/")
def get_info(request:HttpRequest,  account:AccountGet, auth:ApiSecretToken):
    if auth.secret_key == api_secret_token: 
        account = Account.objects.get(id=account.token)
        return answer(account=account)
    else: 
        return answer_404()

@api.post("get/categories/")
def get_categories(request:HttpRequest,  account:AccountGet, auth:ApiSecretToken, platform: Platforms):
    if auth.secret_key == api_secret_token: 
        account = get_object_or_404(Account, mobile_token=account.token)
        categories = Category(platform=platform.title).objects.all()
        return answer(account=account, categories=categories)
    else: 
        return answer_404()


@api.post("get/subcategories/")
def get_subcategories(request:HttpRequest,  account:AccountGet, auth:ApiSecretToken, platform: Platforms, category: SubcategoryGet):
    if auth.secret_key == api_secret_token: 
        account = get_object_or_404(Account, mobile_token=account.token)
        subcategories = SubCategory(platform=platform.title).objects.filter(category_id=category.category_id)
        return answer(account=account, subcategories=subcategories)
    else: 
        return answer_404()


@api.post("get/sliders/")
def get_sliders(request:HttpRequest,  account:AccountGet, auth:ApiSecretToken, platform: Platforms):
    if auth.secret_key == api_secret_token: 
        account = get_object_or_404(Account, mobile_token=account.token)
        sliders = Slider(platform=platform.title).objects.all()
        return answer(account=account,  sliders=sliders)
    else: 
        return answer_404()


@api.post("get/blogs/")
def get_blogs(request:HttpRequest,  account:AccountGet, auth:ApiSecretToken, platform: Platforms):
    if auth.secret_key == api_secret_token: 
        account = get_object_or_404(Account, mobile_token=account.token)
        blogs = Blog(platform=platform.title).objects.all()
        return answer(account=account,  blogs=blogs)
    else: 
        return answer_404()