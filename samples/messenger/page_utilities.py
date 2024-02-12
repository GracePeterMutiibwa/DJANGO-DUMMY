from django.http import HttpRequest

from django.shortcuts import get_object_or_404

from django.contrib import messages

from mariadmin.models import PageCategory, VendorPage, VendorDetails, SocialMediaHandles, VendorService

class PageTools:
    def __init__(self):
        pass
    
    def getPagePreviews(self, limit=None, categoryRequired=None, districtRequired=None):
        if categoryRequired is None:
            # get all
            allPagesInstances = VendorPage.objects.all()
            
        else:
            # select those of a category
            allPagesInstances = VendorPage.objects.filter(pageCategory=categoryRequired)
            
        
        if districtRequired is None:
            pass
        
        else:
            # filter only those that have the district
            allPagesInstances = allPagesInstances.filter(vendorDistrict=districtRequired)

        allPageInformation = [
            {
                'name': " ".join([eachToken.capitalize() for eachToken in pageInstance.pageName.split("-")]),
                'description': pageInstance.pageDescription,
                'actual_name': pageInstance.pageName,
                'image': pageInstance.pageImageLogo,
                'id': pageInstance.pk
            } for pageInstance in allPagesInstances if (pageInstance.isVisibleAndHasServices() is True)
        ]
        
        allPageInformation = allPageInformation[:limit] if (limit is not None and len(allPageInformation) >= limit) else allPageInformation
        
        
        
        return allPageInformation
        
        
        
    
    
    def extractPageDataToRender(self, pageDetailObject):
        # get the details
        extractedPageDetails = {
            'name': ' '.join([ nameToken.title() for nameToken in pageDetailObject.associatedVendorPage.pageName.split("-")]),
            'header': pageDetailObject.pageHeaderText,
            'slogan': pageDetailObject.vendorSlogan,
            'phone': pageDetailObject.vendorContact,
            'email': pageDetailObject.vendorEmail,
            'location': pageDetailObject.businessLocation
            
        }
        
        return extractedPageDetails
    
    
    def extractVendorServices(self, vendorPage):
        # get the service
        availableServices = vendorPage.vendor_services.all()
        
        preparedServices = [
            {
                'name': eachServiceObject.serviceName,
                'brief': eachServiceObject.serviceBriefDescription,
                'detail': eachServiceObject.serviceDetailedDescription,
                'image': eachServiceObject.servicePreviewImage
                
            } 
            
            for eachServiceObject in availableServices
        ]
        
        return preparedServices
    
    def getVendorPageDetails(self, vendorPage):
        # get the page with that data
        
        textualDetailsPresent = False
        
        
        try:
            # alert present
            textualDetailsPresent = True
            
            # get the details
            textualDetails = vendorPage.vendor_detail
            
        except:
            pass
        
        # is data present
        if textualDetailsPresent is True:
            pageData = {
                'media_handles': PageTools().getSocialHandles(pageId=vendorPage.pk),
                'details': self.extractPageDataToRender(pageDetailObject=textualDetails),
                'present_services': self.extractVendorServices(vendorPage=vendorPage)
            }
        
        else:
            # page data
            pageData = None
        
        return textualDetailsPresent, pageData
            
        
        
    
    def getServiceMeta(self, serviceId):
        # service
        selectedService = get_object_or_404(VendorService, pk=serviceId)
        
        serviceDetails = {
            'name': selectedService.serviceName,
            'brief': selectedService.serviceBriefDescription,
            'detailed': selectedService.serviceDetailedDescription,
            'image': selectedService.servicePreviewImage,
            'id': selectedService.pk
            
        }
        
        return serviceDetails
    
    def deleteServiceWithId(self, serviceId):
        # service
        selectedService = get_object_or_404(VendorService, pk=serviceId)
        
        # get the name
        foundName = selectedService.serviceName
        
        foundPageId = selectedService.associatedVendorPage.pk
        
        # delete the service
        selectedService.delete()
        
        return foundName, foundPageId
    
    def getPageServices(self, pageId):
        # page
        pageInstance = get_object_or_404(VendorPage, pk=pageId)
        
        # all services
        attachedServices = [
            {
                'name': eachService.serviceName,
                'id': eachService.pk
                
            } for eachService in pageInstance.vendor_services.all()
        ]
        
        return attachedServices
        
    
    def getSocialHandles(self, pageId):
        # get the page
        associatedPage = get_object_or_404(VendorPage, pk=pageId)
        
        try:
            # get the object
            associatedHandleObject = associatedPage.vendor_handles
            
            # check if the objects are present
            mediaHandles = {
                'facebook': associatedHandleObject.facebookHandle if associatedHandleObject.facebookHandle else None,
                'twitter': associatedHandleObject.twitterHandle if associatedHandleObject.twitterHandle else None,
                'instagram': associatedHandleObject.instagramHandle if associatedHandleObject.instagramHandle else None,
                'whatsapp': associatedHandleObject.whatsappHandle if associatedHandleObject.whatsappHandle else None
                
            }
            
        except:
            # blanks
            mediaHandles = {
                'facebook':None,
                'twitter': None,
                'instagram': None,
                'whatsapp': None
                
            }
        
        return mediaHandles
    
    def getPageMetaForId(self, pageId):
        # page
        pageInstance = get_object_or_404(VendorPage, pk=pageId)
        
        # extract the data
        pageMeta = {
            'name': pageInstance.pageName,
            'category': pageInstance.pageCategory,
            'description': pageInstance.pageDescription,
            'visible': pageInstance.isVisible,
            'district': pageInstance.vendorDistrict,
            'image': pageInstance.pageImageLogo,
            'id': pageInstance.pk,
            
        }
        
        return pageMeta
    
    def getPresentPages(self):
        # present pages
        presentPages = VendorPage.objects.all()
        
        pageMeta = [
            {
                'name': eachPage.pageName,
                'category': eachPage.pageCategory,
                'id': eachPage.pk
                
            } for eachPage in presentPages
        ]
        
        return pageMeta
    
    def getPageDetails(self, pageId):
        # get the vendor page
        vendorPage = get_object_or_404(VendorPage, pk=pageId)
        
        try:
            # get the details object
            vendorDetail = vendorPage.vendor_detail
            
            # extract the details
            pageDetails = {
                'heading': vendorDetail.pageHeaderText,
                'slogan': vendorDetail.vendorSlogan,
                'phone': vendorDetail.vendorContact,
                'email': vendorDetail.vendorEmail,
                'location': vendorDetail.businessLocation    
            }
            
        except:
            # for missing details
            pageDetails = {
                'heading': None,
                'slogan': None,
                'phone': None,
                'email': None,
                'location': None
                
                
            }
            
        
        return pageDetails
    
            
    def getPageCategories(self):
        # get all the categories
        presentCategories = PageCategory.objects.all()
        
        # arranged categories
        preparedCategories = [
            {
                'name': eachPageCategory.categoryName,
                'id': eachPageCategory.pk 
            } 
            
            for eachPageCategory in presentCategories
        ]
        
        return preparedCategories
        
        

