from django.shortcuts import render, redirect, get_object_or_404, resolve_url

from django.contrib import messages

from django.http import JsonResponse, HttpResponse

from .editor_processor import SectionUtils, ChatUtilities

from .posts_utilities import PostsManager, PostTools

from .page_utilities import PageManager, PageTools

from .admin_controls import AdminTools, AdminUtilities

from .reset_processor import ResetUtilities, CodeValidationUtilities, PasswordRestTools

from .venue_control import VenueUtilities, VenueTools

from .mail_processor import MessengerUtils

from django.db.models import Q


from .models import UserProfileImage


from django.contrib.auth.models import User

from django.contrib.auth import login, logout

from django.contrib.auth.decorators import login_required, user_passes_test

from django.views.decorators.cache import cache_control

from django.http import HttpRequest

from datetime import datetime


from mariadmin.models import (Category, ImageAsset,
            AboutHeading, AboutDetails, LeftCard, RightCard,
            OfferedService, MiddleGrid, VenueItem,
            Testimonial, StatisticsMeta, Contacts, MessageEntryNames, MessageFlow,
            SimpleContactMessages, EmailHolders, EmailReplies, PageCategory, VendorPage,
            EmailReset, NotAccessibleYet, WebsiteHeadingImage,
            gardensTourVideoLink, EventsServicesContacts,
            BookingFormDetail, AboutImage
            )

from userenv.views import ProcessingUtilities

def isAdmin(userInstance):
    return userInstance.is_authenticated and userInstance.is_superuser

class CommUtilities:
    def deleteMessageThread(self, userName, userEmail):
        # delete the holder
        associatedHolder = EmailHolders.objects.filter(userEmail=userEmail).first()

        if associatedHolder:
            associatedHolder.delete()
            
        else:
            pass

        # delete the messages thread
        messageThread = SimpleContactMessages.objects.filter(UserName=userName)

        if messageThread:
            messageThread.delete()

        return

    def getInboxCount(self):
        currentCount = SimpleContactMessages.objects.all().count()

        return currentCount

    def getHolderCount(self):
        currentCount = EmailHolders.objects.all().count()

        return currentCount

    def getEmailEntries(self):
        allEmails = [emailHolderObject.userEmail for emailHolderObject in EmailHolders.objects.all()]

        return allEmails

    def getMessagesFromEmail(self, emailAddress):
        # get all the emails
        presentEmails = SimpleContactMessages.objects.filter(UserEmail=emailAddress)

        emailMeta = [
            {
                'date': eachEmail.dateSent.strftime("On %d-%m-%Y, at %H:%M %p"),
                'subject': eachEmail.UserSubject,
                'name': eachEmail.UserName,
                'email': eachEmail.UserEmail,
                'message': eachEmail.UserMessage,
                'initials': eachEmail.UserName.split(" ")[0][0].upper()

            } for eachEmail in presentEmails
        ]

        return emailMeta


    def getLatestEmailData(self, emailAddress):
        latestEmail = SimpleContactMessages.objects.filter(UserEmail=emailAddress).order_by("-dateSent").first()

        return {
            'name': latestEmail.UserName,
            'message': latestEmail.UserMessage,
            'email': latestEmail.UserEmail,
            'date': latestEmail.dateSent.strftime("%d-%m-%Y, %H:%M %p"),
            'initials': latestEmail.UserName.split(" ")[0][0].upper()
        }

    def getPresentReplies(self):
        # replies present
        presentReplies = EmailReplies.objects.all()

        # extract the data
        extractedReplies = [
            {
                'to':str(eachEmailReply.associatedHolder),
                'when': eachEmailReply.dateCreated.strftime("%d-%m-%Y, %H:%M %p"),
                'message': eachEmailReply.replyMessage,
                'id': eachEmailReply.pk
            } for eachEmailReply in presentReplies
        ]

        return extractedReplies

    def getAllPresentEmails(self):
        # get a list of email holders
        holdersList = self.getEmailEntries()

        emailData = [
                        self.getLatestEmailData(emailAddress=eachEmailHolder) for eachEmailHolder in holdersList
                    ]

        return emailData



    def extractUserName(self, fromToMetaObject:str):
        # extract the name
        fromSection, toSection = fromToMetaObject.split(">>>")

        userName = toSection if fromSection == 'admin' else fromSection

        return userName

    def getInitialChat(self):
        # get present names
        latestChatObject = MessageFlow.objects.all().order_by("-dateSent").first()

        if latestChatObject is None:
            associatedUserName, associatedEmail, firstChatData = None, None, None

        else:
            # get the meta object
            nameMetaObject = latestChatObject.fromToMeta

            # extract the name out of the object
            associatedUserName = self.extractUserName(fromToMetaObject=nameMetaObject)

            associatedEmail = User.objects.filter(username=associatedUserName).first().email

            # first chat
            firstChatData = self.getChatsOfUser(userName=associatedUserName)

        return associatedUserName, associatedEmail, firstChatData



    def getContactsWithChats(self):
        # get those with chats
        thoseWithChats = [eachObject.UserName for eachObject in  MessageEntryNames.objects.all()]

        return thoseWithChats

    def getChatsOfUser(self, userName):
        presentChats = ProcessingUtilities().getTheAvailableMessagesFlow(userName=userName)

        return presentChats

    def getLatestMessageAndTime(self, userName, section):
        # fromToMeta
        fromToMeta = f"{userName}>>>admin"


        # get the messages
        latestMessageObject = MessageFlow.objects.filter(fromToMeta=fromToMeta).order_by("-dateSent").first()

        # print("Object:", userName)

        if section == 1:
            if not latestMessageObject is None:
                # get the time the message was sent
                lastSentMessageTime = latestMessageObject.dateSent.strftime("%H:%M %p")
                
            else:
                lastSentMessageTime = None

            return lastSentMessageTime

        elif section == 2:
            if not latestMessageObject is None:
                # get the actual message
                lastSentMessageBody = latestMessageObject.messageMeta
                
            else:
                lastSentMessageBody = None

            return lastSentMessageBody
        
        else:
            # get the status
            validityStatus = True if latestMessageObject else False
            
            return validityStatus




    def getAvailableContactInfoOnChatUsers(self):
        # get users with chats
        havingChats = self.getContactsWithChats()


        # preparedData
        preparedMessageData = [
            {
                'name': eachContactName,
                'date': self.getLatestMessageAndTime(eachContactName, 1),
                'message': self.getLatestMessageAndTime(eachContactName, 2),
                'avatar': self.getUserAvatar(userName=eachContactName),
                'initials': eachContactName.split(" ")[0][0].upper()

            } for eachContactName in havingChats if self.getLatestMessageAndTime(userName=eachContactName, section=3)
        ]

        # print("Chats:", len(preparedMessageData))

        return preparedMessageData



    def updateUserAvatar(self, userId, imageUrl, request:HttpRequest):
        # get the user instance
        userObject = User.objects.filter(pk=int(userId)).first()

        # get image object
        userImageObject = userObject.profile_image

        # update
        userImageObject.userProfileImage = imageUrl

        # save the object again
        userImageObject.save()

        # update the session
        request.session['avatar'] = imageUrl

        return


    def getUserAvatar(self, userName):
        print("Found Name:", userName)
        # get the user instance
        userObject = User.objects.filter(username=userName).first()

        # get the persons image
        foundImageUrl = userObject.profile_image.userProfileImage

        # print("Url:", foundImageUrl)

        profileImageUrl = None if (foundImageUrl is None or len(foundImageUrl) == 0) else foundImageUrl

        return profileImageUrl

    def getAvailableContacts(self):
        # get those with chats
        contactsToExclude = self.getContactsWithChats()

        # get contacts without chats
        usersToFilter = User.objects.exclude(username__in=contactsToExclude)

        filteredContactNames = sorted([userObject.username for userObject in usersToFilter if userObject.is_superuser is False])

        contactsDetail = [
            {
                'name': eachContactName,
                'email': User.objects.filter(username=eachContactName).first().email,
                'avatar': self.getUserAvatar(userName=eachContactName),
                'initials': eachContactName.split(" ")[0][0].upper()
            } for eachContactName in filteredContactNames
        ]

        return contactsDetail


