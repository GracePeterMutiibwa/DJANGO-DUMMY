from mariadmin.models import Category, BookingRequest, BookingTransaction

import datetime

from datetime import date


class PaymentLinkUtils:
    def __init__(self):
        pass
    
    def getAttachedBookingRequest(self, requestId):
        # get the booking request
        bookingRequest = BookingRequest.objects.filter(pk=requestId).first()
        
        return bookingRequest
    
    def getTransactionsOfClientViaEmail(self, clientEmail):
        # present transactions
        pendingTransactions = BookingTransaction.objects.filter(clientEmailAddress=clientEmail, isVisible=True, isSatisfied=False).all()
        
        # get payment details
        paymentLinkData = [
            {
                'date': eachLinkObject.issuedDate.strftime('%d-%m-%Y'),
                'dates': eachLinkObject.clientDetails.getDateSummary(),
                'time': eachLinkObject.clientDetails.getCastTimes(getMode=2),
                'bill': eachLinkObject.transactionBill,
                'id': eachLinkObject.pk
            }
            for eachLinkObject in pendingTransactions
        ]
        
        return paymentLinkData
        
    
    def savePaymentLinkDetails(self, linkVisibility, billToPay, personnelInCharge, clientDetails:BookingRequest, clientEmail):
        # create a payment link
        newTransactionLink = BookingTransaction.objects.create(
            isVisible=linkVisibility,
            transactionBill=billToPay,
            whoIssuedTransaction=personnelInCharge,
            clientDetails=clientDetails,
            clientEmailAddress=clientEmail
        )
        
        # save the payment link
        newTransactionLink.save()
        
        # update that a link was issued
        clientDetails.hasLinkIssued = True
        
        clientDetails.save()

        return


