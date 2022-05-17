import json
import string
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from baymarket import models as baymarket 
from bayhouse import models as bayhouse
from baycar import models as baycar
from baywork import models as baywork
from control.models import Account, AccountTemp, User
from django.views.decorators.csrf import csrf_exempt
import requests
import random

platforms = ["baymarket", "baycar", "bayhouse", "baywork"]

class Exc:

    def phone_number_invalid():
        answer = {
            "code": 403,
            "status": "error",
            "answer": 'phone_number_invalid'
        }
        return JsonResponse(answer, safe=False)

    def sms_code_invalid():
        answer = {
            "code": 403, 
            "status": "error",
            "answer": "sms_code_invalid"
        }
        return JsonResponse(answer, safe=False)

    def phone_number_not_verified():
        answer = {
            "code": 403, 
            "status": "error", 
            "answer": "phone_number_not_verified"
        }
        return JsonResponse(answer, safe=False)

    def account_username_invalid():
        answer = {
            "code": 403, 
            "status": "error",
            "answer": "account_already_exists"
        }
        return JsonResponse(answer, safe=False)

    def fullname_invalid():
        answer = {
            "code": 403,
            "status": "error", 
            "answer": "fullname_invalid"
        }
        return JsonResponse(answer, safe=False)

    def platform_invalid():
        answer = {
            "code": 403, 
            "status": "error",
            "answer": "platform_invalid" 
        }
        return JsonResponse(answer, safe=False)

    def password_invalid():
        answer = {
            "code": 403, 
            "status": "error",
            "answer": "password_invalid" 
        }
        return JsonResponse(answer, safe=False)

    def category_invalid():
        answer = {
            "code": 403, 
            "status": "error",
            "answer": "category_invalid" 
        }
        return JsonResponse(answer, safe=False)
        

    def answer_404():
        answer = {
            "code": 404
        }
        return JsonResponse(answer, safe=False)


class Suc:
    
    def sms_sended():
        answer = {
            "code": 200, 
            "status": "success", 
            "answer": "sms_sended"
        }
        return JsonResponse(answer, safe=False)


    def phone_verified():
        answer = {
            "code": 200, 
            "status": "success", 
            "answer": "phone_verified"
        }
        return JsonResponse(answer, safe=False)


    def answer(account: Account = None, categories=None, subcategories=None, sliders=None, blogs=None, products=None):
        answer = {
            "code": 200
            ,
            "status": "success",
            "answer": {}
        }
        if account:
            answer["answer"]["account"]=  {
                    "token": account.mobile_token, 
                    "user":{
                        "username": account.user.username,
                        "fullname": account.user.first_name,
                    },
                    "phone": account.phone,
                    "block": {
                        "status": account.block,
                        "date_end_block": account.block_end
                    },
                    "legal": account.legal,
                    "balance_id": account.balance_id,
                    "date_create": account.date_created,
                }
        if categories:
            answer["answer"]["categories"] = list(map(lambda category: {
                    "id": category.id,
                    "title_ru": category.title_ru,
                    "title_uz": category.title_uz,
                    "slug": category.slug,
                    "total_products": category.total_products,
                    "img": category.img.url
                }, categories))

        if subcategories:
            answer["answer"]["subcategories"]= list(map(lambda subcategory: {
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
                }, subcategories))

        if products:
            answer["answer"]["products"] = list(map(lambda product: {
                "id": product.id, 
                "title_ru": product.title_ru, 
                "title_uz": product.title_uz,
                "slug": product.slug, 
                "category": {
                    "id": product.category.id,
                    "title_ru": product.category.title_ru, 
                    "title_uz": product.category.title_uz,
                    "slug": product.category.slug,
                    "total_products": product.category.total_products
                } if product.category else None,
                "subcategory": {
                    "id": product.subcategory.id,
                    "title_ru": product.subcategory.title_ru, 
                    "title_uz": product.subcategory.title_uz,
                    "slug": product.subcategory.slug,
                    "total_products": product.subcategory.total_products
                } if product.subcategory else None
                ,
                "price": product.price,
            }, products))
            
            

        if sliders:
            answer["answer"]["sliders"] = list(map(lambda slider: {
                    "img": slider.img_full.url,
                    "title_uz": slider.title_uz,
                    "title_ru": slider.title_ru,
                    "content_ru": slider.content_ru,
                    "content_uz": slider.content_uz, 
                    "description_ru": slider.description_ru,
                    "description_uz": slider.description_uz,
                }, sliders))

        if blogs:
                answer["answer"]["blogs"] =  list(map(lambda blog: {
                    "img": blog.img_full.url,
                    "title_uz": blog.title_uz,
                    "title_ru": blog.title_ru,
                    "description_ru": blog.description_ru,
                    "description_uz": blog.description_uz,
                }, blogs))


        return  JsonResponse(answer, safe=False)




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
    
    print("SMS Sended for Mobile APP to number " + phone_number)


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
        
    else: return Exc.platform_invalid()

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
        return Exc.platform_invalid()
    
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
        return Exc.platform_invalid()
    
    return Blog


