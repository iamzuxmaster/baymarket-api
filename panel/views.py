from platform import platform
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import TemplateDoesNotExist
from baymarket import models as baymarket 
from bayhouse import models as bayhouse
from baycar import models as baycar
from baywork import models as baywork
from control.models import Account

SECURE_PATH_ADMIN = '/control/'

def Category(platform):
    if platform == 'baymarket':
        Category = baymarket.Category
    elif platform == 'bayhouse':
        Category = bayhouse.Category
    elif platform == 'baycar':
        Category = baycar.Category
    elif platform == 'baywork':
        Category = baywork.Category

    else: 
        Category = bayhouse.Category
    return Category


def SubCategory(platform): 
    if platform == 'baymarket': 
        SubCategory = baymarket.SubCategory
    elif platform == 'bayhouse': 
        SubCategory = bayhouse.SubCategory
    elif platform == 'baycar':
        SubCategory = baycar.SubCategory
    elif platform == 'baywork':
        SubCategory = baywork.SubCategory
        
    else: 
        SubCategory = baymarket.SubCategory
    return SubCategory

def Slider(platform):
    if platform == 'baymarket': 
        Slider = baymarket.Slider
    elif platform == 'bayhouse': 
        Slider = bayhouse.Slider
    elif platform == 'baycar':
        Slider = baycar.Slider
    elif platform == 'baywork':
        Slider = baywork.Slider
    else: 
        Slider = baymarket.Slider
    
    return Slider

def Blog(platform):
    if platform == 'baymarket': 
        Blog = baymarket.Blog
    if platform == 'bayhouse': 
        Blog = bayhouse.Blog
    elif platform == 'baycar':
        Blog = baycar.Blog
    elif platform == 'baywork':
        Blog = baywork.Blog
        
    else: 
        Blog = baymarket.Blog
    
    return Blog

def Product(platform):
    if platform == 'baymarket': 
        Product = baymarket.Product
    if platform == 'bayhouse': 
        Product = bayhouse.Product
    elif platform == 'baycar':
        Product = baycar.Product
    elif platform == 'baywork':
        Product = baywork.Product
    else: 
        Product = baymarket.Product
    
    return Product



def base_context(request): 
    platform = request.build_absolute_uri().split("/control/")[1].split("/")[0]
    try: 
        code = request.build_absolute_uri().split('?')[1]
    except: 
        code = None
    accounts = Account.objects.all()
    CHAT_SERVER = request.build_absolute_uri().split("://")[1].split("/")[0].split(":")[0]
    context = {
        "platform": platform,
        "accounts": accounts,
        "code": code,
        "chat_server": CHAT_SERVER
    }
    return context


def control_panel_index(request, platform):
    categories = Category(platform=platform).objects.all()
    sliders = Slider(platform=platform).objects.all()
    products = Product(platform=platform).objects.all()
    
    context= {
        "base": base_context(request),
        "products": products,
        "sliders": sliders,
        "categories": categories
    }

    try:
        return render(request, f"control/{platform}/index.html", context)

    except TemplateDoesNotExist:
        answer = {
            "code": 404
        }
        return JsonResponse(answer, safe=False)

def control_panel_categories_all(request, platform):
    
    categories = Category(platform=platform).objects.all()


    context= {
        "base": base_context(request),
        "categories": categories
    }

    try:
        return render(request, f"control/{platform}/categories/all.html", context)

    except TemplateDoesNotExist:
        answer = {
            "code": 404
        }
        return JsonResponse(answer, safe=False)

def control_panel_categories_add(request, platform):
    context= {
        "base": base_context(request)
    }

    try:
        return render(request, f"control/{platform}/categories/add.html", context)

    except TemplateDoesNotExist:
        answer = {
            "code": 404
        }
        return JsonResponse(answer, safe=False)

def control_panel_categories_detail(request, platform, slug):
    category = get_object_or_404(Category(platform=platform), slug=slug)


    context= {
        "base": base_context(request),
        "category": category
    }

    try:
        return render(request, f"control/{platform}/categories/detail.html", context)

    except TemplateDoesNotExist:
        answer = {
            "code": 404
        }
        return JsonResponse(answer, safe=False)

def control_panel_categories_create(request, platform):
    if request.method == 'POST' and request.FILES["file"]: 
        title_ru = request.POST["title_ru"]
        title_uz = request.POST["title_uz"]
        priority = request.POST["priority"]
        img = request.FILES["file"]
        if title_ru.lower().strip() in list(map(lambda category: category.title_ru.lower().strip(), Category(platform).objects.all())):
            return redirect(SECURE_PATH_ADMIN+f"{platform}/category/add/?error")
        else:
            category = Category(platform).objects.create(title_uz=title_uz, title_ru=title_ru, priority=priority, img=img)
            category.save()
            return redirect(SECURE_PATH_ADMIN+f"{platform}/categories/?created")
    else: 
        answer = {
            "code": 404,
            "error": "Page Not Found"
        }
        return JsonResponse(answer, safe=False)