class ControlUtils:
    def getContactData(self, whatToGet=1):
        # get the contacts
        contactsObject = Contacts.objects.all() if whatToGet == 1 else EventsServicesContacts.objects.all()

        presentContactData = {
            eachContact.contactType: eachContact.contactValue for eachContact in contactsObject
        }

        return presentContactData

    def getRibbonDetails(self):
        ribbonDetails = {
            'heading': MiddleGrid.objects.all().first().gridTitle,
            'message': MiddleGrid.objects.all().first().gridMessage,
            'text': MiddleGrid.objects.all().first().gridButtonText,
            'url': MiddleGrid.objects.all().first().gridRedirectionUrl
            }

        return ribbonDetails
    def getVenueDetails(self, venueName):
        # get the instance
        venueToView = get_object_or_404(VenueItem, venueName=venueName)

        excludedVenues = [
                            {
                                'image': eachVenue.hasImages(checkState=2),
                                'name': eachVenue.venueName,
                                'description': eachVenue.venueDescription,
                                'capacity': eachVenue.venueCapacity,
                            } for eachVenue in VenueItem.objects.exclude(pk=venueToView.pk) if (eachVenue.hasImages(checkState=1) is True)
                        ]

        # get the details
        venueDetails = {
            'name': venueName,
            'venue_images': VenueTools().getAllVenueImages(venueId=venueToView.pk),
            'description': venueToView.venueDescription,
            'capacity': venueToView.venueCapacity,
            'categories': venueToView.venueCategory.split("|||"),
            'id': venueToView.pk,
            'excluded': excludedVenues
        }

        return venueDetails

    def getTestimonials(self):
        presentTestimonials = [
                {
                    'name': eachTestimonial.guestName,
                    'comment': eachTestimonial.guestComment,
                    'position': eachTestimonial.guestPosition,
                    'image': eachTestimonial.guestImageUrl,
                } for eachTestimonial in Testimonial.objects.all()
            ]

        return presentTestimonials


    def getVenueInfo(self, whatToGet):
        if whatToGet == 1:
            venueData = [
                            {
                                'url': '#',
                                'image': eachVenue.hasImages(checkState=2),
                                'name': eachVenue.venueName,
                                'description': eachVenue.venueDescription,
                                'capacity': eachVenue.venueCapacity,
                            } for eachVenue in VenueItem.objects.all() if (eachVenue.hasImages(checkState=1) is True)
                        ]

        else:
            venueData = [
                            {
                                'url': '#',
                                'image': eachVenue.hasImages(checkState=2),
                                'name': eachVenue.venueName,
                                'description': eachVenue.venueDescription,
                                'capacity': eachVenue.venueCapacity,
                            } for eachVenue in VenueItem.objects.filter(isFeatured=True) if (eachVenue.hasImages(checkState=1) is True)
                        ]

        return venueData


    def getUploadsData(self, forGallery=False):
        # get all images
        if forGallery is False:
            attachedImages = ImageAsset.objects.all()

        else:
            attachedImages = ImageAsset.objects.filter(isGalleryItem=True)

        # get present images data
        # "/media/" + 
        uploadsMetaData = [
            
            {
                'name': eachImageMeta.imageName,
                'data': eachImageMeta.imageData.url,
                'id': eachImageMeta.pk,
                'date': eachImageMeta.uploadDate.strftime("On %d-%b-%Y At %H:%M %p") if eachImageMeta.uploadDate else "",
                'for_gallery': eachImageMeta.isGalleryItem
            }

            for eachImageMeta in attachedImages
        ]
        
        print("Data:", uploadsMetaData)

        return uploadsMetaData


    def saveNewFileUpload(self, imageName, imageSize, imageData):
        # save
        imageObject = ImageAsset.objects.create(
            imageName=imageName,
            imageSize=imageSize
        )

        # add the image
        imageObject.imageData = imageData
        
        # print("File Path:", imageData)

        # save the image to the database
        imageObject.save()

        return


    def appendTimeStamp(self, requestObject:HttpRequest):
        # get the date and time
        dateAndTime = datetime.now().strftime("%d-%m-%Y")

        # add it to the request
        requestObject.session['date'] = dateAndTime

        return

    def validateSystemUser(self, userEmail, userPassword):
        # validate access blockage
        isNotAccessible = NotAccessibleYet.objects.filter(adminEmailAddress=userEmail).first()

        if isNotAccessible:
            # print("Found Admin:", isNotAccessible.adminEmailAddress)

            return None, None

        else:
            # pass they can continue
            pass


        # validate
        userInstance = User.objects.filter(email=userEmail).first()
        
        print("Is Present:", userInstance)

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


class HelperUtils:
    # latest
    def getAvailableServices(self):
        pass


    def getCountryList(self):
        countryList = ['Abim', 'Adjumani', 'Agago', 'Alebtong', 'Amolatar', 'Amudat', 'Amuria', 'Amuru', 'Apac', 'Arua', 'Budaka', 'Bududa', 'Bugiri', 'Buhweju', 'Buikwe', 'Bukedea',
                        'Bukomansimbi', 'Bukwo', 'Bulambuli', 'Buliisa', 'Bundibugyo', 'Bushenyi', 'Busia', 'Butaleja',
                        'Butambala', 'Buvuma', 'Buyende', 'Dokolo', 'Gomba', 'Gulu', 'Hoima',
                        'Ibanda', 'Iganga', 'Isingiro', 'Jinja', 'Kaabong', 'Kabale', 'Kabarole',
                        'Kaberamaido', 'Kalangala', 'Kaliro', 'Kalungu', 'Kampala', 'Kamuli', 'Kamwenge', 'Kanungu',
                        'Kapchorwa', 'Kasese', 'Katakwi', 'Kayunga', 'Kibaale', 'Kiboga', 'Kibuku', 'Kiruhuura', 'Kiryandongo', 'Kisoro', 'Kitgum', 'Koboko',
                        'Kole', 'Kotido', 'Kumi', 'Kween', 'Kyankwanzi', 'Kyegegwa', 'Kyenjojo', 'Lamwo', 'Lira', 'Luuka', 'Luwero', 'Lwengo', 'Lyantonde', 'Manafwa', 'Masaka', 'Masindi', 'Mayuge', 'Mbale', 'Mbarara', 'Mitoma', 'Mityana', 'Moroto', 'Moyo', 'Mpigi', 'Mubende', 'Mukono', 'Nakapiripirit', 'Nakaseke',
                        'Nakasongola', 'Namayingo', 'Namutumba', 'Napak', 'Nebbi', 'Ngora', 'Ntoroko', 'Ntungamo', 'Nwoya', 'Nyadri', 'Otuke', 'Oyam',
                        'Pader', 'Pallisa', 'Rakai', 'Rubirizi', 'Rukungiri', 'Sembabule', 'Serere', 'Sheema', 'Sironko', 'Soroti',
                        'Tororo', 'Wakiso', 'Yumbe', 'Zombo'
                    ]

        return sorted(countryList)


