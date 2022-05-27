from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.web_bywork_index, name="web_bywork_index"),
    path("bywork/detail/", views.web_bywork_detail, name="web_bywork_detail"),
]