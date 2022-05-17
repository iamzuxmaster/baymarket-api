
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Room, Message
from django.http import JsonResponse
import json
import random
import string

from control.models import Account

def uuid():
    letters = string.hexdigits
    id = ''
    for letter in range(0,8):
        id += random.choice(letters)
    return id

def control_index(request):
    context = {}
    return render(request, "control/platforms.html/", context)


# chat test
def chat_html(request):
    return render(request, "control/chat_test.html", {})


def get_all_messages(request):
    data = json.loads(request.body)
    account_a = Account.objects.get(id=data["account_a"])
    account_b = Account.objects.get(id=data["account_b"])
    try:
        try:         
            room = Room.objects.get(account_a=account_a, account_b=account_b)
        except:
            room= Room.objects.get(account_a=account_b, account_b=account_a)
    except:
            room= Room.objects.create(account_a=account_a, account_b=account_b) 
            room.uuid = uuid()
            room.save()

    messages = room.messages()
    answer = {
        "room": room.uuid,
        "messages": list(map(lambda message: {"id": message.id, "account":{"id": message.sender.id}, "message": message.message, "date": message.date_created}, messages)) if messages else None
    }
    return JsonResponse(answer, safe=False)


@csrf_exempt
def send_message(request):
    data = json.loads(request.body)
    print(data["account_a"])
    account_a= Account.objects.get(id=data["account_a"])
    room = Room.objects.get(uuid=data["id"])

    message = Message.objects.create(room=room, sender=account_a, message=data["message"])
    answer = {
        "code": 200,
        "message": {"id": message.id, "account": {"id": message.sender.id}, "message": message.message, "date": message.date_created}
    }
    return JsonResponse(answer, safe=False)