def getCategoryPageCount(categoryName):
    # get pages that match that category
    matchingObjects = VendorPage.objects.filter(pageCategory=categoryName, isVisible=True)

    pageCount = len([
        eachObject for eachObject in matchingObjects if (eachObject.isVisibleAndHasServices() is True)
    ])

    return pageCount



def getPageCategoryMeta():
    # get all categrories
    presentPageCategories = PageCategory.objects.all()

    categoriesAndCounts = [
        {
            'name': eachCategory.categoryName,
            'count': getCategoryPageCount(categoryName=eachCategory.categoryName)

        } for eachCategory in presentPageCategories
    ]

    return categoriesAndCounts

def getEventCategories():
    presentCategories = [
        {
            'category': str(eachCategory),
            'tag': eachCategory.pk
        } for eachCategory in Category.objects.all()
    ]

    return presentCategories

def websiteHomePage(request):
    # get the banner image
    bannerImage = WebsiteHeadingImage.objects.all().first()

    videoLinkUrl = gardensTourVideoLink.objects.all().first()
    
    aboutImageObject = AboutImage.objects.all().first()

    # print("Link:", bannerImage.imageUrl)
    
    # "/media/" + 
    homeContext = {
        'home_page': True,
        'about_image_url': aboutImageObject.aboutImageUrl if aboutImageObject else None,
        'page_category_meta': getPageCategoryMeta(),
        'home_page_previews': PageTools().getPagePreviews(limit=6),
        'banner_image': bannerImage.imageUrl if bannerImage else None,
        'tour_video_link': videoLinkUrl.videoUrl if videoLinkUrl else None,
        'district_list': HelperUtils().getCountryList(),
        'heading': str(AboutHeading.objects.all().first()),
        'about_detail': str(AboutDetails.objects.all().first()),
        'left_card_data': {'heading': LeftCard.objects.all().first().leftCardHeading, 'text': LeftCard.objects.all().first().leftCardText, 'image': LeftCard.objects.all().first().leftCardImageUrl} if LeftCard.objects.all().first() else None,
        'right_card_data': {'heading': RightCard.objects.all().first().rightCardHeading, 'text': RightCard.objects.all().first().rightCardText, 'image': RightCard.objects.all().first().rightCardImageUrl} if RightCard.objects.all().first() else None,
        'services': [
            {'name': eachService.serviceName, 'details': eachService.serviceDetails, 'id':eachService.pk} for eachService in OfferedService.objects.all()
            ],
        'ribbon': ControlUtils().getRibbonDetails(),
        'featured_list': ControlUtils().getVenueInfo(2),
        'statistics': {
                'guests': StatisticsMeta.objects.all().first().happyGuests,
                'events': StatisticsMeta.objects.all().first().hostedEvents,
                'staff': StatisticsMeta.objects.all().first().staffCount,
                'venues': StatisticsMeta.objects.all().first().venueCount

            },
        'contacts': ControlUtils().getContactData(),
        'featured_posts': PostTools().getFooterPosts(),

        }

    return render(request, "mariasite/pages/home.html", context=homeContext)


def aboutPage(request):
    # defines page context
    bannerImage = WebsiteHeadingImage.objects.all().first()

    pageContext = {
        'banner_image': bannerImage.imageUrl if bannerImage else None,
        'testimonials': ControlUtils().getTestimonials(),
        'header_name': "About Us",
        'bg_image': None,
        'from_page': {
            "url": '#',
            'name': "Blog"
            },
        'to_page': None,
        'testimonials': ControlUtils().getTestimonials(),
        'ribbon': ControlUtils().getRibbonDetails(),


    }

    return render(request, "mariasite/pages/about.html", context=pageContext)

def imagePreProcessingEngine(imageListObject):
    if len(imageListObject) == 0:
        resultList = []

    else:
        # create groups
        chopSize = 4

        maximumSize = len(imageListObject)

        # groups of images
        resultList = [imageListObject[i : i + chopSize] for i in range(0, maximumSize, chopSize)]

    return resultList


def galleryPage(request):
    # get uploads
    presentUploads = ControlUtils().getUploadsData(forGallery=True)

    # process the images
    processedGalleryImages = imagePreProcessingEngine(imageListObject=presentUploads)

    # print("Groups:", len(processedGalleryImages))

    pageContext = {
        'hide_gallery': True,
        'header_name': "Our Gallery",
        'bg_image': None,
        'from_page': {
            "url": '#',
            'name': "Gallery"
            },
        'to_page': None,
        'contacts': ControlUtils().getContactData(),
        'gallery_images': processedGalleryImages

    }

    return render(request, "mariasite/pages/gallery.html", context=pageContext)


def venuePage(request):
    pageContext = {
        'header_name': "Our Venues",
        'bg_image': None,
        'from_page': {
            "url": '#',
            'name': "Venues"
            },
        'to_page': None,
        'venue_list': ControlUtils().getVenueInfo(1)

    }
    return render(request, "mariasite/pages/venues.html", context=pageContext)

def viewVenueDetails(request, venueName):
    pageContext = {
        'header_name': f"{venueName} Details",
        'bg_image': None,
        'from_page': {
            "url": resolve_url("messenger:venue"),
            'name': "Venues"
            },
        'to_page': venueName,
        'venue_details': ControlUtils().getVenueDetails(venueName=venueName),
        'contacts': {
            eachContact.contactType: eachContact.contactValue for eachContact in Contacts.objects.all()
            }

    }
    return render(request, "mariasite/pages/venue-details.html", context=pageContext)

def viewServicesByDistrict(request):
    # get the selected district
    selectedDistrict = request.POST['selected-district']

    pageContext = {
        'page_category_meta': getPageCategoryMeta(),
        'referer': "district",
        'district_list': HelperUtils().getCountryList(),
        'home_page_previews': PageTools().getPagePreviews(districtRequired=selectedDistrict),
        'header_name': "Service Providers & Partners",
        'bg_image': None,
        'from_page': {
            "url": '#',
            'name': "Our Service Partners"
            },
        'to_page': None
    }

    return render(request, "mariasite/pages/present-providers.html", context=pageContext)


def viewServicesByCategory(request, serviceCategory):
    pageContext = {
        'page_category_meta': getPageCategoryMeta(),
        'referer': "category",
        'district_list': HelperUtils().getCountryList(),
        'home_page_previews': PageTools().getPagePreviews(categoryRequired=serviceCategory),
        'header_name': "Service Providers & Partners",
        'bg_image': None,
        'from_page': {
            "url": '#',
            'name': "Our Service Partners"
            },
        'to_page': None
    }

    return render(request, "mariasite/pages/present-providers.html", context=pageContext)


def servicesPageView(request):
    pageContext = {
        'referer': "home",
        'home_page_previews': PageTools().getPagePreviews(limit=6),
        'page_category_meta': getPageCategoryMeta(),
        'district_list': HelperUtils().getCountryList(),
        'header_name': "Service Providers & Partners",
        'bg_image': None,
        'from_page': {
            "url": '#',
            'name': "Our Service Partners"
            },
        'to_page': None
    }

    return render(request, "mariasite/pages/present-providers.html", context=pageContext)



