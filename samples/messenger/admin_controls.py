from django.http import HttpRequest

from mariadmin.models import AdminNextOfKins, AdminPermissions, NotAccessibleYet, NextOfKinItem

from django.contrib.auth.models import User

from django.contrib import messages

from django.shortcuts import get_object_or_404

from .mail_processor import MessengerUtils

import secrets

class AdminTools:
    def removeAccessBarrier(self, emailToFree):
        # get and wipe the barrier object
        barrierObject = NotAccessibleYet.objects.filter(adminEmailAddress=emailToFree).all()
        
        if barrierObject:
            # object to be deleted
            barrierObject.delete()
            
            # print("Wiped the object")
            
        else:
            pass
        
        return
    def generateTemporaryPassword(self):
        # seed
        seedLength = 5
        
        # get a random password
        generatedPassword = secrets.token_urlsafe(seedLength)
        
        return generatedPassword
    
    def wipeAdminUserObject(self, adminRolesObject:AdminPermissions):
        
        # get the user object
        try:
            # kins item
            kinsItem = adminRolesObject.their_user_profile
            
            # get and delete the userInstance, it will too delete the item
            kinsItem.associatedUserObject.delete()
            
            print("Deleted the user!")
            
        except:
            # not a user yet
            pass
        
        return
        
        
        
    def deleteGivenAdminProfile(self, adminId):
        # delete 
        adminObject = get_object_or_404(AdminNextOfKins, pk=adminId)
        
        # get the permissions
        permissionsObject = adminObject.assigned_permissions
        
        # delete the user
        self.wipeAdminUserObject(adminRolesObject=permissionsObject)
        
        # get the admin name
        adminName = adminObject.adminUserName
        
        adminObject.delete()
        
        # remove all barriers
        self.removeAccessBarrier(emailToFree=adminObject.adminEmailAddress)
        
        
        return adminName
    
    def getAdminDetail(self, adminId):
        adminObject = get_object_or_404(AdminNextOfKins, pk=adminId)
        
        # get admin permissions
        attachedPermissions = adminObject.assigned_permissions
        
        presentDetail = {
            'name': adminObject.adminUserName,
            'email': adminObject.adminEmailAddress,
            'id': adminObject.pk,
            'permissions': {
                'website': attachedPermissions.websiteEditor,
                'blog': attachedPermissions.blogEditor,
                'pages': attachedPermissions.thirdPartyEditor,
                'comms': attachedPermissions.commUtilities                
            }
        }
        
        return presentDetail
        
    
    def getAccessDetailOfAdmin(self, requestObject:HttpRequest):
        # get the user object
        attachedAdminObject = requestObject.user
        
        # check if its an secondary administrator
        hasItemObject = NextOfKinItem.objects.filter(associatedUserObject=attachedAdminObject).first()
        
        if hasItemObject:
            # extract the admin access catalog
            adminAccess = hasItemObject.associatedPermissions.getPresentPermissions()
            
        else:
            # all rights present for the primary administrator
            adminAccess = {
                'website': True,
                'blog': True,
                'pages': True,
                'comms': True,
                'users': True
                }
            
        
            
        # record the permissions in the session
        requestObject.session['allowed_pages'] = adminAccess
        
        # print("Added:", requestObject.session['allowed_pages'])
        
        return
        
        
    
    def doesNotHaveProfile(self, adminObject):
        # check if they have a profile
        adminHasNoProfile = True
        
        try:
            profileObject = adminObject.assigned_permissions.their_user_profile
            
            adminHasNoProfile = False if profileObject else True
            
        except:
            # if it has object
            pass
        
        return adminHasNoProfile
            
    
    def getPresentAdminsCatalog(self):
        allAdmins = AdminNextOfKins.objects.all()
        
        # determine password issuance
        passwordIssuance = lambda adminObject:adminObject.assigned_permissions.hasPermissions() and self.doesNotHaveProfile(adminObject=adminObject)
        
        adminsInfo = [
            {
                'date': eachAdmin.addedDate.strftime("%b-%d-%Y, %H:%M %p"),
                'name': eachAdmin.adminUserName,
                'email': eachAdmin.adminEmailAddress,
                'password_issuance': passwordIssuance(adminObject=eachAdmin),
                'id': eachAdmin.pk 
                
            } for eachAdmin in allAdmins
        ]
        
        return adminsInfo


