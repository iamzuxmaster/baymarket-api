from django.shortcuts import render
from baycar import models as baycar
from baymarket import models as baymarket
from baywork import models as baywork
from bayhouse import models as bayhouse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
import socketio

async_mode = None
sio = socketio.Server(async_mode=async_mode)
thread = None


@sio.event
def my_connect(sid, message):
    print(message["data"])

@sio.event
def edited(sid, message):
    sio.emit("edit", {"id": message["data"]})


def moderator_index(request):
    products = baymarket.Product.objects.filter(drop=False)
    context = {
        "products":products
    }
    return render(request, "control/moderators/index.html", context)


@csrf_exempt
def product_detail(request):
    
    datas = json.loads(request.body)
    print(datas)
    id = datas['product_id']
    product = baymarket.Product.objects.get(id=id)
    data = {
        'status':200,
        'product': {
            "id": product.id,
            "img": product.img_full.url,
            "title": product.title_uz,
            "price":product.price,
            "date_create": product.date_created,
            "verified": product.verified,
            "not_verified": product.not_verified,
            "description": product.description_ru,
            "category": {
                "title": product.category.title_ru
            },
            "account": {
                "phone": product.account.phone
            }
            },
        'product_images':[ product_img.img_full.url for product_img in product.baymarket_product_productimage.all()]
    }
    

    return JsonResponse(data, safe=False)


@csrf_exempt
def product_check(request):

    data = json.loads(request.body)
    print(data)
    id = data['product_id']
    product = baymarket.Product.objects.get(id=id)
    product.moderator = request.user.account
    product.title_ru = data["new_title"]
    product.description_ru = data["new_description"]
    product.verified =True
    product.save()
    answer = {
        "code": 200
    }
    return JsonResponse(answer, safe=False)


@csrf_exempt
def product_block(request):
    data = json.loads(request.body)
    id = data['product_id']
    product = baymarket.Product.objects.get(id=id)
    product.moderator = request.user.account
    product.verified =False
    product.not_verified = True
    product.not_verified_message = data["message"]
    product.save()
    answer = {
        "code": 200
    }
    return JsonResponse(answer, safe=False)