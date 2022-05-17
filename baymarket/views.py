from django.shortcuts import render

def base_context(request): 
    platform = request.build_absolute_uri().split("/control/")[1].split("/")[0]
    context = {
        "platform": platform
    }
    return context


def control_baymarket_index(request, platform):
    context= {
        "base": base_context(request)
    }
    return render(request, f"control/{platform}/index.html", context)


def control_baymarket_categories_all(request):
    context= {
        "base": base_context(request)
    }
    return render(request, "control/baymarket/categories/all.html", context)