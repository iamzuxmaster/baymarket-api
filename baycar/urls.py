from django.urls import path, include
from . import views

urlpatterns = [

    # Web Page
    path("", views.web_index, name="web_index"),
    path("baycar/announcement", views.web_announcement, name="web_announcement"),
 
    path("baycar/send/message/", views.send_message, name="send_message"),
    path("baycar/phone/verify/", views.phone_verify, name="phone_verify"),

    path("baycar/verify/", views.verify),
    path("baycar/login/", views.log),
 
    # Api #############################################################
    path('init/ru/', views.index_api, name="init"),

    # Fetch ###########################################################
    path("baycar/category/detail/", views.web_baycar_category_api, name="web_bycar_category_detail"),
    path("baycar/subcategory/detail/", views.web_baycar_subcategory_api, name="web_bycar_subcategory_detail"),
    
    
    # Page #############################################################
    path("baycar/", views.web_baycar_index, name="web_bycar_index"),
    path("baycar/<str:slug>", views.web_baycar_category, name="web_baycar_category"),
    path("baycar/subcategory/<str:slug>", views.web_baycar_subcategory, name="web_baycar_subcategory"),
    path("baycar/product/<str:slug>", views.web_baycar_detail, name="web_bycar_detail"),
    path("baycar/subcategory/product/<str:slug>", views.web_baycar_detail1, name="web_bycar_detail1"),
    path("baycar/filter/", views.web_baycar_filter, name="web_baycar_filter"),

]