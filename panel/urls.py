from django.urls import path
from . import views

urlpatterns  = [
    path("", views.control_panel_index, name="control_panel_index"),
    path("categories/", views.control_panel_categories_all, name="control_panel_categories_all"),
    path("category/add/", views.control_panel_categories_add, name="control_panel_categories_add"),
    path("category/edit/", views.control_panel_categories_edit, name="control_panel_categories_edit"),
        path("category/create/", views.control_panel_categories_create, name="control_panel_categories_create"),
        path("category/delete/", views.control_panel_categories_delete, name="control_panel_categories_create"),
        path("category/<str:slug>/", views.control_panel_categories_detail, name="control_panel_categories_create"),

    # SubCategories 
    path("subcategories/",views.control_panel_subcategories_all, name="control_subcategories_all"),
    path("subcategory/add/",views.control_panel_subcategories_add, name="control_subcategory_add"),
        path("subcategory/create/",views.control_panel_subcategories_create, name="control_subcategory_create"),
        path("subcategory/edit/",views.control_panel_subcategories_edit, name="control_subcategory_edit"),
        path("subcategory/delete/",views.control_panel_subcategories_delete, name="control_subcategory_delete"),
    path("subcategory/<str:slug>/",views.control_panel_subcategories_detail, name="control_subcategory_detail"),

    # Sliders
    path("sliders/", views.control_panel_sliders_all, name="control_sliders_all"),
    path("slider/add/", views.control_panel_sliders_add, name="control_sliders_add"),
        path("slider/create/", views.control_panel_sliders_create, name="control_sliders_create"), 
        path("slider/edit/", views.control_panel_sliders_edit, name="control_sliders_edit"),
        path("slider/delete/", views.control_panel_sliders_delete, name="control_sliders_delete"),
    path("slider/<slug:slug>/", views.control_panel_sliders_detail, name="control_sliders_detail"),

    # News
    path("blogs/", views.control_panel_blog_all, name="control_blogs_all"),
    path("blog/add/", views.control_panel_blog_add, name="control_blog_add"),
        path("blog/create/", views.control_panel_blog_create, name="control_blog_create"), 
        path("blog/edit/", views.control_panel_blog_edit, name="control_blog_edit"),
        path("blog/delete/", views.control_panel_blog_delete, name="control_blog_delete"),
    path("blog/<int:id>/", views.control_panel_blog_detail, name="control_blog_detail"),
]    