// access the form and the message area
var chatMessageForm = document.querySelector(".form-send-message");

var messageArea = document.querySelector(".message-input");


function scrollToNewMessage() {
    // get the message body 
    var chatBody = document.querySelector(".chat-history-body");
    
    // scroll to the newest message
    chatBody.scrollTo(0, chatBody.scrollHeight);
}


function messageRelay(messageToSend, validityToken, messageReceiver){
    // create a form
    var newForm = new FormData();

    // add the message to the form
    newForm.append("message", messageToSend);

    newForm.append('receiver', messageReceiver);

    // prepare to send
    var xmlHttpRequest = new XMLHttpRequest();

    // bridge to the server
    xmlHttpRequest.open("POST", "/submit-message/1/");

    // add the validation headers
    xmlHttpRequest.setRequestHeader("X-CSRFToken", validityToken);

    // track changes
    xmlHttpRequest.onload = ()=>{
        if (xmlHttpRequest.status == 200){

            // alert success
            // statusShowLabel.innerHTML = `The state of the venue ${venueName} was updated successfully!`;
            // console.log('message sent');

        } else {
            // alert network issues
            // statusShowLabel.innerHTML = "No Internet connection detected, please try again";
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

        // get the receiver
        var receiver = document.getElementById("user-name-holder").getAttribute("data-user-name");

        // send the message to the server
        messageRelay(submittedMessage, validationCode, receiver);

        // then show the message on the users end

        // create a temporary div element
        var temporaryDivElement = document.createElement("div");

        
        // add the necessary classes to the message node
        temporaryDivElement.classList.add("chat-message");
        temporaryDivElement.classList.add("chat-message-right");

        var imageNode = `
                        <div class="avatar ms-3">
                            <span class="avatar-initial rounded-circle bg-label-info">
                                <i class="bx bx-support"></i>
                            </span>
                        </div>
                        `;

        
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