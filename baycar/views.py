from django.shortcuts import render
from .models import *
import json
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate
import requests

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Web ByCar Api
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
def answer(
    account:Account= None, categories:Category=None, subcategories:SubCategory=None, regions:Region=None, products: Product=None, category:Category=None, subcategory:SubCategory=None
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
    
    if category:
        answer["category"] = {
            "id": category.id, 
            "title": category.title_ru,
        }

    if subcategory:
        answer["subcategory"] = {
            "id": subcategory.id, 
            "title": subcategory.title_ru,
        }
    
    if regions:
        answer["regions"] = list(map(lambda region: { 
            "id": region.id,
            "title": region.title_ru,
        }, regions))


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
            'marka': product.marka,
            'region': product.region.title_ru,
            'district': product.district.title_ru,
            'type': product.type.title,
            'transmission': product.transmission.title,
            'color': product.color.title,
            'price': product.price,
            'fixprice': product.fix_price,
            'available': product.available,
            'verified': product.verified,
            'notverified': product.not_verified,
            'year': product.year,
            'km': product.km,
            'arenda': product.arenda,
            'oil': product.oil,
            'gass': product.gass,
            'dizel': product.dizel,
            'electr': product.electr,
            'dollar': product.dollar,
            'sum': product.sum,
            'arr': product.arr,
            'driveunit': product.drive_unit,
            'drop': product.drop,
            'img_min': product.img_min.url,
            'img_full': product.img_full.url,
            'datecreate': product.date_created,
            "link": f"product/{product.slug}",
            "subcategorylink": f"subcategroy/product/{product.slug}"
        }, products ))

    return JsonResponse(answer, safe=False)


def index_api(request:HttpRequest):

    if request.user.is_authenticated:
        account = request.user.account
    else:
        account = None

    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    regions = Region.objects.all()
    products = Product.objects.filter(drop=False, available=True)

    return answer(account=account, categories=categories, subcategories=subcategories, regions=regions, products=products)

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Web Bycar base context
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
def base_context(request): 
    context = {
    }
    return context


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Web Index Page
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
def web_index(request):
    context= {
    }
    return render(request, "web/web/index.html")


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Web Announcement Page
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
def web_announcement(request):
    context= {
    }
    return render(request, "web/web/announcement.html")


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Web ByCar Page
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
def web_baycar_index(request):
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    context= {
        "categories": categories,
        "subcategories": subcategories
    }
    return render(request, "web/baycar/index.html", context)


# Bay Car Category Page ###################################################
###########################################################################
def web_baycar_category(request, slug):
    category = Category.objects.get(slug=slug)
    subcategories = SubCategory.objects.filter(category=category)
    products = Product.objects.filter(category = category, drop=False, available=True)
    context = {
        "products": products,
        "category": category,
        "subcategories": subcategories,
    }
    return render(request, "web/baycar/category.html", context)

def web_baycar_category_api(request:HttpRequest): 
    data = json.loads(request.body)
    slug = data["slug"]
    category = Category.objects.get(slug=slug)
    products = Product.objects.filter(drop=False, available=True, category=category)

    return answer(category=category, products=products)


# Bay Car SubCategory Page ################################################
###########################################################################
def web_baycar_subcategory(request, slug):
    subcategory = SubCategory.objects.get(slug=slug)
    products = Product.objects.filter(subcategory = subcategory, drop=False, available=True)
    context = {
        "products": products,
        "subcategory": subcategory,
    }
    return render(request, "web/baycar/subcategory.html", context)

def web_baycar_subcategory_api(request:HttpRequest): 
    data = json.loads(request.body)
    slug = data["slug"]
    subcategory = SubCategory.objects.get(slug=slug)
    products = Product.objects.filter(drop=False, available=True, subcategory=subcategory)

    return answer(subcategory=subcategory, products=products)



# Bay Car Detail Page #####################################################
###########################################################################
def web_baycar_detail(request, slug):
    product = Product.objects.get(slug=slug)
    product_image = ProductImage.objects.filter(product = product)
    context= {
        "product": product,
        "product_image": product_image
    }
    return render(request, "web/baycar/detail.html", context)

