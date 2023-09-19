from django.db import models

from django.utils import timezone

from datetime import datetime

from django.contrib.auth.models import User

class WebsiteHeadingImage(models.Model):
    imageUrl = models.TextField()
    
    
class gardensTourVideoLink(models.Model):
    videoUrl = models.TextField()

class NotAccessibleYet(models.Model):
    adminEmailAddress = models.TextField()

class AdminNextOfKins(models.Model):
    addedDate = models.DateTimeField(auto_now_add=True)
    
    adminUserName = models.TextField()
    
    adminEmailAddress = models.TextField()
    
    class Meta:
        ordering = ("-addedDate",)

class AdminPermissions(models.Model):
    websiteEditor = models.BooleanField(default=False)
    
    blogEditor = models.BooleanField(default=False)
    
    thirdPartyEditor = models.BooleanField(default=False)

    commUtilities = models.BooleanField(default=False)
    
    associatedAdmin = models.OneToOneField(AdminNextOfKins, on_delete=models.CASCADE, related_name="assigned_permissions", default=None)
    
    def getPresentPermissions(self):
        return {
            'website': self.websiteEditor,
            'blog': self.blogEditor,
            'pages': self.thirdPartyEditor,
            'comms': self.commUtilities,
            'users': False,
        }
    
    def hasPermissions(self):
        # permissions
        permissionsList = [
            self.websiteEditor,
            self.blogEditor,
            self.thirdPartyEditor,
            self.commUtilities,
        ]
        
        # any present
        isAuthenticated = permissionsList.count(True) > 0
        
        return isAuthenticated

        
class NextOfKinItem(models.Model):
    associatedUserObject = models.OneToOneField(User, on_delete=models.CASCADE, related_name="their_access_tag")
    
    associatedPermissions = models.OneToOneField(AdminPermissions, on_delete=models.CASCADE, related_name="their_user_profile")


class EmailReset(models.Model):
    attachedEmail = models.TextField()
    
    generatedCode = models.TextField()
    
    expiryTime = models.DateTimeField()
    
    createdDate = models.DateTimeField(auto_now_add=True)
    
    
    def timeNotYetExpired(self):
        # calculate if the time is expired
        currentTimeInstance = datetime.now(timezone.utc)
        
        # converted expiry time
        expiryTime = self.expiryTime.replace(tzinfo=timezone.utc)
        
        expiryStatus = True if expiryTime >= currentTimeInstance else False
        
        return expiryStatus
    
    

class PostCategory(models.Model):
    categoryName = models.TextField()

    def __str__(self):
        return str(self.categoryName)
    



class VendorPage(models.Model):
    pageName = models.TextField()
    
    pageDescription = models.TextField()
    
    pageImageLogo = models.TextField(default="")
    
    pageCategory = models.TextField()
    
    isVisible = models.BooleanField(default=False)
    
    vendorDistrict = models.TextField(default='Kampala')
    
    dateAdded = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        ordering = ("-dateAdded",)
        
    
    def isVisibleAndHasServices(self):
        # get services info
        serviceCount = self.vendor_services.all().count()
        
        # get status
        totalStatus = serviceCount > 0 and self.isVisible is True
        
        return totalStatus
        

class VendorService(models.Model):
    associatedVendorPage = models.ForeignKey(VendorPage, on_delete=models.CASCADE, related_name="vendor_services")
        
    serviceName = models.TextField()
    
    serviceBriefDescription = models.TextField(max_length=180)
    
    serviceDetailedDescription = models.TextField()
    
    servicePreviewImage = models.TextField()
    
    dateAdded = models.DateTimeField(auto_created=True, default=timezone.now)
    
    class Meta:
        ordering = ("-dateAdded",)

class VendorDetails(models.Model):
    associatedVendorPage = models.OneToOneField(VendorPage, on_delete=models.CASCADE, related_name="vendor_detail")
    
    pageHeaderText = models.TextField()
    
    vendorSlogan = models.TextField()
    
    vendorContact = models.TextField()
    
    vendorEmail = models.TextField()
    
    businessLocation = models.TextField()
    

class SocialMediaHandles(models.Model):
    associatedVendorPage = models.OneToOneField(VendorPage, on_delete=models.CASCADE, related_name="vendor_handles")

    facebookHandle = models.TextField(blank=True, null=True)
    
    twitterHandle = models.TextField(blank=True, null=True)
    
    instagramHandle = models.TextField(blank=True, null=True)
    
    whatsappHandle = models.TextField(blank=True, null=True)

class PageCategory(models.Model):
    categoryName = models.TextField()

    def __str__(self):
        return str(self.categoryName)
    
    class Meta:
        ordering = ("categoryName",)   
    

    

class PostItem(models.Model):
    postHeading = models.TextField()
    
    postHeadingImage = models.TextField()
    
    postTopBody = models.TextField()
    
    postMainImage = models.TextField()
    
    postLeftSubImage = models.TextField(blank=True, null=True)
    
    postRightSubImage = models.TextField(blank=True, null=True)
    
    postLowerBody = models.TextField(default='')
    
    postPossibleCategories = models.TextField(default='general')
    
    postDate = models.DateTimeField(auto_now_add=True)
    
    postFeatured = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('-postDate',)
        