def control_panel_categories_edit(request, platform):
    if request.method == 'POST' or request.FILES["file"]: 
        category = get_object_or_404(Category(platform=platform), slug=request.POST["category_slug"])
        category.priority = request.POST["priority"]
        category.title_uz = request.POST["title_uz"]
        title_ru = request.POST["title_ru"]
        try:
            category.img = request.FILES["file"]
        except:
            pass

        if title_ru.lower().strip() == category.title_ru.lower().strip():
            category.save()
            return redirect(SECURE_PATH_ADMIN + f"{platform}/category/{category.slug}/?edited")

        elif title_ru.lower().strip() in list(map(lambda category: category.title_ru.lower().strip(), Category(platform=platform).objects.all())):
            category.save()
            return redirect(SECURE_PATH_ADMIN + f"{platform}/category/{category.slug}/?title_error")
        else:
            category.title_ru = title_ru
            category.save()
            print(category.slug)
            return redirect(SECURE_PATH_ADMIN + f"{platform}/category/{category.slug}/?edited")
        
    else: 
        answer = {
            "code": 404,
            "error": "Page Not Found"
        }
        return JsonResponse(answer, safe=False)

def control_panel_categories_delete(request, platform):
    if request.method == "POST": 
        print(request.POST["category_slug"])
        category = get_object_or_404(Category(platform=platform), slug=request.POST["category_slug"])
        category.delete()
        return redirect(SECURE_PATH_ADMIN + f"{platform}/categories/?deleted")
    else: 
        answer = {
            "code": 404,
            "error": "Page Not Found"
        }
        return JsonResponse(answer, safe=False)



# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# Subcategory

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

def control_panel_subcategories_all(request, platform):
    subcategories = SubCategory(platform=platform).objects.all()
    context = {
        "base": base_context(request=request),
        "subcategories":subcategories
    }
    try:
        return render(request, f"control/{platform}/subcategories/all.html", context)
    except TemplateDoesNotExist:
        answer = {
            "code": 404
        }
        return JsonResponse(answer, safe=False)


def control_panel_subcategories_add(request, platform):
    categories = Category(platform=platform).objects.all()
    context = {
        "base": base_context(request=request),
        "categories":categories
    }
    try:
        return render(request, f"control/{platform}/subcategories/add.html", context)
    except TemplateDoesNotExist:
        answer = {
            "code": 404
        }
        return JsonResponse(answer, safe=False)



# def control_panel_subcategories_category_add(request):
#     data = json.loads(request.body)
#     title_ru,  title_uz , priority = data["title_ru"],  data["title_uz"], data["priority"]

#     if title_ru.lower().strip() in list(map(lambda category: category.title_ru.lower().strip(), Category.objects.all())):
#         answer ={
#             "code": 403,
#             "error": "Есть категория с таким названием.!"
#         }
#         return JsonResponse(answer, safe=False)
#     else:
#         category = Category.objects.create(title_ru=title_ru, title_uz=title_uz, priority=priority)
#         category.save()

#     answer ={
#         "code": 200,
#         "category": {"id": category.id, "title_ru": category.title_ru}
#     }


#     return JsonResponse(answer, safe=False)


def control_panel_subcategories_create(request, platform):    
    if request.method == "POST": 
        title_ru, title_uz, priority = request.POST["title_ru"], request.POST["title_uz"], request.POST["priority"]
        category = get_object_or_404(Category(platform=platform), id=request.POST["category_id"])

        if title_ru.lower().strip() in list(map(lambda subcategory: subcategory.title_ru.lower().strip(), SubCategory(platform=platform).objects.all())):
            return redirect(SECURE_PATH_ADMIN+f"{platform}/subcategory/add/?error")
        else:
            subcategory = SubCategory(platform=platform).objects.create(category=category,title_uz=title_uz, title_ru=title_ru, priority=priority)
            subcategory.save()
            return redirect(SECURE_PATH_ADMIN+f"{platform}/subcategories/?created")

    else: 
        answer = {
            "code": 404,
            "error": "Page Not Found"
        }
        return JsonResponse(answer, safe=False)


def control_panel_subcategories_detail(request,platform, slug):
    categories = Category(platform=platform).objects.all()
    subcategory = get_object_or_404(SubCategory(platform=platform), slug=slug)
    context = {
        "base": base_context(request=request),
        "categories": categories, 
        "subcategory": subcategory
    }
    try:
        return render(request, f"control/{platform}/subcategories/detail.html", context)
    except TemplateDoesNotExist:
        answer = {
            "code": 404
        }
        return JsonResponse(answer, safe=False)



