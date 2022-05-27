from django.shortcuts import render
from .models import *
import json
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
import requests

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Web ByCar Api
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
def answer(
    account:Account= None, categories:Category=None, subcategories:SubCategory=None, types:Type=None, products: Product=None, conditions:Condition=None, materials:Material=None
    ):

    answer = {
        "code": 200
    }

    if account:
        answer["account"] = {
            "id": account.id,
            "user": {
                "username": account.user.username,
                "first_name": account.user.first_name,
                "email": account.user.email
            },
            "phone": account.user.username
        }

    if categories:
        answer["categories"] = list(map(lambda category: { 
            "id": category.id,
            "title": category.title_ru,
            "img": category.img.url if category.img else None
        }, categories))

    if subcategories:
        answer["subcategories"] = list(map(lambda subcategory: {
            "id": subcategory.id,
            "title": subcategory.title_ru, 
            "img": subcategory.img.url if subcategory.img else None
        }, subcategories))

    if types:
        answer["types"] = list(map(lambda types: { 
            "id": types.id,
            "title": types.title,
        }, types))


    if conditions:
        answer["conditions"] = list(map(lambda condition: { 
            "id": condition.id,
            "title": condition.title,
        }, conditions))

    if materials:
        answer["materials"] = list(map(lambda material: { 
            "id": material.id,
            "title": material.title,
        }, materials))

    if products:
        answer["products"] = list(map(lambda product: {
            "category": {
                "id": product.category.id,
                "title": product.category.title_ru,
                "img": product.category.img.url if product.category.img else None
            } if product.category else None,
            "subcategory": {
                "id": product.subcategory.id, 
                "title": product.subcategory.title_ru,
                "img": product.subcategory.img.url if product.subcategory.img else None
            } if product.subcategory else None,
            "id": product.id,
            "title": product.title_ru, 
            'description': product.description_ru,
            'category_id': product.category_id,
            'subcategory_id': product.subcategory_id, 
            'region': product.region.title_ru,
            'district': product.district.title_ru,
            'type': product.type.title,
            'sum': product.sum,
            'dollar': product.dollar,
            'price': product.price,
            'fixprice': product.fix_price,
            'available': product.available,
            'verified': product.verified,
            'meterial': product.materials.title,
            "condition": product.condition.title,
            "arenda": product.arenda,
            "area": product.area,
            "rooms": product.rooms,
            "storeys": product.storeys,
            'drop': product.drop,
            'img_min': product.img_min.url,
            'img_full': product.img_full.url,
            'datecreate': product.date_created,
            "link": f"product/{product.slug}",
            "subcategorylink": f"subcategroy/product/{product.slug}"
        }, products ))

    return JsonResponse(answer, safe=False)


def bay_house_index_api(request:HttpRequest):

    if request.user.is_authenticated:
        account = request.user.account
    else:
        account = None

    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    conditions = Condition.objects.all()
    types = Type.objects.all()
    materials = Material.objects.all()
    products = Product.objects.filter(drop=False, available=True)

    return answer(account=account, categories=categories, subcategories=subcategories, types=types, conditions=conditions, materials=materials, products=products)

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Web By House base context
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
def base_context(request): 
    context = {
    }
    return context



# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Web By House Page
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
def web_byhouse_index(request):
    context= {
    }
    return render(request, "web/byhouse/index.html")


def web_byhouse_detail(request):
    context= {
        
    }
    return render(request, "web/byhouse/detail.html")
