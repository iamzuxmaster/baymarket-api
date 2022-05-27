from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.web_bymarket_index, name="web_bymarket_index"),
    path("bymarket/detail/", views.web_bymarket_detail, name="web_bymarket_detail"),
]