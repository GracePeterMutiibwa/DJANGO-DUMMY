function updateVenueFeaturedState(venueId, venueState, validityToken){
    // get name of venue
    var venueName = document.querySelector(`td[data-venue-form="${venueId}"]`).textContent;

    // status show
    var statusShowLabel = document.getElementById("feature-update-alert");

    // create a form
    var newForm = new FormData();

    // add the data
    newForm.append("venue-id", venueId);

    newForm.append("featured-state", venueState);

    // prepare to send
    var xmlHttpRequest = new XMLHttpRequest();

    // bridge to the server
    xmlHttpRequest.open("POST", "/update-venue/");

    // add the validation headers
    xmlHttpRequest.setRequestHeader("X-CSRFToken", validityToken);

    // track changes
    xmlHttpRequest.onload = ()=>{
        if (xmlHttpRequest.status == 200){

            // alert success
            statusShowLabel.innerHTML = `The state of the venue ${venueName} was updated successfully!`;
            

        } else {
            // alert network issues
            statusShowLabel.innerHTML = "No Internet connection detected, please try again";

        }
    };

    // send
    xmlHttpRequest.send(newForm);

}

document.addEventListener('DOMContentLoaded', ()=>{
    // get all featured triggers if any
    var allFeaturedTriggers = document.querySelectorAll(".venue-featured");

    if (allFeaturedTriggers){
        // track each
        allFeaturedTriggers.forEach(eachFeaturedButton =>{
            // listen for toggle
            eachFeaturedButton.addEventListener('change', function(event){
                // get current state
                var currentState = eachFeaturedButton.checked;

                // get associated venue object
                var associatedVenueId = eachFeaturedButton.getAttribute("data-venue-tag");

                // get a token
                var formToUse = document.querySelector(`form[data-venue-form="${associatedVenueId}"]`);

                var middlewareToken = formToUse.querySelector('input[name=csrfmiddlewaretoken]').value;

                // console.log('Token:', middlewareToken);

                // update the venue object
                updateVenueFeaturedState(associatedVenueId, currentState, middlewareToken);
            });
        });

    } else {
        // do nothing
    }
});