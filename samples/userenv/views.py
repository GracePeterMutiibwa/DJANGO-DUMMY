from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required, user_passes_test

from django.views.decorators.cache import cache_control

from mariadmin.models import MessageFlow, WebsiteHeadingImage

from django.http import HttpRequest, JsonResponse

from django.db.models import Q

from django.contrib import messages

from messenger.bookings_engine import BookingUtilities, PaymentLinkUtils


def isAdmin(userInstance):
    return userInstance.is_authenticated and userInstance.is_superuser



class ProcessingUtilities:
    def getUserMessageFlows(self, userName):
        # get the lookup parameters
        parameterOne = f"admin>>>{userName}"
        
        parameterTwo = f"{userName}>>>admin"
        
        # create the lookup queries
        lookupQuery = Q(fromToMeta=parameterOne) | Q(fromToMeta=parameterTwo)
        
        # execute the query
        userMessageFlow = MessageFlow.objects.filter(lookupQuery)
        
        return userMessageFlow
    
    def deleteAllMessageForUser(self, userName):
        userMessageFlow = self.getUserMessageFlows(userName=userName)
        
        # delete
        if userMessageFlow:
            userMessageFlow.delete()
            
        else:
            pass
        
        return
            
    def getTheAvailableMessagesFlow(self, userName):
        # get the messages
        userMessageFlow = self.getUserMessageFlows(userName=userName)
        
        # results
        messageFlowData = [
            {
                'time': eachMessageObject.dateSent.strftime("%d-%m-%Y, %H:%M %p"),
                'message': eachMessageObject.messageMeta,
                'userGroup': 1 if (eachMessageObject.fromToMeta == f"admin>>>{userName}") else 2
            } for eachMessageObject in userMessageFlow
        ]
        
        return messageFlowData
        


@login_required(login_url="messenger:home")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def accountsHomePage(request):
    # context={'avatar': request.session['avatar']}
    
    if request.user.is_superuser:
        return redirect("admin_panel:admin-home")
    
    else:
        # get user messages
        loggedInUserName = request.user.username  
        
        # load initials
        if 'avatar' in request.session:
            # print('url:', request.session['avatar'])
            pass
        
        else:
            # add the initials
            userInitials = loggedInUserName.strip()[0].upper()
        
            request.session['initials'] = userInitials
        
        # get all messages
        availableMessages = ProcessingUtilities().getTheAvailableMessagesFlow(userName=loggedInUserName)
        
        bannerImage = WebsiteHeadingImage.objects.all().first()
        
        bookingRequests = BookingUtilities().getBookingRequestsOfClient(clientAddress=request.user.email)
        
        paymentLinkData = PaymentLinkUtils().getTransactionsOfClientViaEmail(clientEmail=request.user.email)
        
        pageContext = {
            'chat_messages': availableMessages,
            'banner_image': bannerImage.imageUrl if bannerImage else None,
            'event_categories': BookingUtilities().getEventsList(),
            'booking_requests': bookingRequests,
            'booking_size': len(bookingRequests),
            'payment_links': paymentLinkData,
            'links_size': len(paymentLinkData)
            
        }
        
        
        # print(bookingRequests)
        
        # print("Image:", request.session['avatar'])
        
        # chat-page.html
        return render(request, "mariadmin/profile-page.html", context=pageContext)
    


def preRequestRegisterRoutine(request:HttpRequest, dateObjects:tuple, timeObjects:tuple, eventDays:int):
    # user email address
    userEmail = request.user.email
    
    # dates
    fromDate, toDate = dateObjects
    
    # create a meta object from event times
    fromTime, toTime = timeObjects
    
    eventTimeMeta = f'{fromTime}-{toTime}'
    
    # validate duplicates
    isDuplicate = BookingUtilities().checkForDuplicateBookings(userEmail=userEmail, fromDate=fromDate, toDate=toDate, timeSlot=eventTimeMeta)
    
    if isDuplicate is True:
        # alert duplicates
        messages.error(request, "There exists a booking with the same details!")
    
    else:
        # get the rest of the details
        submittedBookingData = request.POST.dict()
        
        eventCategory = submittedBookingData['event-category']
        
        guestCount = int(submittedBookingData['guest-count'])
        
        eventDetails = submittedBookingData['other-details']
        
        # write the request
        BookingUtilities().saveNewBookingRequest(
            clientName=request.user.username.title(),
            clientEmail=request.user.email,
            eventDetails=eventDetails.capitalize(),
            startDate=fromDate,
            endDate=toDate,
            timeStamps=eventTimeMeta,
            daysOfUse=eventDays,
            eventCategory=eventCategory,
            guestNumber=guestCount
        )
        
        
        # alert success
        messages.error(request, "Your booking request was submitted successfully")
        
        print('User Name:', request.user.username.title())
        
        
    return