def control_panel_subcategories_edit(request, platform):
    if request.method == "POST":
        category = get_object_or_404(Category(platform=platform), id=request.POST["category_id"])
        subcategory = get_object_or_404(SubCategory(platform=platform), slug=request.POST["subcategory_slug"])
        title_ru, title_uz, priority = request.POST["title_ru"], request.POST["title_uz"], request.POST["priority"]
        subcategory.title_uz = title_uz
        subcategory.priority = priority
        subcategory.category = category

        if title_ru.lower().strip() == subcategory.title_ru.lower().strip():
            subcategory.save()
            return redirect(SECURE_PATH_ADMIN + f"{platform}/subcategory/{subcategory.slug}/?edited")
        elif title_ru.lower().strip() in list(map(lambda subcategory: subcategory.title_ru.lower().strip(), SubCategory(platform=platform).objects.all())):
            subcategory.save()
            return redirect(SECURE_PATH_ADMIN + f"{platform}/subcategory/{subcategory.slug}/?title_error")
        else:
            subcategory.title_ru = title_ru
            subcategory.save()
            return redirect(SECURE_PATH_ADMIN + f"{platform}/subcategory/{subcategory.slug}/?edited")
        
    else: 
        answer = {
            "code": 404,
            "error": "Page Not Found"
        }
        return JsonResponse(answer, safe=False)


def control_panel_subcategories_delete(request, platform):
    if request.method == "POST": 
        category = get_object_or_404(SubCategory(platform=platform), slug=request.POST["subcategory_slug"])
        category.delete()
        return redirect(SECURE_PATH_ADMIN + f"{platform}/subcategories/?deleted")
    else: 
        answer = {
            "code": 404,
            "error": "Page Not Found"
        }
        return JsonResponse(answer, safe=False)



# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# Sliders

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$



def control_panel_sliders_all(request, platform):
    sliders = Slider(platform=platform).objects.all()
    context = {
        "base": base_context(request=request),
        "sliders": sliders
    }
    try:
        return render(request, f"control/{platform}/sliders/all.html", context)
    except TemplateDoesNotExist:
        answer = {
            "code": 404
        }
        return JsonResponse(answer, safe=False)



def control_panel_sliders_add(request, platform):
    context = {
        "base": base_context(request=request)
    }
    try:
        return render(request, f"control/{platform}/sliders/add.html", context)
    except TemplateDoesNotExist:
        answer = {
            "code": 404
        }
        return JsonResponse(answer, safe=False)



def control_panel_sliders_create(request, platform):
    if request.method == "POST" and request.FILES["file"]: 
        title_ru = request.POST["title_ru"]
        title_uz = request.POST["title_uz"]
        content_uz = request.POST["content_uz"]
        content_ru = request.POST["content_ru"]
        description_ru = request.POST["description_ru"]
        desctiption_uz = request.POST["description_uz"]
        priority = request.POST["priority"]
        if title_ru.lower().strip() in list(map(lambda slider: slider.title_ru.lower().strip(), Slider(platform=platform).objects.all())):
            return redirect(SECURE_PATH_ADMIN+"slider/add/?error")
        else:
            slider = Slider(platform=platform).objects.create(
                title_uz=title_uz,
                title_ru=title_ru,
                priority=priority,
                img_min = request.FILES["file"],
                img_full = request.FILES["file"],
                description_ru = description_ru,
                description_uz = desctiption_uz
                )
            
            slider.content_ru=content_ru
            slider.content_uz=content_uz
            slider.save()
            return redirect(SECURE_PATH_ADMIN+f"{platform}/sliders/?created")
    else: 
        answer = {
            "code": 404,
            "error": "Page Not Found"
        }
        return JsonResponse(answer, safe=False)


def control_panel_sliders_detail(request, slug, platform):
    slider = get_object_or_404(Slider(platform=platform), slug=slug)
    context = {
        "base": base_context(request=request),
        "slider":slider
    }
    try:
        return render(request, f"control/{platform}/sliders/detail.html", context)
    except TemplateDoesNotExist:
        answer = {
            "code": 404
        }
        return JsonResponse(answer, safe=False)