class BookingUtilities:
    # converts dates and times to integer tokens
    
    def __init__(self):
        self.tokensMint = lambda conversionType, rawObject: [int(eachToken) for eachToken in rawObject.strip().split('-')] if conversionType == 1 else [int(eachToken) for eachToken in rawObject.strip().split(':')]
        
    
    def extractFullRequestDetails(self, idOfRequest):
        # get the details
        bookingRequest = BookingRequest.objects.filter(pk=idOfRequest).first()
        
        if bookingRequest:
            # get full details
            fullRequestDetails = bookingRequest.getFullDetails()
        
        else:
            # return blank
            fullRequestDetails = {}
            
        return fullRequestDetails
    
    def deleteBookingRequest(self, requestId):
        # get the object
        bookingRequest = BookingRequest.objects.filter(pk=requestId).first()
        
        if bookingRequest:
            # delete the booking request
            bookingRequest.delete()
            
        else:
            pass
        
        return
    
    
    
    def getBookingRequestsOfClient(self, clientAddress=None):
        if clientAddress is None:
            presentRequests = BookingRequest.objects.filter(isComplete=False, hasLinkIssued=False).all()
            
            pendingRequests = BookingRequest.objects.filter(isComplete=False, hasLinkIssued=True).all()
            
            completeRequests = BookingRequest.objects.filter(isComplete=True).all()
            
            requestsData = {
                'new_requests': [eachRequest.getRequestDetails(fetchMode=2) for eachRequest in presentRequests if presentRequests],
                'complete_requests': [eachRequest.getRequestDetails(fetchMode=2) for eachRequest in completeRequests if completeRequests],
                'pending_requests': [eachRequest.getRequestDetails(fetchMode=2) for eachRequest in pendingRequests if pendingRequests],
            }
        
        else:
            presentRequests = BookingRequest.objects.filter(clientEmailAddress=clientAddress, isComplete=False).all()
        
            # present requests
            requestsData = [
                {
                    'info': eachRequest.getRequestDetails(),
                    'id': eachRequest.pk
                } for eachRequest in presentRequests
                ] if presentRequests else []
        
        return requestsData
        
    
    def saveNewBookingRequest(self, clientName, clientEmail, eventDetails, startDate, endDate, timeStamps, daysOfUse, eventCategory, guestNumber):
        # create a new instance
        bookingRequestObject = BookingRequest.objects.create(
            clientName=clientName,
            clientEmailAddress=clientEmail,
            requestParticulars=eventDetails,
            eventCategory=eventCategory,
            venueUsageDate=startDate,
            venueEndDate=endDate,
            numberOfGuests=guestNumber,
            numberOfDays=daysOfUse,
            timeStamps=timeStamps
            )
        
        bookingRequestObject.save()
        
        return
    
    def generateDateObjects(self, rawDateInfo, objectType=1):
        # break the date into tokens
        tokenList = self.tokensMint(objectType, rawObject=rawDateInfo)
        
        # create date objects
        dateOrTimeObject = date(tokenList[0], tokenList[1], tokenList[2])
        
        return dateOrTimeObject
    
    def validateDateAgainstToday(self, fromDate:date):
        # get todays date
        todaysDateObject = datetime.datetime.today().date()
        
        # compare the dates
        isDateTodayOrAhead = fromDate >= todaysDateObject
        
        return isDateTodayOrAhead
    
    
    def timeObjectsMint(self, timeTokens):
        # check if the time is valid
        todaysDateObject = datetime.datetime.today().date()
        
        # generate time objects
        timeObject = datetime.datetime(year=todaysDateObject.year, month=todaysDateObject.month, day=todaysDateObject.day, hour=timeTokens[0], minute=timeTokens[1])
        
        return timeObject
    
    def validateStartTimeAgainstToday(self, eventStartTime, eventDate:date):
        # track time validity
        isTimeValid = None
        
        # get the current date
        todaysDate = datetime.datetime.today().date()
        
        # check if the date is today
        areDatesTheSame = eventDate == todaysDate
        
        if areDatesTheSame is True:
            # get that days date
            eventStartTime = self.timeObjectsMint(self.tokensMint(conversionType=2, rawObject=eventStartTime))
            
            # check the hours if they are not pas
            todaysTimeObject = datetime.datetime.now()
            
            # check if the time is valid if the date is the same
            isTimeValid = eventStartTime > todaysTimeObject
            
        else:
            pass
        
        
        return isTimeValid
    
    def validateEventTimes(self, startTime, endTime):
        # check if the ranges are valid
        areRangesValid = False
        
        startTimeTokens = self.tokensMint(conversionType=2, rawObject=startTime)
        
        endTimeTokens = self.tokensMint(conversionType=2, rawObject=endTime)
        
        # get time objects
        startTimeObject = self.timeObjectsMint(timeTokens=startTimeTokens)

        endTimeObject = self.timeObjectsMint(timeTokens=endTimeTokens)
        
        # create readable time formats
        readableStart = startTimeObject.strftime('%H:%M %p')
        
        readableEnd = endTimeObject.strftime('%H:%M %p')
        
        # is start time greater than the end time
        timeGapIsPresent = startTimeObject < endTimeObject
        
        return timeGapIsPresent, (readableStart, readableEnd)
    
    def validateDateObjects(self, fromDate:date, toDate:date):
        # validity
        isRangeValid = False
        
        daysEventWillTake = 0
        
        # against today
        isDateTodayOrAhead = self.validateDateAgainstToday(fromDate=fromDate)
        
        if isDateTodayOrAhead is True:
            # alert that the range is ok
            isRangeValid = True
            
            # given they are valid against today then the number of days the event will take can
            # be attained
            daysEventWillTake = (toDate - fromDate).days + 1
                
        else:
            pass
        
        return isRangeValid, daysEventWillTake
    
    def getEventsList(self):
        eventsCatalogue = [
                str(eachCategory) for eachCategory in Category.objects.all()
            ]
        
        return eventsCatalogue
    
    
    def checkForDuplicateBookings(self, userEmail, fromDate, toDate, timeSlot):
        # check for a booking on that date for the given client
        bookingObject = BookingRequest.objects.filter(clientEmailAddress=userEmail, venueUsageDate=fromDate, venueEndDate=toDate, timeStamps=timeSlot).first()
        
        # check the status
        duplicatePresent = True if bookingObject else False
        
        return duplicatePresent