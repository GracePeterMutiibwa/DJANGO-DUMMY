

import random

from mariadmin.models import EmailReset

from datetime import timedelta, datetime

from django.http import HttpRequest

from django.contrib.auth.models import User

from .mail_processor import MessengerUtils

class PasswordRestTools:
    def __init__(self, request:HttpRequest):
        self.requestObject = request
        
        self.submittedRequestData = request.POST.dict()
        
    
    def executePasswordResetSequence(self, emailAddress, newPassword):
        # get user
        associatedUser = User.objects.filter(email=emailAddress).first()
        
        # validity
        userIsValid = False
        
        if associatedUser:
            userIsValid = True
            
            # make the changes
            associatedUser.set_password(raw_password=newPassword)
        
            # save the user object
            associatedUser.save()
            
            print("Changed password!")
        
        else:
            pass
    
        
        return userIsValid
        
    def resetUserPassword(self):
        if 'reset-email' in self.submittedRequestData:
            pass
        else:
            # debug
            print("Email missing!")
            
            return None, None
        
        # get teh submitted passwords
        newPassword = self.submittedRequestData['password']
        
        confirmPassword = self.submittedRequestData['confirm-password']
        
        # confirm that they match
        doRawPasswordsMatch = confirmPassword == newPassword
        
        # change was done
        changeSuccessful = False
        
        if doRawPasswordsMatch is True:
            # get the associated email
            associatedEmail = self.submittedRequestData['reset-email']
            
            # perform the reset and get status of the reset
            changeSuccessful = self.executePasswordResetSequence(emailAddress=associatedEmail, newPassword=confirmPassword)
            
        else:
            pass
        
        # print("Change:", changeSuccessful)
            
        return doRawPasswordsMatch, changeSuccessful
    

class CodeValidationUtilities:
    def __init__(self, request:HttpRequest):
        self.requestObject = request
        
        self.submittedRequestData = request.POST.dict()
        
        
    def tokenReconstructor(self):
        # extract and rebuild the token
        digitOne = self.submittedRequestData['first-digit']
        
        digitTwo = self.submittedRequestData['second-digit']
        
        digitThree = self.submittedRequestData['third-digit']
        
        digitFour = self.submittedRequestData['fourth-digit']
        
        digitFive = self.submittedRequestData['fifth-digit']
        
        digitSix = self.submittedRequestData['sixth-digit']
        
        # create  complete token
        completeToken = "".join([
            digitOne, digitTwo, digitThree, digitFour, digitFive, digitSix
            ])
        
        return completeToken
        
    
    def validateResetToken(self):
        # get the complete token
        submittedToken = self.tokenReconstructor()
        
        # get the user email
        userEmail = self.submittedRequestData['user-email']
        
        # validate the token
        resetInstance = EmailReset.objects.filter(attachedEmail=userEmail, generatedCode=submittedToken).first()
        
        if resetInstance:
            # validate expiry
            tokenValidity = resetInstance.timeNotYetExpired()
        
        else:
            # if its invalid alert
            tokenValidity = None
            
        return tokenValidity, userEmail
        
                
        

class ResetUtilities:
    def __init__(self):
        pass
    
    def codeGenerator(self, referenceEmailAddress):
        codeGenerator = lambda: "".join( str(random.randint(0, 9)) for _ in range(6))
                
        # check for validity
        codeValidityObject = EmailReset.objects.filter(attachedEmail=referenceEmailAddress).first()
        
        # received
        receivedAlready = False
        
        if codeValidityObject:
            expiryStatus = codeValidityObject.timeNotYetExpired()
            
            # go a head and check for code validity
            if expiryStatus is False:
                # delete the object and generate a new code
                codeValidityObject.delete()
                
                # new
                newCode = codeGenerator()
                
            else:
                # extract the present code
                receivedAlready = True
                
                # get the current code
                newCode = codeValidityObject.generatedCode
                
        else:
            # generate a new code
            newCode = codeGenerator()
        
        
        return newCode, receivedAlready
    
    def resetMessageMint(self, resetCodeToUse, userName):
        # draft message
        draftedMessage = f"Hello {userName},\n\n Use this code {resetCodeToUse} to reset your password for your Mariahill Gardens Account"
        
        return draftedMessage
    
    
    def createResetEntry(self, userEmail, resetCode):
        # create an expiry time
        expiryTime = datetime.now() + timedelta(minutes=10)
        
        # reset log
        resetEntry = EmailReset.objects.create(expiryTime=expiryTime)
        
        # add details
        resetEntry.attachedEmail = userEmail
        
        resetEntry.generatedCode = resetCode
        
        # save 
        resetEntry.save()
        
        return
        
        
        
        
    # send an email
    def sendResetCode(self, toEmailAddress, nameOfUser):
        # get a code status
        resetCode, receivedStatus = self.codeGenerator(referenceEmailAddress=toEmailAddress)
        
        # response
        # False - Duplicate
        # True - Message Sent
        
        responseCode = False
        
        if receivedStatus is True:
            # duplicate
            pass
        
        else:
            # get a message
            messageToForward = self.resetMessageMint(resetCodeToUse=resetCode, userName=nameOfUser)
            
            # send the code asap
            MessengerUtils().resetCoreEngine(receiverEmail=toEmailAddress, messageToSend=messageToForward, emailSubject="RESET PASSWORD CODE")
            
            # create and entry
            self.createResetEntry(userEmail=toEmailAddress, resetCode=resetCode)
            
            # alert success
            responseCode = True
            
        return responseCode
            
    
    
    



