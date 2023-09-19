from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required

from django.views.decorators.cache import cache_control

from django.http import JsonResponse

from django.contrib import messages

from django.http import HttpRequest

from .models import (Category, 
                    AboutHeading, AboutDetails, LeftCard, 
                    RightCard, OfferedService, MiddleGrid, 
                    VenueItem, Testimonial, StatisticsMeta, Contacts, WebsiteHeadingImage, gardensTourVideoLink
                    )

from messenger.views import ControlUtils



def getAdminHomeContext():
    # get available categories
    availableCategories = [
            {
                'category': str(eachCategory),
                'tag': eachCategory.pk
            } for eachCategory in Category.objects.all()
        ]
    
    # get the banner image
    bannerImage = WebsiteHeadingImage.objects.all().first()
    
    videoLinkUrl = gardensTourVideoLink.objects.all().first() 
    
    adminContext = {
        'tour_video_link': videoLinkUrl.videoUrl if videoLinkUrl else None,
        'categories': availableCategories,
        'banner_image': bannerImage.imageUrl if bannerImage else None,
        'heading': str(AboutHeading.objects.all().first()) if AboutHeading.objects.all().first() else None,
        'about_detail': str(AboutDetails.objects.all().first()) if AboutDetails.objects.all().first() else None,
        'left_card_data': {'heading': LeftCard.objects.all().first().leftCardHeading, 'text': LeftCard.objects.all().first().leftCardText, 'image': LeftCard.objects.all().first().leftCardImageUrl} if LeftCard.objects.all().first() else None,
        'right_card_data': {'heading': RightCard.objects.all().first().rightCardHeading, 'text': RightCard.objects.all().first().rightCardText, 'image': RightCard.objects.all().first().rightCardImageUrl} if RightCard.objects.all().first() else None,
        'uploads': ControlUtils().getUploadsData(),
        'services': [
            {'name': eachService.serviceName, 'details': eachService.serviceDetails, 'id':eachService.pk} for eachService in OfferedService.objects.all()],
        'ribbon': {
            'heading': MiddleGrid.objects.all().first().gridTitle,
            'message': MiddleGrid.objects.all().first().gridMessage,
            'text': MiddleGrid.objects.all().first().gridButtonText,
            'url': MiddleGrid.objects.all().first().gridRedirectionUrl
            },
        'venues': [
                {
                    'name': eachVenue.venueName,
                    'capacity': eachVenue.venueCapacity,
                    'description': eachVenue.venueDescription.capitalize(),
                    'featured': eachVenue.isFeatured,
                    'id': eachVenue.pk
                } for eachVenue in VenueItem.objects.all()
            ],
        'testimonials': [
                {
                    'name': eachTestimonial.guestName,
                    'comment': eachTestimonial.guestComment,
                    'position': eachTestimonial.guestPosition,
                    'image': eachTestimonial.guestImageUrl,
                    'id': eachTestimonial.pk
                } for eachTestimonial in Testimonial.objects.all()
            ],
        'statistics': {
                'guests': StatisticsMeta.objects.all().first().happyGuests,
                'events': StatisticsMeta.objects.all().first().hostedEvents,
                'staff': StatisticsMeta.objects.all().first().staffCount,
                'venues': StatisticsMeta.objects.all().first().venueCount
            
            },
        'contacts': [
                {
                    'type': eachContact.contactType.capitalize(),
                    'value': eachContact.contactValue,
                    'id': eachContact.pk
                } for eachContact in Contacts.objects.all()
            ]
        }


    return adminContext

def determinePageRoute(accessTag):
    # 'website': True,
    # 'blog': True,
    # 'pages': True,
    # 'comms': True,
    # 'users': True
    if accessTag == 'blog':
        redirectObject = redirect("messenger:blog-editor")
        
    elif accessTag == 'pages':
        redirectObject = redirect("messenger:page-registry")
        
    elif accessTag == 'comms':
        redirectObject = redirect("messenger:chat-page")
        
    else:
        redirectObject = redirect("messenger:next-of-kins")
        
    return redirectObject

def getFirstPermission(request:HttpRequest):
    # get first permission
    for eachPermission, permissionValue in request.session['allowed_pages'].items():
        if permissionValue is True:
            firstPermission = eachPermission
            break
        

    return firstPermission
    
    
        
    

@login_required(login_url='messenger:home')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminHomePage(request):
    # determine if its the home page to be displayed
    if request.session['allowed_pages']['website'] is True:
        # load
        adminContext = getAdminHomeContext()
        
        return render(request, "mariadmin/index.html", context=adminContext)
    
    else:
        # determine redirection route
        firstPermission = getFirstPermission(request=request)
        
        # get a route
        responseObject = determinePageRoute(accessTag=firstPermission)
        
        return responseObject


    
    
    



@login_required(login_url='messenger:home')
def registerCategory(request):
    if request.method == "POST":
        # get the submitted data
        submittedData = request.POST.dict()
        
        # get the category name
        reportedCategoryName  = submittedData['category-name'].lower().capitalize()
        
        isItDuplicate = Category.objects.filter(modelName=reportedCategoryName).first()
        
        if isItDuplicate:
            # alert error
            messages.warning(request, "Category Name exists already!")
        
        else:
            # create the new category
            newCategory = Category.objects.create(modelName=reportedCategoryName)
            
            # save the new category
            newCategory.save()
            
            # alert success
            messages.success(request, "Category name was registered!")
            
        return redirect("admin_panel:admin-home")
    
    else:
        # print("Here")
        
        return JsonResponse(
            dict(
                message = 'resource not accessible'
            )
        )
        
@login_required(login_url='messenger:home')
def deleteCategory(request, categoryId):
    # get and delete the object
    categoryToDelete = get_object_or_404(Category, pk=categoryId)
    
    # delete the category
    categoryToDelete.delete()
    
    return redirect("admin_panel:admin-home")


