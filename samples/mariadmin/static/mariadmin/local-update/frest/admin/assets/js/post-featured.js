function updatePostFeaturedState(postId, postState, validityToken){
    // status show
    var statusShowLabel = document.getElementById("feature-update-alert");

    // create a form
    var newForm = new FormData();

    // add the data
    newForm.append("post-id", postId);

    newForm.append("featured-state", postState);

    // prepare to send
    var xmlHttpRequest = new XMLHttpRequest();

    // bridge to the server
    xmlHttpRequest.open("POST", "/update-post-state/");

    // add the validation headers
    xmlHttpRequest.setRequestHeader("X-CSRFToken", validityToken);

    // track changes
    xmlHttpRequest.onload = ()=>{
        if (xmlHttpRequest.status == 200){

            // alert success
            statusShowLabel.innerHTML = `The state of the Post was updated successfully!`;
            

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
    var allFeaturedTriggers = document.querySelectorAll(".post-featured");

    if (allFeaturedTriggers){
        // track each
        allFeaturedTriggers.forEach(eachFeaturedButton =>{
            // listen for toggle
            eachFeaturedButton.addEventListener('change', function(event){
                // get current state
                var currentPostState = eachFeaturedButton.checked;

                // get associated venue object
                var associatedPostItemId = eachFeaturedButton.getAttribute("data-post-tag");

                // get a token
                var formToUse = document.querySelector(`form[data-post-form="${associatedPostItemId}"]`);

                var middlewareToken = formToUse.querySelector('input[name=csrfmiddlewaretoken]').value;

                // console.log('Token:', middlewareToken);

                // update the venue object
                updatePostFeaturedState(associatedPostItemId, currentPostState, middlewareToken);
            });
        });

    } else {
        // do nothing
    }
});