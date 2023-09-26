from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

from django.views.decorators.cache import cache_control

from mariadmin.models import MessageFlow, WebsiteHeadingImage

from django.db.models import Q

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
        
        pageContext = {
            'chat_messages': availableMessages,
            'banner_image': bannerImage.imageUrl if bannerImage else None
            
        }
        
        # print("Image:", request.session['avatar'])
        
        # chat-page.html
        return render(request, "mariadmin/profile-page.html", context=pageContext)
