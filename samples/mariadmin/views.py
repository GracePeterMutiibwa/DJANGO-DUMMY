from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from django.views.decorators.cache import cache_control



@login_required(login_url='messenger:home')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminHomePage(request):
    return render(request, "mariadmin/index.html")
