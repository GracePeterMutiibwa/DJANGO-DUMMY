const bookingApprovalPanel = document.getElementById('booking-approval-panel');

// get the fields
const bookingClientName= document.getElementById('booking-client-name');

const bookingClientEmail= document.getElementById('booking-client-email');

const bookingClientCategory = document.getElementById('booking-client-category');

const bookingClientDetails = document.getElementById('booking-client-details');

// date and time
const startDateHolder = document.getElementById('start-date-holder');

const endDateHolder = document.getElementById('end-date-holder');

const startTimeHolder = document.getElementById('start-time-show');

const endTimeHolder = document.getElementById('end-time-show');

// periods
const daysCountHolder = document.getElementById('days-of-event');

const guestCountHolder = document.getElementById('guests-of-event');

// trigger
const paymentButton = document.getElementById('payment-issue-trigger');

// id store
const idHolder = document.getElementById('id-holder');

const paymentConfirmationModel = document.getElementById('linkConfirmationIssuance');

const paymentConfirmationProceed = document.getElementById('accept-link-issuance');

const paymentLinkAccepted = document.getElementById('payment-link-accepted');

var modelInstance;


function loadAndDisplayRequestInfo(requestMetaInfo){
    // get the data
    let clientName = requestMetaInfo.name;

    let clientEmail = requestMetaInfo.email;

    let eventCategory = requestMetaInfo.category;

    let eventDetails = requestMetaInfo.details;

    // admin view
    // dates
    let startDate = requestMetaInfo.sDate;

    let endDate = requestMetaInfo.eDate;

    // times
    let startTime = requestMetaInfo.start;

    let endTime = requestMetaInfo.stop;

    // period
    let numberOfDays = requestMetaInfo.days;

    let guestNumber = requestMetaInfo.guests;

    
    // load
    bookingClientName.value = clientName;

    bookingClientEmail.value = clientEmail;

    bookingClientCategory.value = eventCategory

    bookingClientDetails.innerHTML = eventDetails;

    // dates
    startDateHolder.innerHTML = startDate;

    endDateHolder.innerHTML = endDate;

    // times
    startTimeHolder.innerHTML = startTime;

    endTimeHolder.innerHTML = endTime;

    // periods
    daysCountHolder.value = `${numberOfDays}`;

    guestCountHolder.value = `${guestNumber}`;

    // extra info
    let requestId = requestMetaInfo.id;

    // update the value
    idHolder.value = `${requestId}`;
}

function getBookingRequestDetails(bookingId, validityToken){
    // create a form
    var fetchForm = new FormData();

    // add the data
    fetchForm.append("booking-id", bookingId);

    // prepare to send
    var xmlHttpRequest = new XMLHttpRequest();

    // bridge to the server
    xmlHttpRequest.open("POST", "/accounts/find-request-details/");

    // add the validation headers
    xmlHttpRequest.setRequestHeader("X-CSRFToken", validityToken);

    // accept json response
    xmlHttpRequest.setRequestHeader("Accept", "application/json");

    // track changes
    xmlHttpRequest.onload = ()=>{
        if (xmlHttpRequest.status == 200){
            // get the page data
            var gottenData = JSON.parse(xmlHttpRequest.responseText);

            // debug
            console.log(gottenData.info);

            // load and display booking request information
            loadAndDisplayRequestInfo(gottenData.info);

        } else {
            // alert network issues
            console.log("Network Issues");
            
        }
    };

    // send
    xmlHttpRequest.send(fetchForm);

}


document.addEventListener('DOMContentLoaded', ()=>{
    // 
    var bookingApprovals = document.querySelectorAll(".booking-approval-trigger");

    bookingApprovals.forEach(eachBookingApproval => {
        eachBookingApproval.addEventListener('click', (clickEvent)=>{
            clickEvent.preventDefault();

            // get the attached id
            let attachedRequestId = eachBookingApproval.getAttribute('attached-booking');

            // get the form and token
            let formWithToken = document.getElementById(`form-${attachedRequestId}`);

            let validationToken = formWithToken.querySelector("input[name='csrfmiddlewaretoken']").value;

            // console.log('Token:', validationToken);

            getBookingRequestDetails(attachedRequestId, validationToken);

            // display the panel
            let panelInstance = new bootstrap.Offcanvas(bookingApprovalPanel);

            // display the panel
            panelInstance.show();
        });
            
    });

    paymentButton.addEventListener('click', buttonClickEvent => {
        modelInstance = new bootstrap.Modal(paymentConfirmationModel);

        modelInstance.show();
    });

    paymentConfirmationProceed.addEventListener('click', proceedEvent => {
        // close the modal
        modelInstance.hide();

        // proceed with submission of the link
        paymentLinkAccepted.click();
    });



});