from django.shortcuts import render, redirect

from django.contrib import messages

from django.http import HttpResponse, JsonResponse


from .models import UserProfileImage

from django.contrib.auth.models import User

from django.contrib.auth import login, logout

from django.contrib.auth.decorators import login_required

from django.views.decorators.cache import cache_control

from django.http import HttpRequest

from datetime import datetime


class ControlUtils:
    def appendTimeStamp(self, requestObject:HttpRequest):
        # get the date and time
        dateAndTime = datetime.now().strftime("%d-%m-%Y")
        
        # add it to the request
        requestObject.session['date'] = dateAndTime
        
        return
        
    def validateSystemUser(self, userEmail, userPassword):
        # validate
        userInstance = User.objects.filter(email=userEmail).first()
        
        # get user status
        validationResult = False if not userInstance else userInstance.check_password(raw_password=userPassword)
        
        return validationResult, userInstance
    

    def savePrimaryUserInstance(self, userName, userEmail, userPassword, userIsAdmin=None):
        # create a user instance
        newUser = User.objects.create_user(
            username=userName,
            email=userEmail,
            password=userPassword)
        
        if userIsAdmin:
            # add admin status
            newUser.is_superuser = True
            
        else:
            # use is saved as staff
            pass
        
        newUser.save()
        
        return newUser
    
    
    def saveNewSystemUser(self, userName, userEmail, userPassword):
        # first save the user
        userInstance = self.savePrimaryUserInstance(
            userName=userName,
            userEmail=userEmail,
            userPassword=userPassword
        )
        
        # create a profile image instance
        newProfileImage = UserProfileImage(userInstance=userInstance)
        
        # save the specific user
        newProfileImage.save()
        
        return userInstance
        


def websiteHomePage(request):
    return render(request, "mariasite/pages/home.html")

def aboutPage(request):
    # defines page context
    pageContext = {
        'header_name': "About Us",
        'bg_image': None,
        'from_page': {
            "url": '#',
            'name': "Blog"
            }, 
        'to_page': None
        
    }
    
    return render(request, "mariasite/pages/about.html", context=pageContext)

def venuePage(request):
    pageContext = {
        'header_name': "Our Venues",
        'bg_image': None,
        'from_page': {
            "url": '#',
            'name': "Venues"
            }, 
        'to_page': None,
        'venue_list': [
            {
                'url': '#',
                'image': None,
                'name': 'Simba Resort',
                'description': 'Far far away, behind the word mountains, far from the countries Vokalia and Consonantia, there live the blind texts.',
                'capacity': '12'
            },
            
            {
                'url': '#',
                'image': None,
                'name': 'Charm Tree Shade',
                'description': 'Far far away, behind the word mountains, far from the countries Vokalia and Consonantia, there live the blind texts.',
                'capacity': '12'
            },

            {
                'url': '#',
                'image': None,
                'name': 'Picnic House',
                'description': 'Far far away, behind the word mountains, far from the countries Vokalia and Consonantia, there live the blind texts.',
                'capacity': '12'
            }

        ]
        
    }
    return render(request, "mariasite/pages/venues.html", context=pageContext)


def restaurantPage(request):
    pageContext = {
        'header_name': "Resto & Bar",
        'bg_image': None,  
        'from_page': {
            "url": '#',
            'name': "RESTO"
            }, 
        'to_page': None      
    }
    
    return render(request, "mariasite/pages/restaurant.html", context=pageContext)

def blogPostPage(request):
    pageContext = {
        'header_name': "Our Blog",
        'bg_image': None,  
        'from_page': {
            "url": '#',
            'name': "BLOG"
            }, 
        'to_page': None,
        'posts': [
            {
                'date': 'DEC. 23, 2020',
                'comment_count': 4,
                'heading': 'Best Hotel Near Beach in Kampala',
                'summary': 'A small river named Duden flows by their place and supplies it with the necessary regelialia.'
            },
            {
                'date': 'DEC. 23, 2020',
                'comment_count': 4,
                'heading': 'Best Hotel Near Beach in Kampala',
                'summary': 'A small river named Duden flows by their place and supplies it with the necessary regelialia.'
            },
            {
                'date': 'DEC. 23, 2020',
                'comment_count': 4,
                'heading': 'Best Hotel Near Beach in Kampala',
                'summary': 'A small river named Duden flows by their place and supplies it with the necessary regelialia.'
            }
            
        ]      
    }
    
    return render(request, "mariasite/pages/blog.html", context=pageContext)    

def contactPage(request):
    # defines page context
    pageContext = {
        'header_name': "Contact us",
        'bg_image': None,
        'from_page': {
            "url": '#',
            'name': "CONTACT"
            }, 
        'to_page': None
        
    }
    
    return render(request, "mariasite/pages/contact.html", context=pageContext)

# prevent page caching
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def homePage(request):
    if request.method == "POST":
        # get the data
        submittedFormData = request.POST.dict()
        
        userEmail = submittedFormData['email']
        
        userPassword = submittedFormData['password']
        
        # print("password:", userPassword)
        
        # userStatus
        userStatus, userObject = ControlUtils().validateSystemUser(
            userEmail=userEmail,
            userPassword=userPassword)
        
        # print("Status:", userStatus)
        
        # print("Status:", userStatus)
        if userStatus is True and userObject:
            # get the user profile image
            login(request, userObject)
            
            # add the date
            ControlUtils().appendTimeStamp(request)
                        
            # determine redirection route
            
            # admin
            if userObject.is_superuser:
                request.session['avatar'] = None
                
                return redirect("admin_panel:admin-home")
            
            else:
                # get the persons image
                usersProfileImage = userObject.profile_image
            
                try:
                    ProfileImageUrl = usersProfileImage.userImage.url
                    
                except:
                    ProfileImageUrl = None
                
            
                # store the avatar
                request.session['avatar'] = ProfileImageUrl
                
                
                # regular user
                return redirect("userenv:useraccount")
        
        else:
            # send back an error message
            messages.error(request, message='Either email or password is invalid')
            
                        
    else:
        pass

    
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect("admin_panel:admin-home")
        
        else:
            return redirect("userenv:useraccount")
    
    else:
        return render(request, 'mariadmin/login.html')


@login_required(login_url='messenger:home')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logoutUser(request):
    # logout the user
    logout(request)
    
    return redirect("messenger:welcome")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def registerPage(request):
    # extract the data
    if request.method == 'POST':
        # extract the data
        submittedData = request.POST.dict()
        
        # get the submitted form data
        userName = submittedData['username']
        
        userEmail = submittedData['email']
        
        userPassword = submittedData['password']
        
        # check for duplicates
        isNewUser = True if not User.objects.filter(email=userEmail).first() else False
        
        if isNewUser is True:
            # print(userName, userEmail, userPassword)
            
            # save the new user
            newUserAccount = ControlUtils().saveNewSystemUser(
                userName=userName,
                userEmail=userEmail,
                userPassword=userPassword,
            )
            
            # login the user
            login(request, newUserAccount)
            
            # add a time stamp
            ControlUtils().appendTimeStamp(request)
            
            return redirect("userenv:useraccount")
            
            
        else:
            # send back an error
            messages.warning(request, "Account already exits, try logging in!")
            
            return redirect("messenger:register")
        

    
    else:
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return redirect("admin_panel:admin-home")
            
            else:
                return redirect("userenv:useraccount")
        
        else:
            return render(request, 'mariadmin/register.html')