@login_required(login_url='messenger:home')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def registerNewBooking(request):
    # get the booking details
    submittedBookingData = request.POST.dict()
    
    # get the date object
    presentDateObject = submittedBookingData['event-date'].split('to')
    
    # check if only a single day was selected
    useVenueForOneDay = len(presentDateObject) == 1
    
    # get the date values
    if useVenueForOneDay is False:
        # different dates
        fromDate, toDate = [BookingUtilities().generateDateObjects(rawDateInfo=eachRawDate) for eachRawDate in presentDateObject]
        
    else:
        fromDate = BookingUtilities().generateDateObjects(rawDateInfo=presentDateObject[0])
        
        # same date for start and end
        toDate = fromDate
    
    # print('from:', fromDate, ' to:', toDate)
    
    datesInRange, daysForTheEvent = BookingUtilities().validateDateObjects(fromDate=fromDate, toDate=toDate)
    
    # print('In Range:', datesInRange, ' Days to Take:', daysForTheEvent)
    
    if datesInRange is True:
        # process the time periods
        fromTime = submittedBookingData['from-time']
        
        toTime = submittedBookingData['to-time']
        
        # print('from:', fromTime, ', To:', toTime)
        
        # validate the times
        areTimesValid, readableTime = BookingUtilities().validateEventTimes(startTime=fromTime, endTime=toTime)
        
        if areTimesValid is True:
            # check they are the same
            if useVenueForOneDay is True:
                # validate start time if venue is today
                isVenueToday = BookingUtilities().validateStartTimeAgainstToday(eventStartTime=fromTime, eventDate=fromDate)
                
                if isVenueToday is True or isVenueToday is None:
                    # go ahead and save the booking
                    # print('valid Booking')
                    preRequestRegisterRoutine(request=request, dateObjects=(fromDate, toDate), timeObjects=readableTime, eventDays=daysForTheEvent)
                
                else:
                    # print('second error')
                    messages.error(request, "Please ensure that the start time of the event is before the end time")
            
            else:
                # for many days
                # print('valid Booking')
                preRequestRegisterRoutine(request=request, dateObjects=(fromDate, toDate), timeObjects=readableTime, eventDays=daysForTheEvent)
        
        else:
            # print('first error')
            messages.error(request, "Please ensure that the start time of the event is before the end time")
        
    else:
        messages.error(request, "Please select a date that is not today or past!")
    

    return redirect("userenv:useraccount")


@login_required(login_url='messenger:home')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def cancelBooking(request, bookingId):
    # delete the request from the database
    BookingUtilities().deleteBookingRequest(requestId=bookingId)
    
    # alert the user that the booking request was deleted
    messages.error(request, 'The booking request was cancelled successfully!')
    
    return redirect("userenv:useraccount")

@login_required(login_url='messenger:home')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(isAdmin)
def fetchFullRequestDetails(request):
    # get the booking id
    bookingId = request.POST.dict()['booking-id']
    
    # get the details
    foundDetails = BookingUtilities().extractFullRequestDetails(idOfRequest=int(bookingId))
    
    return JsonResponse(
        dict(
            info = foundDetails
        )
    )
    
    
@login_required(login_url='messenger:home')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(isAdmin)
def issuePaymentLink(request):
    # extract the data from the request
    paymentLinkData = request.POST.dict()
    
    # print(paymentLinkData)
    
    # request id
    requestId = int(paymentLinkData['id-holder'])
    
    associatedRequestData = PaymentLinkUtils().getAttachedBookingRequest(requestId=requestId)
    
    if associatedRequestData:
        # check if link is visible
        linkVisibility = True if 'link-visibility' in paymentLinkData else False
        
        # bill
        billToPay = int(paymentLinkData['booking-charge'])
        
        # responsible person
        personnelInCharge = request.user.username
        
        PaymentLinkUtils().savePaymentLinkDetails(
            linkVisibility=linkVisibility,
            billToPay=billToPay,
            personnelInCharge=personnelInCharge,
            clientDetails=associatedRequestData,
            clientEmail=associatedRequestData.clientEmailAddress
            )

        messages.success(request, "Payment Link was issued successfully!")
        
    else:
        messages.error(request, "We are having issues on our end, try again in a few seconds!")
    
    return redirect('messenger:booking-requests')