class AdminUtilities:
    def __init__(self, request:HttpRequest):
        self.requestObject = request
        
        self.submittedRequestData = request.POST.dict()
        

    def alterUserPassword(self):
        # validate match
        doPasswordsMatch = self.submittedRequestData['confirm-new-key'] == self.submittedRequestData['user-new-key']
        
        if doPasswordsMatch is True:
            pass
        
        else:
            # alert 
            messages.error(self.requestObject, f"New password and its confirmation password dont match ! 😫")

            return
        
        # get the admin id
        userId = self.submittedRequestData['user-id-tag']
        
        # get the user instance object
        userObject = get_object_or_404(User, pk=int(userId))
        
        # get current key
        currentKey = self.submittedRequestData['user-current-password']
        
        
        if userObject.check_password(raw_password=currentKey):
            # get new key
            newPassword = self.submittedRequestData['user-new-key']
            
            # change the password then
            userObject.set_password(raw_password=newPassword)
            
            userObject.save()
            
            
            # alert okay
            messages.success(self.requestObject, f"Your password was changed successfully! 🥳")
        
        else:
            # alert wrong credentials
            messages.error(self.requestObject, f"Invalid credentials please try again ! 😫")
            
            
        
        return
        
        
    
    def alterAdminPassword(self):
        # get the admin id
        adminId = self.submittedRequestData['admin-id-tag']
        
        # get the admin instance object
        adminObject = get_object_or_404(User, pk=int(adminId))
        
        # get current key
        currentKey = self.submittedRequestData['admin-current-password']
        
        
        if adminObject.check_password(raw_password=currentKey):
            # get new key
            newPassword = self.submittedRequestData['admin-new-key']
            
            # change the password then
            adminObject.set_password(raw_password=newPassword)
            
            adminObject.save()
            
            
            # alert okay
            messages.success(self.requestObject, f"Your password was changed successfully! 🥳")
        
        else:
            # alert wrong credentials
            messages.error(self.requestObject, f"Invalid credentials please try again ! 😫")
            
            
        
        return
            
            


        
    
    def accessWriteRoutine(self, adminEmail, adminName):
        # get a password
        assignedPassword = AdminTools().generateTemporaryPassword()
        
        # create  & save the admin instance
        newAdminUser = User.objects.create(email=adminEmail, username=adminName)
        
        newAdminUser.set_password(assignedPassword)
        
        newAdminUser.is_superuser = True
        
        newAdminUser.save()
        
        return newAdminUser, assignedPassword
        
    
    def grantAdminLoginAccess(self, idOfAdmin):        
        # get the admin instance object
        adminObject = get_object_or_404(AdminNextOfKins, pk=idOfAdmin)
        
        # check if user has permissions
        hasSomeAccess = adminObject.assigned_permissions.hasPermissions()
        
        if hasSomeAccess is True:
            pass
        
        else:
            return False, None
        
        referenceAdminEmail = adminObject.adminEmailAddress
        
        referenceAdminName = adminObject.adminUserName
        
        # write the admin
        adminUserInstance, givenPassword = self.accessWriteRoutine(
            adminEmail=referenceAdminEmail,
            adminName=referenceAdminName)
        
        # create a next of kin entry
        userPermissions = adminObject.assigned_permissions
        
        newKinEntry = NextOfKinItem.objects.create(associatedUserObject=adminUserInstance, associatedPermissions=userPermissions)
        
        newKinEntry.save()
        
        # print('Email used:', referenceAdminEmail)
        
        # remove barrier
        AdminTools().removeAccessBarrier(emailToFree=referenceAdminEmail)
        
        # password message
        passwordMail = f"Hey {referenceAdminName}, Hope all is well, \n\nThis email is from Mariahill Gardens Administrators, Below are your access credentials\n\nEmail:{referenceAdminEmail} \n\nPassword: {givenPassword} \n\nUse those credentials to access your administrator account\n\nThank you, Mariahill Team. "
        
        # send email to the administrator
        MessengerUtils().resetCoreEngine(receiverEmail=referenceAdminEmail, messageToSend=passwordMail, emailSubject="YOUR ADMINISTRATOR ACCOUNT CREDENTIALS")
        
        # true - for success
        
        return True, referenceAdminName
        
    
    def alterAdminPermissions(self):
        # get the admin id
        adminId = self.submittedRequestData['admin-id-tag']
        
        # get the admin instance object
        adminObject = get_object_or_404(AdminNextOfKins, pk=int(adminId))
        
        # name
        adminName = adminObject.adminUserName
        
        # permissions
        accessPermissions = adminObject.assigned_permissions
        
        
        # print(self.submittedRequestData)

        # modify the permissions
        accessPermissions.websiteEditor = True if 'website-editor' in self.submittedRequestData else False
            
        accessPermissions.blogEditor = True if 'blog-editor' in self.submittedRequestData else False

        accessPermissions.thirdPartyEditor = True if 'pages-editor' in self.submittedRequestData else False

        accessPermissions.commUtilities = True if 'comms-panel' in self.submittedRequestData else False

        # commit
        accessPermissions.save()
        
        # execute cleanup script
        self.accessProcessor(emailToValidate=adminObject.adminEmailAddress, permissionState=adminObject.assigned_permissions.hasPermissions())
        
        # alert
        messages.success(self.requestObject, f"Permissions for '{adminName}' were updated successfully! ")
        
        return
    
        
    
    
    def accessProcessor(self, emailToValidate, permissionState):
        # check for validity
        if permissionState is False:
            # make an entry
            self.tagEmailAsNotAuthenticated(emailToTag=emailToValidate)
        
        else:
            # check for entry
            blockingObject = NotAccessibleYet.objects.filter(adminEmailAddress=emailToValidate).first()

            if blockingObject is None:
                # already has access
                pass
            
            else:
                # check if user has an account yet
                userHasAccount = User.objects.filter(email=emailToValidate).first()
                
                if userHasAccount:
                    # has an account 
                    # and is now clear
                    blockingObject.delete()
                    
                else:
                    # they cant be cleared till they have an account
                    # admin must issue them credentials via email
                    pass
                
        return
            

        
    
    def writeNewAdminDetail(self, adminEmail, adminUserName):
        # create a new admin object
        newAdmin = AdminNextOfKins.objects.create()
        
        newAdmin.adminUserName = adminUserName
        
        newAdmin.adminEmailAddress = adminEmail
        
        # save the admin
        newAdmin.save()
        
        # after create a permissions object
        adminRoles = AdminPermissions.objects.create(associatedAdmin=newAdmin)
        
        adminRoles.save()
        
        # tag the user as not yet authenticated
        self.tagEmailAsNotAuthenticated(emailToTag=adminEmail)
        
        return
    
    def tagEmailAsNotAuthenticated(self, emailToTag):
        # create a new entry
        notYetEligibleObject = NotAccessibleYet.objects.create(adminEmailAddress=emailToTag)
        
        # save the object
        notYetEligibleObject.save()
        
        return
        
    
    def registerNewAdmin(self):
        # get email
        submittedEmail = self.submittedRequestData['admin-user-email']
        
        # validate
        isPresent = True if (AdminNextOfKins.objects.filter(adminEmailAddress=submittedEmail).first() or User.objects.filter(email=submittedEmail).first()) else False
        
        if isPresent is True:
            # alert
            messages.warning(self.requestObject, "Email address provided already exists for some User Already 😔")
            
        else:
            # go ahead and save the admin
            submittedUserName = self.submittedRequestData['admin-user-name'].title()
            
            # register the admin
            self.writeNewAdminDetail(adminEmail=submittedEmail, adminUserName=submittedUserName)
            
            # alert success
            messages.success(self.requestObject, f"The admin '{submittedUserName}' was added successfully! ")
            
        return
            

        
        