from django.urls import path, include
from . import views

urlpatterns = [

    path("get/messages/", views.get_all_messages),
    path("send/message/", views.send_message),
    path("<str:platform>/", include("panel.urls")),
    path("moderators/", include("moderators.urls")),
    path("", views.control_index, name="control_index"),
]  