from django.urls import path
from . import views

urlpatterns = [
    path('get/account/', views.get_account),
    path('set/account/', views.set_account),
    path('set/number/', views.set_number),
    path('create/account/', views.create_account),
        path('get/categories/', views.get_categories),
        path('get/subcategories/', views.get_subcategories),
]