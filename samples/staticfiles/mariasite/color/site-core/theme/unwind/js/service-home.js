document.addEventListener('DOMContentLoaded', ()=>{
        // get all present service viewer buttons
        var allServiceViewButtons = document.querySelectorAll('.show-service');

        if (allServiceViewButtons){
            allServiceViewButtons.forEach(viewServiceButton => {
            
                // track their clicks
                viewServiceButton.addEventListener('click', (viewClickEvent)=>{
                    // stop reload
                    viewClickEvent.preventDefault();
        
                    // get the service name
                    // var serviceName = viewServiceButton.getAttribute("data-service-name");

                    // console.log('i was clicked', serviceName);
        
                    // get the details
                    // var serviceDetails = viewClickEvent.target.getAttribute("data-service-details");
        
                    // update modal details
                    // document.getElementById("service-name-modal").innerHTML = serviceName;
        
                    // document.getElementById("service-details-modal").innerHTML = serviceDetails;
        
                    // get the modal
                    // viewerModal = new bootstrap.Modal(document.getElementById("display-service"));
        
                    // display the modal
                    // viewerModal.show();
                });
            });

            // close button
            // document.getElementById("serviceModalCloseButton").addEventListener("click", ()=>{
            //     viewerModal.hide();
        
        
            // });


    
        }
    

});