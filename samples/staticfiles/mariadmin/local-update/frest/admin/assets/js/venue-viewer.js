

function deleteVenueImage(venueImageId, validityToken, venueImageContainer){
    // create a form
    var newForm = new FormData();

    // add the data
    newForm.append("venue-image-id", venueImageId);

    // prepare to send
    var xmlHttpRequest = new XMLHttpRequest();

    // bridge to the server
    xmlHttpRequest.open("POST", "/delete-venue-image/");

    // add the validation headers
    xmlHttpRequest.setRequestHeader("X-CSRFToken", validityToken);

    // track changes
    xmlHttpRequest.onload = ()=>{
        if (xmlHttpRequest.status == 200){
            // delete the object
            venueImageContainer.remove()

            // alert
            var remainingDeleteTriggers = document.querySelectorAll(".image-delete-trigger");

            if (remainingDeleteTriggers.length === 0){
                // alert over
                let missingMessage = `
                                    <div class="d-flex mt-5 p-5 justify-content-center">

                                        <p class="lead">
                                            No Images Yet, add some 😌 !
                                        </p>

                                    </div>`;

                document.getElementById("venue-images-show").innerHTML = missingMessage;

            
            } else {
                // ignore

            }

        } else {
            // ignore alert network issues

        }
    };

    // send
    xmlHttpRequest.send(newForm);

}

function displayVenueImages(venueImageObject){
    // get display section
    var venueImagesDisplay = document.getElementById("venue-images-show");

    if (venueImageObject.length === 0){
        let missingMessage = `
                            <div class="d-flex mt-5 p-5 justify-content-center">

                                <p class="lead">
                                    No Images Yet, add some 😌 !
                                </p>

                            </div>`;

        venueImagesDisplay.innerHTML = missingMessage;

    } else{
        // clear viewer
        venueImagesDisplay.innerHTML = "";


        // load the images
        venueImageObject.forEach(eachImageObject =>{
            // get the details
            let imageUrl = eachImageObject.url;

            let imageId = eachImageObject.id;

            // create a div
            let imageHolder = document.createElement("div");

            imageHolder.classList.add("mb-3");

            imageHolder.setAttribute("data-deletion-tag", imageId);

            let imageContainer = `
                            <button type="button" class="btn btn-primary image-delete-trigger mb-2" data-delete-id="${imageId}">
                                <i class='bx bxs-folder-minus bx-burst-hover me-2'></i> Delete
                            </button>

                            <img src="${imageUrl}" class="img-fluid rounded" alt="#"> `;

            // add image to the container
            imageHolder.innerHTML = imageContainer;

            // append the imag element
            venueImagesDisplay.appendChild(imageHolder);

            // track items
            var allImageDeleteTriggers = document.querySelectorAll(".image-delete-trigger");

            allImageDeleteTriggers.forEach(eachDeleteTrigger =>{
                // listen for click
                eachDeleteTrigger.addEventListener('click', function(event){
                    // get the attached venue id
                    let attachedVenueId = eachDeleteTrigger.getAttribute("data-delete-id");
        
                    // form
                    let attachedForm = document.getElementById("venue-token-form");
        
                    let validityToken = attachedForm.querySelector("input[name='csrfmiddlewaretoken']").value;
                
                    // console.log(`id=${attachedVenueId}, Token=${validityToken}`);

                    // container to delete
                    var imageContainerToDelete = document.querySelector(`div[data-deletion-tag='${attachedVenueId}']`);

                    deleteVenueImage(attachedVenueId, validityToken, imageContainerToDelete);
        
                    
                });
            });

        });

    }
    // get viewer
    var venueViewer = new bootstrap.Offcanvas(document.getElementById("venue-image-details"));

    // display the viewer
    venueViewer.show();
}

function getAndDisplayVenueImages(venueId, validityToken){
    // create a form
    var newForm = new FormData();

    // add the data
    newForm.append("venue-id", venueId);

    // prepare to send
    var xmlHttpRequest = new XMLHttpRequest();

    // bridge to the server
    xmlHttpRequest.open("POST", "/fetch-venue-images/");

    // add the validation headers
    xmlHttpRequest.setRequestHeader("X-CSRFToken", validityToken);

    // track changes
    xmlHttpRequest.onload = ()=>{
        if (xmlHttpRequest.status == 200){
            // get the data
            let foundVenueInformation = JSON.parse(xmlHttpRequest.responseText);

        
            // debug
            // console.log(foundVenueInformation.info);

            // display
            displayVenueImages(foundVenueInformation.info);
            

        } else {
            // alert network issues
            document.getElementById("feature-update-alert").innerHTML = "No Internet connection detected, please try again";

        }
    };

    // send
    xmlHttpRequest.send(newForm);

}

// wait for the page to load
document.addEventListener('DOMContentLoaded', ()=>{
    // get all the venue triggers
    var allVenueTriggers = document.querySelectorAll('.venue-display-trigger');

    allVenueTriggers.forEach(eachVenueTrigger =>{
        // listen for click
        eachVenueTrigger.addEventListener('click', function(event){
            // get the attached venue id
            let attachedVenueId = eachVenueTrigger.getAttribute("data-venue-id");

            // get a closest token
            let attachedForm = document.querySelector(`form[data-venue-form="${attachedVenueId}"]`);

            // attached token
            let validityToken = attachedForm.querySelector("input[name='csrfmiddlewaretoken']").value;

            // debug
            // console.log(`id=${attachedVenueId}, Token=${validityToken}`);

            getAndDisplayVenueImages(attachedVenueId, validityToken);

        });
    });


});