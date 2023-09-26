from django.http import HttpRequest

from django.db.models import Q

from django.contrib import messages

from mariadmin.models import (
    AboutHeading, AboutDetails, LeftCard, RightCard, OfferedService, 
    MiddleGrid, VenueItem, Testimonial, 
    StatisticsMeta, Contacts, MessageFlow, MessageEntryNames, WebsiteHeadingImage, gardensTourVideoLink,
    EventsServicesContacts, AboutImage
    )



class ChatUtilities:
    def __init__(self, request:HttpRequest):
        self.chatMessageRequest = request
        
    def wipeAllChats(self, userName):
        # get the all related object
        lookUpQuery = Q(fromToMeta__icontains=userName)
        
        # get all objects
        allRelatedChats = MessageFlow.objects.filter(lookUpQuery)
        
        if allRelatedChats:
            # delete all
            allRelatedChats.delete()
            
        else:
            # no chats
            pass

        return        
        
        
    def recordSubmittedMessage(self, userGroup):
        # get the data
        submittedData = self.chatMessageRequest.POST.dict()
        
        
        # get the sender
        if userGroup == 1:
            messageReceiver = submittedData['receiver']
            
            fromToMeta = f"admin>>>{messageReceiver}"
                        
        else:
            messageSender = self.chatMessageRequest.user.username
            
            fromToMeta = f"{messageSender}>>>admin"
            
            # alert that user holds entry
            messageEntryObject = MessageEntryNames.objects.filter(UserName=messageSender).first()
            
            if messageEntryObject:
                pass
            
            else:
                # create the entry
                newEntry = MessageEntryNames.objects.create(UserName=messageSender)
                
                # save it
                newEntry.save()
                
                # debug
                # print("Entry created")
                
        # get the sent message
        messageMeta = submittedData['message']

        # record the message
        newMessageObject = MessageFlow.objects.create(
            fromToMeta=fromToMeta,
            messageMeta=messageMeta
        )
        
        # save the message that was sent
        newMessageObject.save()
        
        
        # debug
        # print("message received!")
        
        return
        


class ExistenceCheck:
    def __init__(self):
        pass
    
    def validateCardPresence(self, whatCard):
        if whatCard == 1:
            # check if the card already exists
            allCards = LeftCard.objects.all()
            
        else:
            allCards = RightCard.objects.all()
            
        # determine presence of the card
        cardPresence = allCards.first() if allCards.first() else False
        
        return cardPresence
    
    
        

