function updateGalleryItemFeaturedState(imageItemId, currentImageState, validityToken){
    // status show
    var statusShowLabel = document.getElementById("feature-gallery-update-alert");

    // create a form
    var newForm = new FormData();

    // add the data
    newForm.append("gallery-image-id", imageItemId);

    newForm.append("featured-state", currentImageState);

    // prepare to send
    var xmlHttpRequest = new XMLHttpRequest();

    // bridge to the server
    xmlHttpRequest.open("POST", "/update-image-state/");

    // add the validation headers
    xmlHttpRequest.setRequestHeader("X-CSRFToken", validityToken);

    // track changes
    xmlHttpRequest.onload = ()=>{
        if (xmlHttpRequest.status == 200){

            // alert success
            statusShowLabel.innerHTML = `The state of the Image was updated successfully!`;
            

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
    var allFeaturedTriggers = document.querySelectorAll(".gallery-image-toggle");

    if (allFeaturedTriggers){
        // track each
        allFeaturedTriggers.forEach(eachFeaturedButton =>{
            // listen for toggle
            eachFeaturedButton.addEventListener('change', function(event){
                // get current state
                var currentImageState = eachFeaturedButton.checked;

                // get associated venue object
                var associatedImageItemId = eachFeaturedButton.getAttribute("data-image-tag");

                // get a token
                var formToUse = document.querySelector(`form[data-gallery-form="${associatedImageItemId}"]`);

                var middlewareToken = formToUse.querySelector('input[name=csrfmiddlewaretoken]').value;

                // console.log('Token:', middlewareToken, "Id=", associatedImageItemId);

                // update the venue object
                updateGalleryItemFeaturedState(associatedImageItemId, currentImageState, middlewareToken);
            });
        });

    } else {
        // do nothing
    }
});