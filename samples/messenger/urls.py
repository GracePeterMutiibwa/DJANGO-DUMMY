from django.urls import path

from django.views.generic import RedirectView

from . import views

app_name = 'messenger'

urlpatterns = [
    path('', views.websiteHomePage, name='welcome'),
    
    path('login/', views.homePage, name='home'),
    
    path('update-avatar/', views.updateUserAvatar, name='update-avatar'),
    
    path('save-venue-image/', views.saveVenueImage, name='write-venue-image'),
    
    path('delete-venue-image/', views.deleteVenueImage, name='delete-venue-image'),

    path('fetch-venue-images/', views.findVenueImages, name='get-venue-images'),
    
    path('reset/', views.getResetCodeViaEmail, name='start-reset'),
    
    path('submit-reset-code/', views.displayResetPage, name='collect-reset-code'),
    
    path('reset-password/', views.resetUserPassword, name='password-reset'),
    
    path('search-by-district/', views.viewServicesByDistrict, name='search-by-district'),
    
    path('signup/', views.registerPage, name='register'),
    
    path('about-us/', views.aboutPage, name='about'),
    
    path('venues/', views.venuePage, name='venue'),
    
    path('venue-detail/<str:venueName>/', views.viewVenueDetails, name='venue-details'),
    
    path('chat/', views.chatPage, name='chat-page'),
    
    path('blog-editor/', views.blogEditorPage, name='blog-editor'),
    
    path('blog-page/<int:pageId>', views.viewBlogPostDetails, name='blog-post'),
    
    path('delete-post/<int:postCategoryId>/', views.deleteSpecificPostCategory, name='delete-post'),
    
    path('delete-post-data/<int:postItemId>/', views.deleteSpecificPostItem, name='delete-post-data'),
    
    path('email/', views.emailPage, name='email-page'),
    
    path('submit-message/<int:userGroup>/', views.submitChatMessage, name='chat-upload'),
    
    path('gallery/', views.galleryPage, name='gallery'),
    
    path('gallery-manager/', views.galleryControlPanel, name='gallery-control'),
    
    path('update-image-state/', views.updateGalleryImageState, name='gallery-image-control'),
    
    path('page-registry/', views.viewPageRegistry, name='page-registry'),
    
    path('services/', views.servicesPageView, name='restaurant'),
    
    path('services/<str:serviceCategory>/', views.viewServicesByCategory, name='services-by-category'),
    
    path('blog/', views.blogPostPage, name='blog'),
    
    path('submit-comment/', views.submitPostComment, name='submit-comment'),
    
    path('get-post-data/', views.getPostInformation, name='get-post-data'),
    
    path('contact/', views.contactPage, name='contact'),
    
    path('logout/', views.logoutUser, name='logout-user'),
    
    path('uploads/', views.fileManagerPage, name='file-manager'),
    
    path('alter-primary-credentials/', views.managePrimaryCredentials, name='primary-credentials'),
    
    path('user-access/', views.manageNextOfKins, name='next-of-kins'),
    
    path('register-admin/', views.registerNewAdmin, name='register-admin'),
    
    path('wipe-admin-user/<int:adminId>', views.ripOffAdmin, name='wipe-administrator'),
    
    path('get-admin-profile/', views.fetchAdminDetail, name='get-admin-data'),
    
    path('alter-admin-profile/', views.changeAdminPermissions, name='alter-admin-profile'),
    
    path('alter-local-user-credentials/', views.updateUserCredentials, name='update-local-user-credentials'),
    
    path('grant-admin-access/<int:idOfAdmin>/', views.giveSecondaryAdminAccess, name='grant-admin-access'),
    
    path('delete-upload/<int:imageId>/', views.deleteSpecificUpload, name='wipe-upload'),
    
    path('delete-thread/', views.wipeMessagesThread, name='wipe-thread'),
    
    path('delete-service/<int:serviceId>/', views.deleteSpecificService, name='wipe-service'),
    
    path('delete-page-category/<int:categoryId>/', views.deletePageCategory, name='wipe-page-category'),
    
    path('delete-venue/<int:venueId>/', views.deleteSpecificVenue, name='wipe-venue'),
    
    path('delete-contact/<int:contactId>/<int:whoseContact>/', views.deleteSpecificContact, name='wipe-contact'),
    
    path('delete-comments/<int:postId>/', views.deletePostComments, name='delete-comments'),
    
    path('delete-reply/<int:replyId>/', views.deleteSpecificReply, name='wipe-reply'),
    
    path('delete-vendor-page/<int:pageId>/', views.deleteVendorPage, name='wipe-vendor-page'),
    
    path('delete-all-chats/<str:userName>/', views.deleteChatsForGivenUser, name='wipe-all-chats'),
    
    path('delete-testimonial/<int:testimonialId>/', views.deleteSpecificTestimonial, name='wipe-testimonial'),
    
    path('editor/<int:sectionId>/', views.makeWebsiteEdit, name='edit-website'),
    
    path('update-venue/', views.updateVenueFeaturedStatus, name='update-venue'),
    
    path('update-post-state/', views.updatePostFeaturedState, name='update-post'),
    
    path('get-user-chats/', views.getNewUserChats, name='get-chats'),
    
    path('submit-message/', views.submitSimpleMessage, name='submit-message'),
    
    path('submit-page-category/', views.registerPageCategory, name='submit-page-category'),
    
    path('get-thread/', views.getMessageThreadData, name='get-thread'),
    
    path('submit-reply/', views.submitAdminReply, name='send-reply'),
    
    path('save-page/', views.recordNewVendorPage, name='save-page'),
    
    path('get-page-data/', views.fetchPageMeta, name='get-page-meta'),
    
    path('page-manager/<int:pageId>', views.manageThirdPartyPage, name='manage-vendor-page'),
    
    path('save-page-details/', views.savePageDetails, name='save-page-details'),
    
    path('save-page-handles/', views.savePageHandles, name='save-page-handles'),
    
    path('save-page-services/', views.savePageServices, name='save-page-services'),
    
    path('delete-page-service/<int:serviceId>', views.wipePageService, name='wipe-page-service'),
    
    path('get-service-meta/', views.fetchServiceInformation, name='get-service-info'),
    
    path("service-providers/<str:vendorPageName>/", views.viewVendorPage, name='vendor-page'),
                
]