class SectionUtils:
    def __init__(self, request:HttpRequest):
        self.submissionRequest = request
        
    
    def processAboutImage(self):
        submittedData = self.submissionRequest.POST.dict()
        
        # get the image url
        submittedImageUrl = submittedData['about-image-url']
        
        if submittedImageUrl.endswith(".jpg") or submittedImageUrl.endswith(".png") or submittedImageUrl.endswith(".jpeg"):
            pass
        
        else:
            # alert 
            messages.error(self.submissionRequest, "Please select an image, then a valid image path will be provided 😌")
            
            return
        
        aboutImageInstance = AboutImage.objects.all().first()
        
        if aboutImageInstance:
            # update if present
            aboutImageInstance.aboutImageUrl = submittedImageUrl
            
        else:
            # create a new entry
            aboutImageInstance = AboutImage.objects.create(
                aboutImageUrl=submittedImageUrl
            )
            
        # save the contact
        aboutImageInstance.save()
        
        messages.success(self.submissionRequest, "The About Image was updated successfully! 🥳")

        return 
        
    
    def processGardensTourVideoLink(self):
        submittedData = self.submissionRequest.POST.dict()
        
        # get the video url
        submittedVideoSource = submittedData['video-link-url']
        
        tourVideoLinkInstance = gardensTourVideoLink.objects.all().first()
        
        if tourVideoLinkInstance:
            # update
            tourVideoLinkInstance.videoUrl = submittedVideoSource
            
        else:
            # create a new entry
            tourVideoLinkInstance = gardensTourVideoLink.objects.create(
                videoUrl=submittedVideoSource
            )
            
        # save the contact
        tourVideoLinkInstance.save()
        
        messages.success(self.submissionRequest, "The Gardens Tour Video Link was updated successfully! 🥳")

        return 

        
    def processWebsiteHeadingImage(self):
        submittedData = self.submissionRequest.POST.dict()
        
        # get the image url
        submittedImageUrl = submittedData['header-image-url']
        
        if submittedImageUrl.endswith(".jpg") or submittedImageUrl.endswith(".png") or submittedImageUrl.endswith(".jpeg"):
            pass
        
        else:
            # alert 
            messages.error(self.submissionRequest, "Please select an image, then a valid image path will be provided 😌")
            
            return
        
        headingImageInstance = WebsiteHeadingImage.objects.all().first()
        
        if headingImageInstance:
            # update
            headingImageInstance.imageUrl = submittedImageUrl
            
        else:
            # create a new entry
            headingImageInstance = WebsiteHeadingImage.objects.create(
                imageUrl=submittedImageUrl
            )
            
        # save the contact
        headingImageInstance.save()
        
        messages.success(self.submissionRequest, "Header Image was updated successfully! 🥳")

        return 
        
    
    def processContactData(self):
        submittedData = self.submissionRequest.POST.dict()
        
        # get the values
        contactType = submittedData['contact-type']
        
        contactValue = submittedData['contact-value']
        
        whoseContact = int(submittedData['whose-contacts'])
        
        if whoseContact == 1:
            contactInstance = Contacts.objects.filter(contactType=contactType).first()
            
        else:
            contactInstance = EventsServicesContacts.objects.filter(contactType=contactType).first()
        
        if contactInstance:
            # update
            contactInstance.contactValue = contactValue
            
        else:
            # create a new one
            if whoseContact == 1:
                contactInstance = Contacts.objects.create(
                    contactType=contactType,
                    contactValue=contactValue)
            else:
                contactInstance = EventsServicesContacts.objects.create(
                        contactType=contactType,
                        contactValue=contactValue)
        # save the contact
        contactInstance.save()
        
        # new or updated
        isNew = True if contactInstance is None else False
        
        return isNew, whoseContact


    
    def processStatisticsData(self):
        submittedData = self.submissionRequest.POST.dict()
        
        # get the values
        happyGuests = int(submittedData['happy-guests'])
        
        hostedEvents = int(submittedData['events-hosted'])
        
        staffCount = int(submittedData['staff-count'])
        
        venueCount = int(submittedData['venues-count'])
        
        presentStatistics = StatisticsMeta.objects.all().first()
        
        if presentStatistics:
            presentStatistics.happyGuests = happyGuests
            
            presentStatistics.hostedEvents = hostedEvents
            
            presentStatistics.staffCount = staffCount
            
            presentStatistics.venueCount = venueCount
            
            
            
        else:
            presentStatistics = StatisticsMeta.objects.create(
                happyGuests=happyGuests,
                hostedEvents=hostedEvents,
                staffCount=staffCount,
                venueCount=venueCount
                )
            
        # save 
        presentStatistics.save()
        
        return
        
    
    def processTestimonial(self):
        submittedData = self.submissionRequest.POST.dict()
        
        guestName = submittedData['guest-name'].title()
        
        # check for duplicates
        isDuplicate = True if Testimonial.objects.filter(guestName=guestName).first() else False
        
        if isDuplicate is False:
            guestPosition = submittedData['guest-position'].upper()
            
            guestComment = submittedData['guest-comment'].capitalize()
            
            guestImageUrl = submittedData['guest-avatar']
            
            # save load the data
            newTestimonial = Testimonial.objects.create()
            
            newTestimonial.guestName = guestName
            
            newTestimonial.guestPosition = guestPosition
            
            newTestimonial.guestComment = guestComment
            
            newTestimonial.guestImageUrl = guestImageUrl
            
            # save
            newTestimonial.save()
            
            
        else:
            pass
        
        return isDuplicate, guestName
        
        
    
    def updateVenueState(self):
        submittedData = self.submissionRequest.POST.dict()
        
        # cast the venue id to integer
        venueId = int(submittedData['venue-id'])
        
        venueState = True if submittedData['featured-state'] == 'true' else False
        
        # get the selected object
        selectedVenue = VenueItem.objects.get(pk=venueId)
        
        # update its state
        selectedVenue.isFeatured = venueState
        
        # save the changes
        selectedVenue.save()
        
        return
        
    
    def processVenueData(self):
        submittedData = self.submissionRequest.POST.dict()
                
        # print("submitted:", selectedCategories)
        
        # # validate duplicates
        venueName = submittedData['venue-name'].title()
        
        isDuplicate = True if VenueItem.objects.filter(venueName=venueName).first() else False
        
        if isDuplicate is False:
            # get the rest of the data
            venueDescription = submittedData['venue-description'].capitalize()
            
            venueCapacity = submittedData['venue-capacity']
            
            isFeatured = False
            
            # get category info
            selectedCategories = [infoEntry for infoEntry, infoValue in submittedData.items() if infoValue == 'on']
            
            # print("Available:", selectedCategories)
            
            # create new venue
            newVenue = VenueItem.objects.create(isFeatured=isFeatured)
            
            # load venue details
            newVenue.venueName = venueName
            
            newVenue.venueDescription = venueDescription
            
            
            newVenue.venueCapacity = venueCapacity
            
            # store the category along
            if len(selectedCategories) > 0:
                newVenue.venueCategory = '|||'.join(selectedCategories)
                
                # print("Gave category")
                
            else:
                # a default value of social events is given
                # print("Did not give category")
                pass
            
            # save the venue
            newVenue.save()
            
        else:
            pass
        
        return isDuplicate, venueName
        
        
        
        
    
    def processRibbonDetails(self):
        submittedData = self.submissionRequest.POST.dict()
        
        # get the details
        ribbonHeading = submittedData['ribbon-heading'].upper()
        
        ribbonMessage = submittedData['ribbon-message'].capitalize()
        
        ribbonButtonText= submittedData['ribbon-button'].upper()
        
        ribbonUrl = submittedData['ribbon-url']
        
        # get present instances
        ribbonInstance = MiddleGrid.objects.all().first()
        
        if ribbonInstance:
            pass
        
        else:
            # create a new one
            ribbonInstance = MiddleGrid.objects.create()
            
        # make the updates
        ribbonInstance.gridTitle = ribbonHeading
        
        ribbonInstance.gridMessage = ribbonMessage
        
        ribbonInstance.gridRedirectionUrl = ribbonUrl
        
        ribbonInstance.gridButtonText = ribbonButtonText
        
        # save the instance
        ribbonInstance.save()
        
        return
        
        
        
        
    
    def processService(self):
        submittedData = self.submissionRequest.POST.dict()
        
        # get the name and the details
        serviceName = submittedData['service-name'].title()
        
        # validate for duplication
        notDuplicate = True if not OfferedService.objects.filter(serviceName=serviceName).first() else False
        
        if notDuplicate is True:
            serviceDetails = submittedData['service-details'].capitalize()
            
            # create the service
            newService = OfferedService.objects.create(
                serviceName=serviceName,
                serviceDetails=serviceDetails
                )
            
            newService.save()
            
        else:
            # alert
            pass
        
        return notDuplicate
        
        
        
    def cardsImageProcessor(self, whatCard):
        # image selector
        imageSelectorMap = {
            1: 'selected-left-image',
            2: 'selected-right-image'
        }
        
        # get the submitted data
        submittedData = self.submissionRequest.POST.dict()
        
        # get the appropriate selector
        imageSelectorSeed = imageSelectorMap[whatCard]
        
        # get the image url
        submittedImageUrl = submittedData[imageSelectorSeed]
        
        extensionValidation = submittedImageUrl.lower()
        
        if extensionValidation.endswith(".png") or extensionValidation.endswith(".jpeg") or extensionValidation.endswith(".jpg"):
            # proceed
            pass
        
        else:
            # alert
            return None
        
        
        presentCard = ExistenceCheck().validateCardPresence(whatCard=whatCard)
        
        if presentCard:
            # update the card image
            if whatCard == 1:
                presentCard.leftCardImageUrl = submittedImageUrl
                
            else:
                presentCard.rightCardImageUrl = submittedImageUrl
            
            # save the image
            presentCard.save()
            
            responseMessageCode = True
            
        else:
            responseMessageCode = False
            
        return responseMessageCode
        
        
    def cardsMetaProcessor(self, whatCard):
        # meta selector
        metaSelectorMap = {
            1: ('left-heading', 'left-text'),
            2: ('right-heading', 'right-text')
        }
        
        # get the submitted data
        submittedData = self.submissionRequest.POST.dict()
        
        # get the appropriate selector
        headingSelector, textSelector = metaSelectorMap[whatCard]
        
        # get the data        
        submittedCardHeading = submittedData[headingSelector].title()
        
        submittedCardText = submittedData[textSelector].capitalize()
        
        # check presence
        presentCard = ExistenceCheck().validateCardPresence(whatCard=whatCard)
        
        if presentCard:
            pass            
            
        else:
            presentCard = LeftCard.objects.create() if whatCard == 1 else RightCard.objects.create()
        
        # make an update
        if whatCard == 1:
            presentCard.leftCardHeading = submittedCardHeading
            
            presentCard.leftCardText = submittedCardText
            
        else:
            presentCard.rightCardHeading = submittedCardHeading
            
            presentCard.rightCardText = submittedCardText
        
        # update the card meta
        presentCard.save()
        
        return        
        
    
    def processAboutDetails(self):
        # get the submitted data
        submittedData = self.submissionRequest.POST.dict()
        
        submittedDetails = submittedData['about-details'].capitalize()
        
        # delete all the present
        AboutDetails.objects.all().delete()
        
        # print("heading:", submittedHeading)
        aboutDetailsInstance = AboutDetails.objects.create(aboutMore=submittedDetails)
        
        # save the heading to the database
        aboutDetailsInstance.save()

        return 
        
    
    def processHeading(self):
        # get the submitted data
        submittedData = self.submissionRequest.POST.dict()
        
        submittedHeading = submittedData['about-heading'].title()
        
        # delete all the present
        AboutHeading.objects.all().delete()
        
    
        # print("heading:", submittedHeading)
        headingInstance = AboutHeading.objects.create(headingName=submittedHeading)
        
        # save the heading to the database
        headingInstance.save()

        return 
        
        
        