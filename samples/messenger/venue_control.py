from django.http import HttpRequest
from django.contrib import messages
from mariadmin.models import VenueImageItem, VenueItem
from django.shortcuts import get_object_or_404

class VenueTools:
    def deleteVenueImage(self, venueImageId):
        # get
        venueImageObject = get_object_or_404(VenueImageItem, pk=venueImageId)
        
        # delete
        venueImageObject.delete()
        
        return
        
    
    
    def getAllVenueImages(self, venueId):
        venueObject = get_object_or_404(VenueItem, pk=venueId)
        
        # get the images
        allVenueImages = venueObject.attached_venue_images.all()
        
        preparedImages = [
            {
                'url': eachVenueImage.imageUrl,
                'id': eachVenueImage.pk
            }
            for eachVenueImage in allVenueImages
        ]
        
        return preparedImages
        
        
        
        

class VenueUtilities:
    def __init__(self, request:HttpRequest):
        self.requestObject = request
        
        self.submittedRequestData = request.POST.dict()
        
    
    def saveVenueImage(self):
        # get the image name
        imageUrl = self.submittedRequestData['venue-image']
        
        if imageUrl.endswith(".jpg") or imageUrl.endswith(".png") or imageUrl.endswith(".jpeg"):
            pass
        
        else:
            # alert 
            messages.error(self.requestObject, "The Image Url selected is invalid.., use the selector to select an image, 😌!")
            
            return
        
        # validate duplicate
        # get venue
        venueId = self.submittedRequestData['selected-venue-id']
        
        referenceVenueItem = get_object_or_404(VenueItem, pk=int(venueId))
        
        isDuplicate = referenceVenueItem.attached_venue_images.filter(imageUrl=imageUrl).first()
        
        if isDuplicate:
            messages.error(self.requestObject, "The Image Already exists for the venue, maybe first delete it 😌!")

            return
        
        else:
            # create a new venue image item
            newVenueImageItem = VenueImageItem.objects.create(associatedVenue=referenceVenueItem, imageUrl=imageUrl)
            
            # save
            newVenueImageItem.save()
            
            # alert success
            messages.success(self.requestObject, f"The Image was successfully saved for  '{referenceVenueItem.venueName}' 🥳!")
            
            return

        
        