def viewBlogPostDetails(request, pageId):
    # check presence
    postIsPresent = PostTools().confirmPostPresence(postId=pageId)

    if postIsPresent is False:
        return redirect("messenger:blog")

    else:
        # proceed
        pass

    # get the comments
    postComments = PostTools().getPostComments(postId=pageId)

    pageContext = {
        'header_name': "Our Blog",
        'bg_image': None,
        'from_page': {},
        'post_id': pageId,
        'blog_details': True,
        'post_details': PostTools().getSinglePostMeta(postId=pageId),
        'featured_posts': PostTools().getFeaturedPosts(),
        'comments': postComments,
        'comments_count': len(postComments),
        'footer_posts': PostTools().getFooterPosts(idToIgnore=pageId),
        'contacts': ControlUtils().getContactData()
    }

    return render(request, "mariasite/pages/blog-page.html", context=pageContext)


def submitPostComment(request):
    # save the post
    idOfPost = PostsManager(request=request).savePostComment()

    # alert
    return redirect("messenger:blog-post", pageId=idOfPost)

def blogPostPage(request):
    # get available post previews
    availablePostPreviews = PostTools().getBlogPagePreviews()

    # print('data:', availablePostPreviews)

    pageContext = {
        'header_name': "Our Blog",
        'bg_image': None,
        'from_page': {
            "url": '#',
            'name': "BLOG"
            },
        'to_page': None,
        'available_post_previews': availablePostPreviews,
        'featured_posts': PostTools().getFeaturedPosts(),
        'contacts': ControlUtils().getContactData()
    }

    return render(request, "mariasite/pages/blog.html", context=pageContext)


@login_required(login_url='messenger:home')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def recordBookingInformation(request):
    submittedData = request.POST.dict()

    # get the submitted data
    submittedName = submittedData['user-name'].title()

    submittedEmail = submittedData['user-email']

    submittedContact = submittedData['user-phone']

    submittedCategory = submittedData['event-category']

    guestNumber = int(submittedData['guest-number'])

    bookingMessage = submittedData['booking-message'].capitalize()

    # email message
    emailMessage = f"""NAMES: {submittedName}, CONTACT: {submittedContact}, EVENT CATEGORY: {submittedCategory}, GUEST NUMBER: {guestNumber}, DETAILS : {bookingMessage}"""

    #save
    writeMailMessageData(
        submittedUserName=submittedName,
        submittedUserEmail=submittedEmail,
        submittedMessageSubject="MARIAHILL GARDENS BOOKING",
        submittedActualMessage=emailMessage
    )

    # send message
    messages.success(request, "Booking request sent successfully!")

    return redirect("messenger:book-gardens")



def bookMariahillGardens(request):
    # get the booking form object
    bookingFormObject = BookingFormDetail.objects.all().first()

    bookingFormText, bookingFormImage = bookingFormObject.formText, bookingFormObject.imageUrl

    # defines page context
    pageContext = {
        "booking_section": True,
        "contact_form_text": bookingFormText,
        "booking_image": bookingFormImage,
        'header_name': "Book Mariahill Gardens",
        'event_categories': getEventCategories(),
        'bg_image': None,
        'from_page': {
            "url": '#',
            'name': "BOOKING"
            },
        'to_page': None,
        'contacts': ControlUtils().getContactData(whatToGet=1),

    }

    return render(request, "mariasite/pages/booking.html", context=pageContext)