class PageManager:
    def __init__(self, request:HttpRequest):
        # get the request
        self.requestObject = request
        
        # get the data
        self.sentRequestData = request.POST.dict()
        
        
    def writeServiceDetail(self, associatedPageObject, editMode=False):
        # create
        if editMode is True:
            # get the pk
            serviceId = int(self.sentRequestData['service-to-edit'])
            
            # create object
            serviceInstance = get_object_or_404(VendorService, pk=serviceId)
            
        else:
            serviceInstance = VendorService.objects.create(associatedVendorPage=associatedPageObject)
        
        # extract the service
        serviceName = self.sentRequestData['service-name'].title()
        
        # add the details
        serviceInstance.serviceName = serviceName
        
        serviceInstance.serviceBriefDescription = self.sentRequestData['brief-description'].capitalize()
    
        serviceInstance.serviceDetailedDescription = self.sentRequestData['detailed-description'].capitalize()

        serviceInstance.servicePreviewImage = self.sentRequestData['service-image']
        
        # save the 
        serviceInstance.save()
        
        return
    
    def savePageServiceDetail(self, pageId):        
        # get service name
        serviceName = self.sentRequestData['service-name'].title()
        
        # get the associated page
        associatedPageObject = get_object_or_404(VendorPage, pk=pageId)
        
        # edit mode
        editMode = True if 'service-to-edit' in self.sentRequestData else False
        
        # duplicates
        if editMode is True:
            # get the id
            idToExclude = int(self.sentRequestData['service-to-edit'])
            
            # avoid those that match it and check for duplicates
            isDuplicate = associatedPageObject.vendor_services.exclude(pk=idToExclude).filter(serviceName=serviceName).first()

        else:
            isDuplicate = associatedPageObject.vendor_services.filter(serviceName=serviceName).first()
        
        if isDuplicate:
            # alert
            messages.warning(self.requestObject, f"The service name '{serviceName}' already exists maybe delete it 😌")
        
        else:

            # make the write
            self.writeServiceDetail(associatedPageObject=associatedPageObject, editMode=editMode)
            
            # determine the result messages
            operationMessage = "updated" if editMode is True else "saved"
            
            messages.success(self.requestObject, f"The service '{serviceName}' was {operationMessage} successfully!")
            

        return
        
    
    def saveSocialMediaInformation(self):
        # get the associated page data
        pageId = int(self.sentRequestData['page-id'])
        
        # get the associated page
        associatedPage = get_object_or_404(VendorPage, pk=pageId)
        
        # handle is by default present
        handleIsPresent = True
        
        try:
            # get the social media handle
            associatedHandleObject = associatedPage.vendor_handles
            
        except:
            # new
            handleIsPresent = False
            
            # create a new one
            associatedHandleObject = SocialMediaHandles.objects.create(associatedVendorPage=associatedPage)
            
            
        # save the handles
        # add the handles
        if 'facebook-handle' in self.sentRequestData:
            associatedHandleObject.facebookHandle = self.sentRequestData['facebook-handle']

        if 'twitter-handle' in self.sentRequestData:
            associatedHandleObject.twitterHandle = self.sentRequestData['twitter-handle']            

        if 'instagram-handle' in self.sentRequestData:
            associatedHandleObject.instagramHandle = self.sentRequestData['instagram-handle']  
            
        if 'whatsapp-handle' in self.sentRequestData:
            associatedHandleObject.whatsappHandle = self.sentRequestData['whatsapp-handle']
            
        #   save the object
        associatedHandleObject.save()
        
        # determine the return message for the user
        returnMessage = "updated" if handleIsPresent is True else "saved"
        
        messages.success(self.requestObject, f"Page Handles were {returnMessage} successfully! !")

        return 
        
        
        
    def fetchPageMeta(self):
        # id
        pageId = int(self.sentRequestData['page-id'])
        
        # get the meta
        foundMeta = PageTools().getPageMetaForId(int(pageId))
        
        return foundMeta
        
    
    def writeVendorPage(self, writeMode):
        if writeMode == 1:
            # create new category
            newVendorPage = VendorPage.objects.create()
            
        else:
            # get the id
            idForPage = int(self.sentRequestData['page-id'])
            
            newVendorPage = get_object_or_404(VendorPage, pk=idForPage)
            
            
        pageName = '-'.join(self.sentRequestData['page-name'].lower().split(" "))
        
        # get the page meta
        pageDescription = self.sentRequestData['page-description'].capitalize()
        
        # page image
        pageImageUrl = self.sentRequestData['page-image-url']
        
        pageCategory = self.sentRequestData['page-category']
        
        businessLocation = self.sentRequestData['business-location']

        # add the data
        newVendorPage.pageName = pageName
        
        newVendorPage.pageDescription = pageDescription
        
        newVendorPage.pageCategory = pageCategory
        
        newVendorPage.vendorDistrict = businessLocation
        
        newVendorPage.pageImageLogo = pageImageUrl
        
        # get state
        if 'page-visibility' in self.sentRequestData and self.sentRequestData['page-visibility'] == 'on':
            # get update the state
            newVendorPage.isVisible = True
            
        else:
            # turn it off
            newVendorPage.isVisible = False
            
        
        # save
        newVendorPage.save()
        
        return
    
    def getPageDetailsObject(self, vendorInstance):
        # get the objects
        detailsObject = VendorDetails.objects.filter(associatedVendorPage=vendorInstance).first()
        
        detailsPresent = True
        
        if detailsObject:
            pass
        
        else:
            # alert new
            detailsPresent = False
            
            # create a new one
            detailsObject = VendorDetails.objects.create(associatedVendorPage=vendorInstance)
            
        return detailsObject, detailsPresent
    
    def writePageDetails(self, pageId):
        # get the page
        userPageInstance = get_object_or_404(VendorPage, pk=pageId)
        
        # get the page object
        pageDetailsObject, detailsPresent = self.getPageDetailsObject(userPageInstance)
        
        # save the details
        pageHeaderText = self.sentRequestData['page-heading'].title()
        
        vendorSlogan = self.sentRequestData['vendor-slogan'].capitalize()
        
        vendorContact = self.sentRequestData['phone-contact']
        
        vendorEmail = self.sentRequestData['business-email']
        
        businessLocation = self.sentRequestData['main-location'].title()
        
        # update the fields
        pageDetailsObject.pageHeaderText = pageHeaderText
        
        pageDetailsObject.vendorSlogan = vendorSlogan
        
        pageDetailsObject.vendorContact = vendorContact
        
        pageDetailsObject.vendorEmail = vendorEmail
        
        pageDetailsObject.businessLocation = businessLocation
        
        # save the details object
        pageDetailsObject.save()
        
        # operation message
        operationMessage = "updated" if detailsPresent is True else "saved"
        
        # alert success
        messages.success(self.requestObject, f"Page Details were {operationMessage} successfully! !")

        return
        
        
        
    
    def saveNewVendorPage(self):
        # get the submitted page name
        pageName = '-'.join(self.sentRequestData['page-name'].lower().split(" "))
        
        # write mode
        writeMode = 1
        
        # check for duplicates
        if 'page-id' in self.sentRequestData:
            # initialize the write mode
            writeMode = 2
            
            # get the page id
            pageId = self.sentRequestData['page-id']
            
            isDuplicate = VendorPage.objects.exclude(pk=int(pageId)).filter(pageName=pageName).first()
        
        else:
            isDuplicate = VendorPage.objects.filter(pageName=pageName).first()  
        
        
        if isDuplicate:
            # alert duplicate
            messages.warning(self.requestObject, "That Page name already exists, maybe delete it first!")
            
        else:
            # make a save or update
            self.writeVendorPage(writeMode=writeMode)

            # operation name
            if writeMode == 1:
                operationName = 'registered'
            
            else:
                operationName = 'updated'
                
            # create a display message
            messages.success(self.requestObject, f"The page Named '{pageName}' was {operationName} successfully! !")
                
        return
        
    
    def savePageCategoryInformation(self):
        # get the category name and validate its existance
        pageCategoryName = self.sentRequestData['page-category-name'].title()
        
        # check for duplicates
        isDuplicate = PageCategory.objects.filter(categoryName=pageCategoryName).first()
        
        if isDuplicate:
            # alert duplicate
            messages.warning(self.requestObject, "Category name already exists, maybe delete it first!")
            
        else:
            # create new category
            newCategoryName = PageCategory.objects.create(categoryName=pageCategoryName)
            
            # save
            newCategoryName.save()
            
            messages.success(self.requestObject, f"A new Page Category '{pageCategoryName}' was added successfully! !")

            
        return