class PostComment(models.Model):
    attachedPost = models.ForeignKey(PostItem, on_delete=models.CASCADE, related_name='associated_comments', blank=True, null=True)
    
    posterName = models.TextField()
    
    commentDate = models.DateTimeField(auto_now_add=True)
    
    postComment = models.TextField()
    
    class Meta:
        ordering = ("-commentDate",)
    

class EmailHolders(models.Model):
    userEmail = models.TextField()
    
    def __str__(self):
        return str(self.userEmail)

class EmailReplies(models.Model):
    associatedHolder = models.ForeignKey(EmailHolders, on_delete=models.CASCADE, related_name='user_replies')

    replyMessage = models.TextField()
    
    dateCreated = models.DateTimeField(auto_created=True, default=timezone.now)
    
    class Meta:
        ordering = ('-dateCreated',)
    
class SimpleContactMessages(models.Model):
    UserName = models.TextField()
    
    UserEmail= models.TextField()
    
    UserSubject = models.TextField()
    
    UserMessage= models.TextField()
    
    dateSent = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('dateSent',)
    

class MessageEntryNames(models.Model):
    UserName = models.TextField()
    
    def __str__(self):
        return str(self.UserName)

class MessageFlow(models.Model):
    fromToMeta = models.TextField(blank=False)
    
    dateSent = models.DateTimeField(auto_now_add=True)
    
    messageMeta = models.TextField(blank=False)
    
    class Meta:
        ordering = ('dateSent',)
        
    
    def __str__(self):
        return f"On {self.dateSent}, {self.fromToMeta}: {self.messageMeta}"


class Contacts(models.Model):
    contactType = models.TextField(blank=False)
    
    contactValue = models.TextField(blank=False)

class StatisticsMeta(models.Model):
    happyGuests = models.IntegerField()
    
    hostedEvents = models.IntegerField()
    
    staffCount = models.IntegerField()
    
    venueCount = models.IntegerField()
    

    
    
    

class Testimonial(models.Model):
    guestName = models.TextField(blank=False)
    
    guestPosition = models.TextField(blank=False)
    
    guestComment = models.TextField(blank=False)
    
    guestImageUrl = models.TextField(blank=False)
    


class VenueItem(models.Model):
    venueName = models.TextField(blank=False)
    
    venueDescription = models.TextField(blank=False)
    
    venueCapacity = models.IntegerField(default=0)
    
    isFeatured = models.BooleanField(blank=False)
    
    venueCategory = models.TextField(default='Social Event')
    
    def hasImages(self, checkState=1):
        # get them
        firstImage = self.attached_venue_images.all().first()
        
        if checkState == 1:
            # status
            imagePresenceStatus = True if firstImage else False
            
            return imagePresenceStatus
        
        else:
            # get the image, since we now know they are present
            return firstImage.imageUrl

    

class VenueImageItem(models.Model):
    associatedVenue = models.ForeignKey(VenueItem, on_delete=models.CASCADE, related_name="attached_venue_images")
    
    imageUrl = models.TextField(blank=False)
    
    dateAdded = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ("-dateAdded",)

class MiddleGrid(models.Model):
    gridTitle = models.TextField(blank=False)
    
    gridMessage = models.TextField(blank=False)
    
    gridRedirectionUrl = models.TextField(blank=False)
    
    gridButtonText = models.TextField(blank=True)

class OfferedService(models.Model):
    serviceName = models.TextField(blank=False)
    
    serviceDetails = models.TextField(blank=False)

class RightCard(models.Model):
    rightCardHeading = models.TextField(blank=False)
    
    rightCardText = models.TextField(blank=False)
    
    rightCardImageUrl = models.TextField(blank=True, null=True)
    

class LeftCard(models.Model):
    leftCardHeading = models.TextField(blank=False)
    
    leftCardText = models.TextField(blank=False)
    
    leftCardImageUrl = models.TextField(blank=True, null=True)


class AboutDetails(models.Model):
    aboutMore = models.TextField(blank=False)
    
    def __str__(self):
        return self.aboutMore

class AboutHeading(models.Model):
    headingName = models.TextField(max_length=250, blank=False)
    
    def __str__(self):
        return self.headingName

class Category(models.Model):
    modelName = models.TextField(max_length=45, blank=False)
    
    def __str__(self):
        return self.modelName
    
    class Meta:
        ordering = ['modelName']
        
        
class ImageAsset(models.Model):
    imageName = models.TextField(blank=False)
    
    imageSize = models.TextField(blank=False)
    
    imageData = models.ImageField(upload_to="assets/")
    
    uploadDate = models.DateTimeField(auto_now_add=True, blank=False, null=True)
    
    isGalleryItem = models.BooleanField(default=False)
    
    
    def delete(self, *args, **kwargs):
        # delete the image file
        self.imageData.delete()
        
        # call the parent delete method
        super().delete(*args, **kwargs)
        
        return
        
