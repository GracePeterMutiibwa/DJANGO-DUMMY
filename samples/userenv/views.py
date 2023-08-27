from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

@login_required(login_url="messenger:home")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def accountsHomePage(request):
    # context={'avatar': request.session['avatar']}
    
    if request.user.is_superuser:
        return redirect("admin_panel:admin-home")
    
    else:
        # print("date:", request.session['date'])
        
        # chat-page.html
        return render(request, "mariadmin/profile-page.html", )
