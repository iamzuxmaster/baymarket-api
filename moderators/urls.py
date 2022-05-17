from django.urls import path
from . import views
urlpatterns = [
    path("", views.moderator_index,name="moderators_index"),
    path("product_detail/", views.product_detail),
    path("product_check/", views.product_check),
    path("product_block/", views.product_block),
] 