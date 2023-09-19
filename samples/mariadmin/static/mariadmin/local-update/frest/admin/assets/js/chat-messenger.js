// access the form and the message area
var chatMessageForm = document.querySelector(".form-send-message");

var messageArea = document.querySelector(".message-input");

var avatarPresence = document.querySelector(".image-store");


function scrollToNewMessage() {
    // get the message body 
    var chatBody = document.querySelector(".chat-history-body");
    
    // scroll to the newest message
    chatBody.scrollTo(0, chatBody.scrollHeight);
}


function messageRelay(messageToSend, validityToken){
    // create a form
    var newForm = new FormData();

    // add the message to the form
    newForm.append("message", messageToSend);

    // prepare to send
    var xmlHttpRequest = new XMLHttpRequest();

    // bridge to the server
    xmlHttpRequest.open("POST", "/submit-message/2/");

    // add the validation headers
    xmlHttpRequest.setRequestHeader("X-CSRFToken", validityToken);

    // track changes
    xmlHttpRequest.onload = ()=>{
        if (xmlHttpRequest.status == 200){

            // check for hidden delete
            var deleteIconHolder = document.getElementById("delete-icon-holder");

            if (deleteIconHolder.classList.contains("d-none")){
                // make the delete button visible
                document.getElementById("delete-icon-holder").classList.remove("d-none");

            } else {
                // do nothing about it
            }


        } else {
            // alert network issues
            // console.log('Connection failed');
        }
    };

    // send
    xmlHttpRequest.send(newForm);

}

// manage any form submissions
chatMessageForm.addEventListener("submit", (submittedFormEvent) => {
    // prevent the form submission
    submittedFormEvent.preventDefault();

    // get the submitted form message
    var submittedMessage = messageArea.value.trim();

    if (submittedMessage.length > 0){
        // get the validity token
        var validationCode = chatMessageForm.querySelector('input[name="csrfmiddlewaretoken"]').value;

        // debug
        // console.log("Token:", validationCode);

        // send the message to the server
        messageRelay(submittedMessage, validationCode);

        // then show the message on the users end

        // create a temporary div element
        var temporaryDivElement = document.createElement("div");

        
        // add the necessary classes to the message node
        temporaryDivElement.classList.add("chat-message");
        temporaryDivElement.classList.add("chat-message-right");

        // get image status
        var imageStatus = avatarPresence.getAttribute("data-image-status");

        // get the image container
        var imageUrl = avatarPresence.getAttribute("data-image-url");

        if (imageStatus === "present"){
            // get the image
            var imageNode = `
                            <div class="user-avatar flex-shrink-0 ms-3">
                                <div class="avatar avatar-sm">
                                    <img src="${imageUrl}" alt="Avatar" class="rounded-circle">
                                </div>
                            </div>`;

        } else {
            // extract the users initials
            var userInitials = imageUrl.split(" ")[0][0].toUpperCase();

            var imageNode = `
                            <div class="avatar me-2">
                                <span class="avatar-initial rounded-circle bg-label-success">
                                    ${userInitials}
                                </span>
                            </div>
                            `;
        }
        
        // get the current time
        var currentDateTimeObject = new Date();

        // get the time
        var currentHours = currentDateTimeObject.getHours();

        var currentMinutes = currentDateTimeObject.getMinutes();

        // load the data components
        temporaryDivElement.innerHTML = `
                                    <div class="d-flex overflow-hidden">
                                        <div class="chat-message-wrapper flex-grow-1">
                                            <div class="chat-message-text">
                                                <p class="mb-0">${submittedMessage}</p>
                                            </div>
                                            <div class="text-end text-muted mt-1">
                                                <small>${currentHours}:${currentMinutes}</small>
                                            </div>
                                        </div>
                                        <div class="user-avatar flex-shrink-0 ms-3">
                                            ${imageNode}
                                        </div>
                                    </div>`;

        // add the message to last message wrapper
        document.querySelector("#chats-holder-container").appendChild(temporaryDivElement);

        
        // wipe the message input area
        messageArea.value = ""

        // scroll to the new message
        scrollToNewMessage();

    }else{
        return;
    }



});