def control_panel_sliders_edit(request, platform):
    if request.method == "POST" or request.FILES["file"]:
        content_uz = request.POST["content_uz"]
        content_ru = request.POST["content_ru"]
        description_ru = request.POST["description_ru"]
        description_uz = request.POST["description_uz"]
        slider = get_object_or_404(Slider(platform=platform), slug=request.POST["slider_slug"])
        title_ru, title_uz, priority = request.POST["title_ru"], request.POST["title_uz"], request.POST["priority"]
        slider.title_uz = title_uz
        slider.content_ru = content_ru
        slider.content_uz = content_uz
        slider.description_ru = description_ru
        slider.description_uz = description_uz
        slider.priority = priority
        try: 
            slider.img_full = request.FILES["file"]
            slider.img_min = request.FILES["file"]
        except:
            pass

        
        if title_ru.lower().strip() == slider.title_ru.lower().strip():
            slider.save()
            return redirect(SECURE_PATH_ADMIN + f"{platform}/slider/{slider.slug}/?edited")
        elif title_ru.lower().strip() in list(map(lambda slider: slider.title_ru.lower().strip(), Slider(platform=platform).objects.all())):
            slider.save()
            return redirect(SECURE_PATH_ADMIN + f"{platform}/slider/{slider.slug}/?title_error")
        else:
            slider.title_ru = title_ru
            slider.save()
            return redirect(SECURE_PATH_ADMIN + f"{platform}/slider/{slider.slug}/?edited")
        
    else: 
        answer = {
            "code": 404,
            "error": "Page Not Found"
        }
        return JsonResponse(answer, safe=False)


def control_panel_sliders_delete(request, platform):
    if request.method == "POST":
        slug = request.POST["slider_slug"]
        slider = get_object_or_404(Slider(platform=platform), slug=slug)
        slider.delete()
    return redirect(SECURE_PATH_ADMIN+f"{platform}/sliders/?deleted")



# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# Blogs

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

def control_panel_blog_all(request, platform):
    blogs= Blog(platform=platform).objects.all()
    context = {
        "base": base_context(request=request),
        "blogs":blogs
    }
    try:
        return render(request, f"control/{platform}/blogs/all.html", context)
    except TemplateDoesNotExist:
        answer = {
            "code": 404
        }
        return JsonResponse(answer, safe=False)


def control_panel_blog_add(request, platform):
    context = {
        "base": base_context(request=request)
    }
    try:
        return render(request, f"control/{platform}/blogs/add.html", context)
    except TemplateDoesNotExist:
        answer = {
            "code": 404
        }
        return JsonResponse(answer, safe=False)


def control_panel_blog_create(request, platform):    
    if request.method == "POST" and request.FILES["file"]:  
        title_ru = request.POST["title_ru"]
        title_uz = request.POST["title_uz"]
        description_uz = request.POST["description_uz"]
        description_ru = request.POST["description_ru"]

        if title_ru.lower().strip() in list(map(lambda category: category.title_ru.lower().strip(), Blog(platform=platform).objects.all())):
            return redirect(SECURE_PATH_ADMIN+f"{platform}/blog/add/?error")
        else:
            Blog(platform=platform).objects.create(
                title_uz=title_uz, title_ru=title_ru, description_ru=description_ru, description_uz=description_uz,
                img_full=request.FILES["file"])
            return redirect(SECURE_PATH_ADMIN+f"{platform}/blogs/?created")
    else: 
        answer = {
            "code": 404,
            "error": "Page Not Found"
        }
        return JsonResponse(answer, safe=False)


def control_panel_blog_detail(request, id, platform):
    blog= get_object_or_404(Blog(platform=platform), id=id)
    context = {
        "base": base_context(request=request),
        "blog": blog
    }
    try:
        return render(request, f"control/{platform}/blogs/detail.html", context)
    except TemplateDoesNotExist:
        answer = {
            "code": 404
        }
        return JsonResponse(answer, safe=False)


def control_panel_blog_edit(request, platform):    
    if request.method == "POST" or request.FILES["file"]:  
        blog = get_object_or_404(Blog(platform=platform), id=request.POST["blog_id"])
        blog.title_uz = request.POST["title_uz"]
        blog.description_uz = request.POST["description_uz"]
        blog.description_ru = request.POST["description_ru"]
        try: 
            blog.img_full = request.FILES["file"]
        except:
            pass

        if request.POST["title_ru"].lower().strip() == blog.title_ru.lower().strip():
            blog.save()
            return redirect(SECURE_PATH_ADMIN+f"{platform}/blog/{blog.id}/?edited")
        if request.POST["title_ru"].lower().strip() in list(map(lambda blog: blog.title_ru.lower().strip(), Blog(platform=platform).objects.all())):
            blog.save()
            return redirect(SECURE_PATH_ADMIN+f"{platform}/blog/add/?error")
        else:
            blog.title_ru = request.POST["title_ru"]
            blog.save()
            return redirect(SECURE_PATH_ADMIN+f"{platform}/blog/{blog.id}/?edited")
        


def control_panel_blog_delete(request, platform):
    if request.method == "POST":
        blog = get_object_or_404(Blog(platform=platform), id=request.POST["blog_id"])
        blog.delete()
        return redirect(SECURE_PATH_ADMIN + f"{platform}/blogs/?deleted")