def contactPage(request):
    # defines page context
    pageContext = {
        'header_name': "Contact us",
        'bg_image': None,
        'from_page': {
            "url": '#',
            'name': "CONTACT"
            },
        'to_page': None,
        'contacts': ControlUtils().getContactData(whatToGet=1),
        'events_contacts': ControlUtils().getContactData(whatToGet=2)

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

                # determine who they are and get their detail
                AdminTools().getAccessDetailOfAdmin(requestObject=request)

                return redirect("admin_panel:admin-home")

            else:
                # get the persons image
                profileImageUrl = CommUtilities().getUserAvatar(userName=request.user.username)


                # store the avatar
                request.session['avatar'] = profileImageUrl


                # regular user
                return redirect("userenv:useraccount")

        else:
            if userStatus is None:
                # alert access denial
                messages.error(request, message='Consult your administrator to grant you access! 😌')

            else:
                # wrong or invalid details

                # send back an error message
                messages.error(request, message='Either email or password is invalid')


    else:
        pass


    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect("admin_panel:admin-home")

        else:
            # regular user
            return redirect("userenv:useraccount")

    else:
        return render(request, 'mariadmin/login.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def resetUserPassword(request):
    if request.method == "GET":
        cookieValue, redirectionObject = getSetCookie(request=request)

        if cookieValue:
            pass

        else:
            # redirect the user
            return redirectionObject

        resetObject = EmailReset.objects.filter(attachedEmail=cookieValue).first()

        # print("Code:", cookieValue)

        # validate expiry
        resetValidity = True if resetObject and resetObject.timeNotYetExpired() else False

        if resetValidity is True:
            pass

        else:
            # tell them
            messages.warning(request, "The Token expired please try again!")

            return redirect("messenger:start-reset")


        # get the name and email
        pageContext = {
            'reset_email': cookieValue

        }

        return render(request, "mariadmin/password-reset.html", context=pageContext)

    else:
        # get the new password
        matchStatus, changeStatus = PasswordRestTools(request=request).resetUserPassword()

        if matchStatus is True:
            # change
            if changeStatus is True:
                messages.success(request, "Your password was changed successfully 🤗, please login down below 👇")

                return redirect("messenger:home")

            else:
                messages.warning(request, "Server Issues were a problem, please Try again 😌!")

                return redirect("messenger:start-reset")

        else:
            if matchStatus is None:
                # alert passwords mismatch
                messages.warning(request, "Server Issues were a problem, please Try again 😌!")

                return redirect("messenger:start-reset")

            else:
                # alert passwords mismatch
                messages.warning(request, "Please ensure that your passwords match 😌!")


                return redirect("messenger:password-reset")



def getSetCookie(request:HttpRequest):
    # get the cookie
    cookieValue = request.COOKIES.get('reset_email', None)


    # find out if the user is eligible
    resetEligibility = True if cookieValue else False

    if resetEligibility is True:
        # in case all is well
        responseObject = None

    else:
        # redirect them
        responseObject = redirect("messenger:start-reset")

    return cookieValue, responseObject


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def displayResetPage(request):
    if request.method == "GET":

        cookieValue, redirectionObject = getSetCookie(request=request)

        if cookieValue:
            pass


        else:
            # redirect the user
            return redirectionObject

        # get the name and email
        pageContext = {
            'reset_email': cookieValue

        }

        # debug
        # print("Received the reset essentials")

        return render(request, "mariadmin/reset-code.html", context=pageContext)

    else:
        # get the submiited data
        validationStatus, referenceEmail = CodeValidationUtilities(request=request).validateResetToken()

        if validationStatus is True:
            # display the password reset page
            resetPage = redirect("messenger:password-reset")

            resetPage.set_cookie("reset_email", referenceEmail)

            return  resetPage

        else:
            # create a validation message for the situation
            validationMessage = "Token Expired, please get another one" if validationStatus is False else "Invalid Page Request"

            # load message
            messages.warning(request, validationMessage)

            if validationStatus is False:
                return redirect("messenger:start-reset")

            else:
                # alert wrong token
                return redirect("messenger:home")




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def getResetCodeViaEmail(request):
    pageContext = {

    }

    # get the users email address
    if request.method == "POST":
        # object
        resetEmailObject = request.POST.dict()

        # get the email
        userEmail = resetEmailObject['reset-email']

        # get the detailse
        isEmailValidObject = User.objects.filter(email=userEmail).first()

        # debug
        # print("Status:", True if isEmailValid else False)

        if isEmailValidObject:
            # get the users name
            userName = isEmailValidObject.username

            # send reset code
            pushStatus = ResetUtilities().sendResetCode(toEmailAddress=userEmail, nameOfUser=userName)

            # validate
            if pushStatus is False:
                # alert
                messages.warning(request, "Check your email address 😁, you already have a reset code email and enter the code below 👇!")

            else:
                # proceed to the reset code page
                pass

            # add reset email and name to the cookie
            resetResponse = redirect("messenger:collect-reset-code")

            # set  a cookie
            resetResponse.set_cookie("reset_email", userEmail)


            return resetResponse



        else:
            # alert
            messages.warning(request, "The email address provided does not seem to be attached to any account 😌")

            # add the email address to the request
            pageContext['reset_email'] = userEmail



    return render(request, "mariadmin/goto-reset.html", context=pageContext)


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
            messages.warning(request, "Account already exists, try logging in!")

            return redirect("messenger:register")



    else:
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return redirect("admin_panel:admin-home")

            else:
                return redirect("userenv:useraccount")

        else:
            return render(request, 'mariadmin/register.html')

@login_required(login_url='messenger:home')
def wipeMessagesThread(request):
    # get the name and email
    submittedThreadMeta = request.POST.dict()

    # delete the data
    CommUtilities().deleteMessageThread(
        userName=submittedThreadMeta['user-name'],
        userEmail=submittedThreadMeta['user-email']
    )

    # debug
    inboxCount = CommUtilities().getInboxCount()

    userCount = CommUtilities().getHolderCount()


    return JsonResponse(
        dict(
            inbox = inboxCount,
            holder = userCount

        )
    )

@login_required(login_url='messenger:home')
@user_passes_test(isAdmin)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deleteSpecificUpload(request, imageId):
    # delete the image
    uploadedImage = get_object_or_404(ImageAsset, pk=imageId)

    # get the name of the image
    imageName = uploadedImage.imageName

    # delete
    uploadedImage.delete()

    # alert deletion success
    messages.success(request, f"The file '{imageName}' was deleted successfully!")

    return redirect("messenger:file-manager")


@login_required(login_url='messenger:home')
@user_passes_test(isAdmin)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deleteSpecificService(request, serviceId):
    # get the service
    serviceToDelete = get_object_or_404(OfferedService, pk=serviceId)

    # get the name of the service
    deletedServiceName = serviceToDelete.serviceName

    # delete
    serviceToDelete.delete()

    # alert deletion success
    messages.success(request, f"The service '{deletedServiceName}' was deleted successfully!")

    return redirect("admin_panel:admin-home")

@login_required(login_url='messenger:home')
@user_passes_test(isAdmin)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deleteSpecificVenue(request, venueId):
    # get the venue
    venueToDelete = get_object_or_404(VenueItem, pk=venueId)

    # get the name of the venue to delete
    deletedVenueName = venueToDelete.venueName

    # delete
    venueToDelete.delete()

    # alert deletion success
    messages.success(request, f"The Venue '{deletedVenueName}' was deleted successfully!")

    return redirect("admin_panel:admin-home")

@login_required(login_url='messenger:home')
@user_passes_test(isAdmin)
def deleteSpecificTestimonial(request, testimonialId):
    # get the instance
    testimonialToDelete = get_object_or_404(Testimonial, pk=testimonialId)

    # get the name of the instance
    deletedTestimonialName = testimonialToDelete.guestName

    # delete
    testimonialToDelete.delete()

    # alert deletion success
    messages.success(request, f"The Testimonial for '{deletedTestimonialName}' was deleted successfully!")

    return redirect("admin_panel:admin-home")

@login_required(login_url='messenger:home')
@user_passes_test(isAdmin)
def deleteSpecificReply(request, replyId):
    # get the instance
    replyToDelete = get_object_or_404(EmailReplies, pk=replyId)

    # delete the reply
    replyToDelete.delete()

    # alert deletion success
    messages.success(request, f"The Reply was deleted successfully!")

    return redirect("messenger:email-page")

@login_required(login_url='messenger:home')
@user_passes_test(isAdmin)
def deleteVendorPage(request, pageId):
    # get the instance
    pageToDelete = get_object_or_404(VendorPage, pk=pageId)

    # delete the page
    pageToDelete.delete()

    # alert deletion success
    messages.success(request, f"The Page was deleted successfully!")

    return redirect("messenger:page-registry")

@login_required(login_url='messenger:home')
@user_passes_test(isAdmin)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewPageRegistry(request):
    pageContext = {
        'present_categories': PageTools().getPageCategories(),
        'present_pages': PageTools().getPresentPages(),
        'district_list': HelperUtils().getCountryList(),
        'uploads': ControlUtils().getUploadsData()

    }

    return render(request, "mariadmin/sections/page-registry.html", context=pageContext)

@login_required(login_url='messenger:home')
@user_passes_test(isAdmin)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def galleryControlPanel(request):
    pageContext = {
        'all_uploads': ControlUtils().getUploadsData()

    }

    return render(request, "mariadmin/sections/gallery-control.html", context=pageContext)

@login_required(login_url='messenger:home')
@user_passes_test(isAdmin)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def updateGalleryImageState(request):
    # get the id
    imageObjectId = request.POST['gallery-image-id']

    imageState = True if request.POST['featured-state'] == 'true' else False

    # get the selected object
    selectedImageItem = get_object_or_404(ImageAsset, pk=int(imageObjectId))

    # update its state
    selectedImageItem.isGalleryItem = imageState

    # save the changes
    selectedImageItem.save()


    return JsonResponse(dict(
        info = 'updated'
    ))

@login_required(login_url='messenger:home')
@user_passes_test(isAdmin)
def deleteSpecificContact(request, contactId, whoseContact):
    # get the instance
    if whoseContact == 1:
        contactToDelete = get_object_or_404(Contacts, pk=contactId)

    else:
        contactToDelete = get_object_or_404(EventsServicesContacts, pk=contactId)

    # get the type of the deleted contact
    deletedContactType = contactToDelete.contactType

    # delete the contact
    contactToDelete.delete()

    # type
    whoseMessage = "Mariahill Gardens" if whoseContact == 1 else "Events Services"

    # alert deletion success
    messages.success(request, f" '{deletedContactType}' Contact For {whoseMessage}  was deleted successfully!")

    return redirect("admin_panel:admin-home")

@login_required(login_url='messenger:home')
@user_passes_test(isAdmin)
def deletePostComments(request, postId):
    PostsManager(request=request).deleteAllPostComments(postId=postId)

    return redirect("messenger:blog-editor")

@login_required(login_url='messenger:home')
def deleteChatsForGivenUser(request, userName):
    # get the object
    entryObject = MessageEntryNames.objects.filter(UserName=userName).first()

    if entryObject:
        # delete the entry
        entryObject.delete()

        # delete the associate chats
        ChatUtilities(request=request).wipeAllChats(userName=userName)

    else:
        # pass
        messages.error(request, "You have no chats yet!")

    # print("To be deleted:", userName)

    return redirect("userenv:useraccount")




@login_required(login_url='messenger:home')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(isAdmin)
def fileManagerPage(request):
    if request.method == "POST":
        # file
        uploadedFile = request.FILES['file-to-upload']

        # get the file name
        fileName = uploadedFile.name

        # check and see if the file is a duplicate
        notDuplicate = True if not ImageAsset.objects.filter(imageName=fileName).first() else False

        if notDuplicate is True:
            # get the file size
            fileSize = uploadedFile.size
            # "/media/assets/" + 

            # save the file
            ControlUtils().saveNewFileUpload(
                imageName=fileName,
                imageSize=fileSize,
                imageData=uploadedFile
                )

            # success
            messages.success(request, "File Uploaded Successfully!")

        else:
            messages.error(request, "File Already Exists.., Try deleting it maybe!")


        return redirect("messenger:file-manager")

    else:
        # print("reached here")
        
        # get the data
        uploadsContext = {
            'uploads': ControlUtils().getUploadsData()
        }

        return render(request, "mariadmin/sections/upload-section.html", context=uploadsContext)


@login_required(login_url='messenger:home')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(isAdmin)
def manageNextOfKins(request):
    pageContext = {
        'admins_present': AdminTools().getPresentAdminsCatalog()
    }

    # print(pageContext)

    # print("data:", request.session['allowed_pages'])

    return render(request, "mariadmin/sections/user-access.html", context=pageContext)

@login_required(login_url='messenger:home')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(isAdmin)
def ripOffAdmin(request, adminId):
    # delete the admin
    deletedAdminName = AdminTools().deleteGivenAdminProfile(adminId=adminId)

    # alert
    messages.success(request, f"The admin '{deletedAdminName}' was deleted successfully!")

    return redirect("messenger:next-of-kins")

@login_required(login_url='messenger:home')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(isAdmin)
def fetchAdminDetail(request):
    adminId = request.POST['admin-id']

    # get the admin details
    adminDetail = AdminTools().getAdminDetail(adminId=adminId)

    return JsonResponse(
        dict(
            info = adminDetail
        )
    )

@login_required(login_url='messenger:home')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(isAdmin)
def changeAdminPermissions(request):
    # modify permissions
    AdminUtilities(request=request).alterAdminPermissions()

    return redirect("messenger:next-of-kins")



@login_required(login_url='messenger:home')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def submitAdminReply(request):
    # get the submitted data
    submittedData = request.POST.dict()

    # submit the reply
    submittedEmail = submittedData['user-email']

    submittedReply = submittedData['reply-message'].capitalize()


    # perform the email sending
    MessengerUtils().resetCoreEngine(
        receiverEmail=submittedEmail,
        emailSubject="REPLY FROM MARIAHILL",
        messageToSend=submittedReply

    )


    # get the email holder
    associatedHolder = EmailHolders.objects.filter(userEmail=submittedEmail).first()

    # create the reply
    createdReplyObject = EmailReplies.objects.create(
        associatedHolder=associatedHolder,
        replyMessage=submittedReply
        )

    # save the object
    createdReplyObject.save()


    # alert success
    messages.success(request, f"Reply to {submittedEmail} was sent successfully!")

    return redirect("messenger:email-page")

@login_required(login_url='messenger:home')
def getMessageThreadData(request):
    threadRequest = request.POST.dict()

    submittedUserEmail = threadRequest['user-email']

    # get the user data
    presentData = CommUtilities().getMessagesFromEmail(emailAddress=submittedUserEmail)

    # print(presentData)

    return JsonResponse(dict(
        info = presentData
    ))


@login_required(login_url='messenger:home')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(isAdmin)
def fetchPageMeta(request):
    # get the meta information
    pageMetaInformation = PageManager(request=request).fetchPageMeta()

    return JsonResponse(
        dict(
            info = pageMetaInformation
            )
        )

@login_required(login_url='messenger:home')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(isAdmin)
def manageThirdPartyPage(request, pageId):
    # test out page id
    isPagePresent = VendorPage.objects.filter(pk=pageId).first()

    if isPagePresent:
        pass

    else:
        # redirect to the registry
        return redirect("messenger:page-registry")

    # prepare the context
    pageContext = {
        'page_id': pageId,
        'details': PageTools().getPageDetails(pageId=pageId),
        'handles': PageTools().getSocialHandles(pageId=pageId),
        'uploads': ControlUtils().getUploadsData(),
        'present_services': PageTools().getPageServices(pageId=pageId)

    }

    return render(request, "mariadmin/sections/page-manage.html", context=pageContext)

@login_required(login_url='messenger:home')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(isAdmin)
def savePageDetails(request):
    # extract the id of the vendor page
    pageId = request.POST['page-id']

    # save the page details
    PageManager(request=request).writePageDetails(pageId=pageId)

    return redirect("messenger:manage-vendor-page", pageId=pageId)

@login_required(login_url='messenger:home')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(isAdmin)
def savePageHandles(request):
    # extract the page id
    pageId = request.POST['page-id']

    # save the page handles
    PageManager(request=request).saveSocialMediaInformation()

    return redirect("messenger:manage-vendor-page", pageId=pageId)


@login_required(login_url='messenger:home')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(isAdmin)
def savePageServices(request):
    # extract the page id
    pageId = request.POST['page-id']

    # save the page handles
    PageManager(request=request).savePageServiceDetail(pageId=pageId)

    return redirect("messenger:manage-vendor-page", pageId=pageId)

@login_required(login_url='messenger:home')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(isAdmin)
def wipePageService(request, serviceId):
    # delete
    serviceName, pageId = PageTools().deleteServiceWithId(serviceId=serviceId)

    # alert
    messages.success(request, f"The service '{serviceName}' was successfully deleted")

    return redirect("messenger:manage-vendor-page", pageId=pageId)

@login_required(login_url='messenger:home')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(isAdmin)
def fetchServiceInformation(request):
    # get the service
    serviceId = request.POST['service-id']

    # get the details
    serviceDetails = PageTools().getServiceMeta(serviceId=serviceId)

    return JsonResponse(
        dict(
            info = serviceDetails
        )
    )


def writeMailMessageData(submittedUserName, submittedUserEmail, submittedMessageSubject, submittedActualMessage):
    # create the message
    newSimpleMessage = SimpleContactMessages.objects.create(
        UserName=submittedUserName,
        UserEmail=submittedUserEmail,
        UserSubject=submittedMessageSubject,
        UserMessage=submittedActualMessage)

    # save the message
    newSimpleMessage.save()

    # record entry
    isPresent = EmailHolders.objects.filter(userEmail=submittedUserEmail).first()

    if isPresent:
        # skip
        pass
    else:
        # create new entry
        newHolderEntry = EmailHolders.objects.create(userEmail=submittedUserEmail)

        # save
        newHolderEntry.save()

        # print("Added new entry")

    return


def submitSimpleMessage(request):
    # get the request
    messageRequest = request.POST.dict()

    submittedUserName = messageRequest['user-name'].title()

    submittedUserEmail = messageRequest['user-email']


    submittedMessageSubject = messageRequest['message-subject'].upper()

    submittedActualMessage = messageRequest['actual-message'].capitalize()

    # send the message
    writeMailMessageData(
        submittedUserName=submittedUserName,
        submittedUserEmail=submittedUserEmail,
        submittedMessageSubject=submittedMessageSubject,
        submittedActualMessage=submittedActualMessage)


    # alert saving
    messages.success(request, "The message was submitted successfully!")

    return redirect("messenger:contact")




@login_required(login_url='messenger:home')
def getNewUserChats(request):
    # get the request
    fetchRequest = request.POST.dict()

    submittedUserName = fetchRequest['user-name']

    associatedEmail = User.objects.filter(username=submittedUserName).first().email

    # get chats
    extractedChatData = CommUtilities().getChatsOfUser(userName=submittedUserName)

    # get the avatar
    userAvatar = CommUtilities().getUserAvatar(userName=submittedUserName)

    # prepare response
    responseMessage = {
            'name': submittedUserName,
            'email': associatedEmail,
            'avatar': "missing" if userAvatar  is None else userAvatar,
            'chats': extractedChatData,
            'initials': submittedUserName.split(" ")[0][0].upper()

        }

    # print(responseMessage)

    return JsonResponse(
        dict(
            message = responseMessage
        )
    )

@login_required(login_url='messenger:home')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(isAdmin)
def blogEditorPage(request):
    # [{'date': '07-09-2023', 'featured': False, 'id': 1}]
    pageContext = {
        'present_post_categories': PostTools().getPostCategories(),
        'uploads': ControlUtils().getUploadsData(),
        'post_previews': PostTools().getPostMetaPreview()
    }

    # print(PostTools().getPostMetaPreview())

    return render(request, "mariadmin/sections/blog-editor.html", context=pageContext)


@login_required(login_url='messenger:home')
@user_passes_test(isAdmin)
def getPostInformation(request):
    # debug point
    # print("Received:", request.POST.dict())

    # get the post information
    postData = PostsManager(request=request).postMetaApi()

    return JsonResponse(
        dict(
            info = postData
        )
    )

@login_required(login_url='messenger:home')
@user_passes_test(isAdmin)
def deleteSpecificPostCategory(request, postCategoryId):
    # delete the post
    PostsManager(request=request).deletePostCategory(categoryId=postCategoryId)

    return redirect("messenger:blog-editor")

@login_required(login_url='messenger:home')
@user_passes_test(isAdmin)
def deleteSpecificPostItem(request, postItemId):
    # delete the post
    PostsManager(request=request).deletePostItem(postItemId=postItemId)

    return redirect("messenger:blog-editor")


@login_required(login_url='messenger:home')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(isAdmin)
def chatPage(request):
    # get initial chat
    initialUserName, initialUserEmail, initialUserChats = CommUtilities().getInitialChat()

    initialChat =  {
            'name': initialUserName,
            'email': initialUserEmail,
            'avatar': CommUtilities().getUserAvatar(userName=initialUserName),
            'chats': initialUserChats,
            'initials': initialUserName.split(" ")[0][0].upper()

        } if not initialUserName is None else None

    # print('email:', initialUserEmail)

    # print('chats:', len(initialUserChats))

    pageContext = {
        'available_contacts': CommUtilities().getAvailableContacts(),
        'available_chats': CommUtilities().getAvailableContactInfoOnChatUsers(),
        'initial_chat': initialChat

    }

    return render(request, "mariadmin/sections/chat-section.html", context=pageContext)

@login_required(login_url='messenger:home')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(isAdmin)
def emailPage(request):
    # get the emails
    presentEmails = CommUtilities().getAllPresentEmails()

    pageContext = {
        'preview_inbox': presentEmails,
        'count': CommUtilities().getInboxCount(),
        'users': len(presentEmails),
        'present_replies': CommUtilities().getPresentReplies()
    }

    return render(request, "mariadmin/sections/email-section.html", context=pageContext)


@login_required(login_url='messenger:home')
def submitChatMessage(request, userGroup):

    # print('Received:', request.POST.dict(), 'Who:', request.user.username)
    ChatUtilities(request=request).recordSubmittedMessage(userGroup=userGroup)

    return JsonResponse(
        dict(
            message = 'received'
        )
    )


def cardsImageAlertManager(request:HttpRequest, whatCard):
    displayMessageTag = SectionUtils(request=request).cardsImageProcessor(whatCard)

    if displayMessageTag is True:
        # card name
        cardName = "Left Card" if whatCard == 1 else "Right Card"

        messages.success(request, f"{cardName} Image updated successfully!")

    else:
        # determine the message to display
        displayMessage = "Please create a heading and text first before adding an image" if displayMessageTag is False else "Please select a valid image address using the image selector!"

        messages.warning(request, displayMessage)

    return

@login_required(login_url='messenger:home')
def updateVenueFeaturedStatus(request):
    # make the update
    SectionUtils(request=request).updateVenueState()

    return JsonResponse(dict(
        message = 'received'
    ))

@login_required(login_url='messenger:home')
def updatePostFeaturedState(request):
    # make the update
    PostsManager(request=request).updatePostItemState()

    return JsonResponse(dict(
        message = 'received'
    ))

@login_required(login_url='messenger:home')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def makeWebsiteEdit(request, sectionId):
    if sectionId == 1:
        # save the heading
        SectionUtils(request=request).processHeading()

        messages.success(request, "Heading updated successfully!")

        return redirect("admin_panel:admin-home")

    elif sectionId == 2:
        # save the heading
        SectionUtils(request=request).processAboutDetails()

        messages.success(request, "About details where updated successfully!")

        return redirect("admin_panel:admin-home")

    elif sectionId == 3 or sectionId == 5:
        # determine what card code
        whatCard = (1 if sectionId == 3 else 2)

        # card name
        cardName = "Left" if sectionId == 3 else "Right"

        # save the heading
        SectionUtils(request=request).cardsMetaProcessor(whatCard=whatCard)

        messages.success(request, f"{cardName} Card heading and text updated successfully!")

        return redirect("admin_panel:admin-home")

    elif sectionId == 4 or sectionId == 6:
        # determine the processing code
        processingCode = (1 if sectionId == 4 else 2)

        cardsImageAlertManager(request=request, whatCard=processingCode)

        return redirect("admin_panel:admin-home")

    elif sectionId == 7:
        # save the details
        notDuplicate = SectionUtils(request=request).processService()

        if notDuplicate is True:
            messages.success(request, f"Service name and details saved successfully!")

        else:
            messages.success(request, f"The service already exists, maybe delete it first!")

        return redirect("admin_panel:admin-home")

    elif sectionId == 8:
        # save the ribbon data
        SectionUtils(request=request).processRibbonDetails()

        # alert success
        messages.success(request, f"The ribbon details were updated successfully!")

        return redirect("admin_panel:admin-home")

    elif sectionId == 9:
        # save venue
        isVenueDuplicate, venueName = SectionUtils(request=request).processVenueData()

        displayMessage = f"The venue name {venueName} already exists maybe delete it first!" if isVenueDuplicate else f"The venue {venueName} was saved successfully!"

        # alert success or error
        if isVenueDuplicate is True:
            messages.warning(request, displayMessage)
        else:
            messages.success(request, displayMessage)

        return redirect("admin_panel:admin-home")

    elif sectionId == 10:
        # check for duplicates
        isTestimonialDuplicate, guestName = SectionUtils(request=request).processTestimonial()

        if isTestimonialDuplicate is True:
            messages.warning(request, "Testimonial exists already, maybe delete it first!")

        else:
            messages.success(request, f"The Testimonial for {guestName} was saved successfully!")

        return redirect("admin_panel:admin-home")

    elif sectionId == 11:
        # save the data
        SectionUtils(request=request).processStatisticsData()

        # alert success
        messages.success(request, "The provided statistics were saved successfully!")

        return redirect("admin_panel:admin-home")

    # 12
    elif sectionId == 12:
        #  save the contact data
        contactIsNew, whoseContacts = SectionUtils(request=request).processContactData()

        # contact type
        contactKind = "Mariahill Gardens" if whoseContacts == 1 else "Events Services"

        # message
        displayMessage =f"The Contact for '{contactKind}' was saved successfully!" if contactIsNew is True else "The Contact was updated successfully!"

        # alert success
        messages.success(request, displayMessage)


        return redirect("admin_panel:admin-home")

    elif sectionId == 13:
        # process the post data
        PostsManager(request=request).saveCategoryInformation()

        return redirect("messenger:blog-editor")

    elif sectionId == 14:
        # save the post
        PostsManager(request=request).savePostItem()

        return redirect("messenger:blog-editor")

    elif sectionId == 15:
        # save the image
        SectionUtils(request=request).processWebsiteHeadingImage()

        return redirect("admin_panel:admin-home")

    elif sectionId == 16:
        # save the video
        SectionUtils(request=request).processGardensTourVideoLink()

        return redirect("admin_panel:admin-home")
    
    elif sectionId == 17:
        # save the about image
        SectionUtils(request=request).processAboutImage()

        return redirect("admin_panel:admin-home")



@login_required(login_url='messenger:home')
@user_passes_test(isAdmin)
def registerPageCategory(request):
    PageManager(request=request).savePageCategoryInformation()

    return redirect("messenger:page-registry")

@login_required(login_url='messenger:home')
@user_passes_test(isAdmin)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletePageCategory(request, categoryId):
    # get the category
    categoryToDelete = get_object_or_404(PageCategory, pk=categoryId)

    # get the name of the category
    deletedCategoryName = categoryToDelete.categoryName

    # delete
    categoryToDelete.delete()

    # alert deletion success
    messages.success(request, f"The Page Category '{deletedCategoryName}' was deleted successfully!")

    return redirect("messenger:page-registry")

@login_required(login_url='messenger:home')
@user_passes_test(isAdmin)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def recordNewVendorPage(request):
    # save the page data
    PageManager(request=request).saveNewVendorPage()

    return redirect("messenger:page-registry")


def viewVendorPage(request, vendorPageName):
    # debug
    isPagePresent = VendorPage.objects.filter(pageName=vendorPageName).first()

    # print("State:", vendorPageName)

    if isPagePresent and isPagePresent.isVisible is True:
        # get the page details
        isValid, pageContext = PageTools().getVendorPageDetails(vendorPage=isPagePresent)

        if isValid is True:
            pass

        else:
            # goto home page
            return redirect("messenger:welcome")


        return render(request, "mariadmin/vendors/vendor-base.html", context=pageContext)

    else:
        # redirect to home page
        return redirect("messenger:welcome")


@login_required(login_url='messenger:home')
@user_passes_test(isAdmin)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def registerNewAdmin(request):
    # record the admin
    AdminUtilities(request=request).registerNewAdmin()

    return redirect("messenger:next-of-kins")

@login_required(login_url='messenger:home')
@user_passes_test(isAdmin)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def giveSecondaryAdminAccess(request, idOfAdmin):
    # grant access
    grantStatus, adminUserName = AdminUtilities(request=request).grantAdminLoginAccess(idOfAdmin=idOfAdmin)

    if grantStatus is True:
        messages.success(request, f"'{adminUserName}' was granted login access successfully! 😊")

    else:
        messages.error(request, f"'{adminUserName}' cant be granted access without any permissions, first assign atleast one 😌")


    return redirect("messenger:next-of-kins")

@login_required(login_url='messenger:home')
@user_passes_test(isAdmin)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def managePrimaryCredentials(request):
    # make the alter
    AdminUtilities(request=request).alterAdminPassword()


    return redirect("messenger:next-of-kins")

@login_required(login_url='messenger:home')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def updateUserCredentials(request):
    # alter the passwords
    AdminUtilities(request=request).alterUserPassword()

    return redirect("userenv:useraccount")


@login_required(login_url='messenger:home')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def updateUserAvatar(request):
    # get teh submitted data
    avatarRequest = request.POST.dict()

    # user avatar
    submittedAvatarUrl = avatarRequest['selected-image-avatar']

    # user id
    userId = avatarRequest['user-id-tag']

    # make the update
    CommUtilities().updateUserAvatar(userId=userId, imageUrl=submittedAvatarUrl, request=request)


    # debug
    # print("User Id:", userId)

    # print("Avatar:", submittedAvatarUrl)

    # alert
    messages.success(request, f" Hey '{request.user.username}' , your profileimage was updated successfully! 😊")

    return redirect("userenv:useraccount")


@login_required(login_url='messenger:home')
@user_passes_test(isAdmin)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def saveVenueImage(request):
    # save
    VenueUtilities(request=request).saveVenueImage()

    return redirect("admin_panel:admin-home")

@login_required(login_url='messenger:home')
@user_passes_test(isAdmin)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def findVenueImages(request):
    venueId = request.POST['venue-id']

    # get the images
    venueImages = VenueTools().getAllVenueImages(venueId=int(venueId))

    return JsonResponse(
        dict(
            info = venueImages
        )
    )

@login_required(login_url='messenger:home')
@user_passes_test(isAdmin)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deleteVenueImage(request):
    # get id
    venueImageId = request.POST['venue-image-id']

    # delete the image
    VenueTools().deleteVenueImage(venueImageId=int(venueImageId))

    return JsonResponse(
        dict(
            message = 'wiped'
        )
    )


@login_required(login_url='messenger:home')
@user_passes_test(isAdmin)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def recordBookingFormDetail(request):
    # request data
    requestData = request.POST.dict()

    # get the object
    submittedFormImage = requestData['side-image-url']

    if submittedFormImage.endswith(".jpg") or submittedFormImage.endswith(".png") or submittedFormImage.endswith(".jpeg"):
        # get the form text
        submittedFormText = requestData['form-display-message']

        # get the object
        presentObject = BookingFormDetail.objects.all().first()

        if presentObject:
            # use present
            pass
        else:
            # create new
            presentObject = BookingFormDetail.objects.create()

        # add the details
        presentObject.formText =  submittedFormText

        presentObject.imageUrl = submittedFormImage

        # save the detail
        presentObject.save()

        messages.success(request, "The Booking form detail was updated successfully! 😊")


    else:
        # alert
        messages.error(request, "Plesase use the image selector button to select and image!")


    return redirect("admin_panel:admin-home")


@login_required(login_url='messenger:home')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deactivateUserAccount(request):
    # get the users details
    usersObject = request.user
    
    emailAddress, userName = usersObject.email, usersObject.username
    
    # print("data:", emailAddress, " ", userName)
    # delete any conversations
    CommUtilities().deleteMessageThread(userName=userName, userEmail=emailAddress)
    
    # delete message flows if its a regular user
    if usersObject.is_superuser is False:
        ProcessingUtilities().deleteAllMessageForUser(userName=userName)
        
    else:
        pass
    
    # delete the user object
    usersObject.delete()
    
    # alert success
    messages.success(request, "We are in grief to see you go.. 😥")

    return redirect("userenv:useraccount")
    