def web_baycar_detail1(request, slug):
    product = Product.objects.get(slug=slug)
    product_image = ProductImage.objects.filter(product = product)
    context= {
        "product": product,
        "product_image": product_image
    }
    return render(request, "web/baycar/detail.html", context)


def send_sms(phone_number, code):
    url = "https://notify.eskiz.uz/api/message/sms/send"
    text = f'BayMarket do\'koniga kirish uchun tasdiqlash kodingiz: {code}'

    payload={
        'mobile_phone': f'{phone_number}',
        'message': text,
        'from': '4546',
    }

    headers = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjc5Nywicm9sZSI6InVzZXIiLCJkYXRhIjp7ImlkIjo3OTcsIm5hbWUiOiJcdTA0MWVcdTA0MWVcdTA0MWUgXCJHZXREQlNcIiIsImVtYWlsIjoia2guc3BiQE1haWwucnUiLCJyb2xlIjoidXNlciIsImFwaV90b2tlbiI6bnVsbCwic3RhdHVzIjoiYWN0aXZlIiwic21zX2FwaV9sb2dpbiI6ImVza2l6MiIsInNtc19hcGlfcGFzc3dvcmQiOiJlJCRrIXoiLCJ1el9wcmljZSI6NTAsImJhbGFuY2UiOjI5OTkwMCwiaXNfdmlwIjowLCJob3N0Ijoic2VydmVyMSIsImNyZWF0ZWRfYXQiOiIyMDIyLTAzLTMxVDA1OjM4OjU4LjAwMDAwMFoiLCJ1cGRhdGVkX2F0IjoiMjAyMi0wNC0wMVQxOToyNToxMC4wMDAwMDBaIn0sImlhdCI6MTY1MjA3ODExMSwiZXhwIjoxNjU0NjcwMTExfQ._6Kn1A371qmkoXTlP1hszpnvGxDMzrLe1JoHKY5F_Tc'
    }

    response = requests.post(url, headers=headers, data=payload)
    print(response.text)
    print("SMS Sended for Mobile APP to number " + phone_number)


def send_message(request):
    data = json.loads(request.body)
    phone_number = data["phone_number"]
    code = ''
    for i in range(0, 6): 
        code += random.choice(string.digits)
    account_temp, account_temp_created = AccountTemp.objects.get_or_create(phone=phone_number)
    account_temp.code=code
    account_temp.save()
    send_sms(phone_number=phone_number, code=code)
    return JsonResponse({"code": 200}, safe=False)


def phone_verify(request: HttpRequest):
    data = json.loads(request.body)
    phone = data["phone"]

    try:
        account = User.objects.get(username=phone)
    except: 
        answer = {
            "code": 200
        }
        return JsonResponse(answer, safe=False)
    answer = {
        "code": 403
    }

    return JsonResponse(answer, safe=False)

def verify(request: HttpRequest):
    data = json.loads(request.body)
    phone = data["phone_number"]
    password = data["sms_password"]
    try: 
        account_temp  = AccountTemp.objects.get(phone=phone)
    except: 
        answer = {
            "code": 403
        }        
        return JsonResponse(answer, safe=False)

    if account_temp.code == password: 
        answer  = {
            "code": 200
        }
        return JsonResponse(answer, safe=False)

    else:
        answer = {
            "code": 403
        }
        return JsonResponse(answer, safe=False)

def log(request:HttpRequest):
    data = json.loads(request.body)
    phone = data["phone_number"]
    password = data["password"]

    try:
        account = Account.objects.get(phone=phone)
    except:
        answer = {
            "code": 403
        }
        return JsonResponse(answer, safe=False)

    if authenticate(username=account.user.username, password=password):
        login(request, account.user)
        answer = {
            "code": 200
        } 
        return JsonResponse(answer, safe=False)

    else:
        answer = {
            "code": 403
        }
        return JsonResponse(answer, safe=False)

def web_baycar_filter(request:HttpRequest):
    data = json.loads(request.body)
    