def Product(platform):
    if platform == 'baymarket': 
        Product = baymarket.Product
    if platform == 'bayhouse': 
        Product = bayhouse.Product
    elif platform == 'baycar':
        Product = baycar.Product
    elif platform == 'baywork':
        Product = baywork.Product
    else: 
        Product = baymarket.Product
    
    return Product

def Product_Filter(platform, answer, product):
    if platform == 'baymarket': 
        answer = {
            "similar": product.similar
        }
    return answer


api_secret_token = "1234"

# /set/account/
@csrf_exempt
def set_account(request:HttpRequest):
    data = json.loads(request.body)
    
    try:
        secret_key = str(data["secret_key"])
    except KeyError:
        return Exc.answer_404()

    try:
        phone_number = str(data["phone_number"])
    except KeyError:
        return Exc.phone_number_invalid() 

    if secret_key == api_secret_token: 
        if phone_number.startswith('998'):
            code = ''
            for i in range(0, 6): 
                code += random.choice(string.digits)
            account_temp, account_temp_created = AccountTemp.objects.get_or_create(phone=phone_number)
            account_temp.code=code
            account_temp.save()
            send_sms(phone_number, code)
            return Suc.sms_sended()

        else:
            return Exc.phone_number_invalid()

    else: 
        return Exc.answer_404()


# /set/number/
@csrf_exempt
def set_number(request:HttpRequest):
    data = json.loads(request.body)
    try:
        secret_key = str(data["secret_key"])
    except KeyError:
        return Exc.answer_404()

    try:
        phone_number = str(data["phone_number"])
    except KeyError:
        return Exc.phone_number_invalid() 

    try:
        code = str(data["code"])
    except KeyError:
        return Exc.sms_code_invalid()
        

    if secret_key == api_secret_token: 
        if phone_number.startswith('998'):
            try: 
                account_temp = AccountTemp.objects.get(phone=phone_number)
            except:
                return Exc.phone_number_invalid()

            if code == account_temp.code:
                account_temp.verified  = True
                account_temp.save()
                return Suc.phone_verified()

            else: 
                return Exc.sms_code_invalid()

        else:
            return Exc.phone_number_invalid()

    else: 
        return Exc.answer_404()


# create/account/
@csrf_exempt
def create_account(request):
    data = json.loads(request.body)

    try:
        secret_key = str(data["secret_key"])
    except KeyError:
        return Exc.answer_404()

    try:
        phone_number = str(data["phone_number"])
    except KeyError:
        return Exc.phone_number_invalid() 

    try:
        password  = str(data["password"])
    except KeyError:
        return Exc.password_invalid()

    try: 
        first_name = str(data["fullname"])
    except KeyError:
        return Exc.fullname_invalid()


    if secret_key == api_secret_token: 
        if phone_number.startswith('998'):

            try: 
                account_temp = AccountTemp.objects.get(phone=phone_number)
            except:
                return Exc.phone_number_not_verified()
            if account_temp.verified:
                try:
                    user = User.objects.create(username=phone_number, password=password)
                except:
                    return Exc.account_username_invalid()
                    
                user.first_name = first_name
                user.account.phone = phone_number
                return Suc.answer(account=user.account)
            else: 
                return Exc.phone_number_not_verified()

        else:
            return Exc.phone_number_invalid()

    else: 
        return Exc.answer_404()


# /get/info/
@csrf_exempt
def get_account(request:HttpRequest):
    data = json.loads(request.body)
    secret_key = str(data["secret_key"])
    token = str(data["token"])

    if secret_key == api_secret_token: 
        try:
            account = Account.objects.get(mobile_token=token)
        except:
            return Exc.answer_404()
        
        return  Suc.answer(account=account)
    else: 
        return Exc.answer_404()


# /get/categories/
@csrf_exempt
def get_categories(request:HttpRequest):
    data = json.loads(request.body)
    try: 
        platform = data["platform"]
    except KeyError:
        return Exc.platform_invalid()

    try:
        secret_key = str(data["secret_key"])
    except KeyError:
        return Exc.answer_404()

    if secret_key == api_secret_token: 
        if platform in platforms:
            categories = Category(platform=platform).objects.all()
            return  Suc.answer(categories=categories)
        else:
            return Exc.platform_invalid()
            g
    else: 
        return Exc.answer_404()

# /get/subcategories/
@csrf_exempt
def get_subcategories(request:HttpRequest):
    data = json.loads(request.body)
    try: 
        platform = data["platform"]
    except KeyError:
        return Exc.platform_invalid()

    try:
        secret_key = str(data["secret_key"])
    except KeyError:
        return Exc.answer_404()

    try:
        category_id = data["category_id"]
    except KeyError:
        return Exc.category_invalid()


    if secret_key == api_secret_token: 
        if platform in platforms:
            try:
                category = Category(platform=platform).objects.get(id=category_id)
            except:
                return Exc.category_invalid()
            products = Product(platform=platform).objects.all()
            subcategories = SubCategory(platform=platform).objects.filter(category=category)
            return  Suc.answer(subcategories=subcategories, products=products)
        else:
            return Exc.platform_invalid()

    else: 
        return Exc.answer_404()