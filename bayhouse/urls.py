from django.urls import path, include
from . import views

urlpatterns = [
    # Api   #####################################################
    path('bayhouse/init/ru/', views.bay_house_index_api, name="init"),
    # Pages #####################################################
    path("", views.web_byhouse_index, name="web_byhouse_index"),

    path("byhouse/detail/", views.web_byhouse_detail, name="web_byhouse_detail"),
]