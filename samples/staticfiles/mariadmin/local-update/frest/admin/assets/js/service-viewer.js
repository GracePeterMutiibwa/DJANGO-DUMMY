// track the modal 
var viewerModal;

// wait for the page to load
document.addEventListener('DOMContentLoaded', ()=>{
    // get all present service viewer buttons
    var allServiceViewButtons = document.querySelectorAll('.service-view-button');

    allServiceViewButtons.forEach(viewServiceButton => {
        // track their clicks
        viewServiceButton.addEventListener('click', (viewClickEvent)=>{
            // get the service name
            var serviceName = viewClickEvent.target.getAttribute("data-service-name");

            // get the details
            var serviceDetails = viewClickEvent.target.getAttribute("data-service-details");

            // update modal details
            document.getElementById("service-name-modal").innerHTML = serviceName;

            document.getElementById("service-details-modal").innerHTML = serviceDetails;

            // get the modal
            viewerModal = new bootstrap.Modal(document.getElementById("display-service"));

            // display the modal
            viewerModal.show();
        });
    });

    // close button
    document.getElementById("serviceModalCloseButton").addEventListener("click", ()=>{
        viewerModal.hide();


    });


});