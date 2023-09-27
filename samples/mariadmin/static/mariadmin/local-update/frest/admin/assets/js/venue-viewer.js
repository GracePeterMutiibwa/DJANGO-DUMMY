

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


            // get viewer
            var venueViewer = new bootstrap.Offcanvas(document.getElementById("venue-image-details"));

            // display the viewer
            venueViewer.show();

        });

    }
}

function displayVenueEditInformation(venueEditInformation){
    // first reset the form
    document.getElementById("venues-register-form").reset();

    // then load the info
    let venueName = venueEditInformation.name;

    let venueDescription = venueEditInformation.description;

    let venueCapacity = venueEditInformation.capacity;

    let venueContact = venueEditInformation.contact;

    let venueId = venueEditInformation.id;

    // categories last
    let presentCategories = venueEditInformation.categories;


    // load the information
    document.getElementById("venue-name-entry").value = venueName;

    document.getElementById("venue-description-entry").value = venueDescription;

    document.getElementById("venue-capacity-entry").value = venueCapacity;

    // validate contact
    if (venueContact !== "Missing"){
        document.getElementById("venue-contact-entry").value = venueContact;
    }
    

    // load the categories
    presentCategories.forEach(eachCategory =>{
        // get the option
        let optionHolder = document.querySelector(`.form-check-input[name='${eachCategory}']`);

        if (optionHolder){
            optionHolder.checked = true;
        } else{
            // ignore
        }

    });


    // load edit button
    let temporaryIdHolder = document.createElement('input');

    temporaryIdHolder.setAttribute('name', 'venue-edit-id');

    temporaryIdHolder.setAttribute('type', 'hidden');

    temporaryIdHolder.value = venueId;

    // document.getElementById("venue-name-entry").value = venueName;
    document.getElementById("venue-detail-edit-holder").innerHTML = temporaryIdHolder.outerHTML;
    

    // display edit environment
    let editCancelButton = document.getElementById("venue-edit-cancel");

    let editFormSubmitter  = document.getElementById("venue-edit-submitter");

    // env
    if (editCancelButton.classList.contains('d-none')){
        // unhide
        editCancelButton.classList.remove('d-none');

        // fit
        editFormSubmitter.classList.remove('w-100');

    } else {

    }
    

}

function getAndDisplayEditDetails(venueId, validityToken){
    // create a form
    var newForm = new FormData();

    // add the data
    newForm.append("venue-id", venueId);

    // prepare to send
    var xmlHttpRequest = new XMLHttpRequest();

    // bridge to the server
    xmlHttpRequest.open("POST", "/fetch-venue-edit-details/");

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
            displayVenueEditInformation(foundVenueInformation.info);
            

        } else {
            // alert network issues
            document.getElementById("feature-update-alert").innerHTML = "No Internet connection detected, please try again";

        }
    };

    // send
    xmlHttpRequest.send(newForm);

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

    var venueEditTriggers = document.querySelectorAll(".venue-detail-trigger");

    var venueEditCancelButton = document.getElementById("venue-edit-cancel");

    // get cancel edit trigger
    venueEditCancelButton.addEventListener('click', (cancelEvent)=>{
        // stop submission
        cancelEvent.preventDefault();

        // hide
        venueEditCancelButton.classList.add('d-none');

        // fit
        document.getElementById("venue-edit-submitter").classList.add('w-100');

        // wipe id holder
        document.getElementById("venue-detail-edit-holder").innerHTML = "";

        // reset the form
        document.getElementById("venues-register-form").reset();

    });

    // track edit triggers
    venueEditTriggers.forEach(eachImageEditTrigger =>{
        // listen for click
        eachImageEditTrigger.addEventListener('click', function(clickEvent){
            // stop default behaviour
            clickEvent.preventDefault();

            // get the attached venue id
            let attachedVenueId = eachImageEditTrigger.getAttribute("data-edit-id");

            // form
            let attachedForm = document.getElementById("venue-token-form");

            let validityToken = attachedForm.querySelector("input[name='csrfmiddlewaretoken']").value;
        
            // console.log(`id=${attachedVenueId}, Token=${validityToken}`);

            // display edit details
            getAndDisplayEditDetails(attachedVenueId, validityToken);
        });

    });

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