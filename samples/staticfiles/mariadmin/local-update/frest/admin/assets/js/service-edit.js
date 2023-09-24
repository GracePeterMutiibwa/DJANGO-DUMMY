
function editRegisterModeToggler(toggleMode){
    // get the save holder and cancel
    let saveButtonHolder = document.getElementById("save-button-holder");

    let cancelButtonHolder = document.getElementById("cancel-button-holder");

    if (toggleMode === 1){
        // unhide cancel
        cancelButtonHolder.classList.remove("d-none");

        // occupy half
        saveButtonHolder.classList.remove("col-12");

        saveButtonHolder.classList.add("col-6");

    } else {
        // hide cancel
        cancelButtonHolder.classList.add("d-none");

        // save button fill whole space
        saveButtonHolder.classList.remove("col-6");

        saveButtonHolder.classList.add("col-12");

        // remove edit form trigger
        document.getElementById("assets-area").innerHTML = "";

    }

}

function fillServiceRegisterEditor(){
    // get service details
    let serviceName = document.getElementById("service-name-input").value;

    let serviceBrief = document.getElementById("brief-description-input").value;

    let serviceDetailed = document.getElementById("detailed-description-input").value;

    let serviceImage = document.getElementById("service-image-holder").getAttribute("src");

    // get the id of the service to edit
    let serviceId = document.getElementById("service-tag-holder").value;

    // load them in the editor

    document.getElementById("service-name").value = serviceName;

    document.getElementById("brief-description").value = serviceBrief;

    document.getElementById("detailed-description").value = serviceDetailed;

    document.getElementById("service-image").value = serviceImage;

    // keep track of an id to edit
    let hiddenInput = document.createElement("input");

    hiddenInput.setAttribute("type", "hidden");

    hiddenInput.setAttribute("name", "service-to-edit");

    hiddenInput.setAttribute("value", serviceId);

    // track the id of the service to edit
    document.getElementById("assets-area").innerHTML = hiddenInput.outerHTML;

    // get viewer
    var serviceDetailsViewer = bootstrap.Offcanvas.getInstance(document.getElementById("view-service-details"));

    // display the viewer
    serviceDetailsViewer.hide();

    // change interface
    editRegisterModeToggler(1);



}

// wait for the page to load
document.addEventListener('DOMContentLoaded', ()=>{
    // get the edit trigger
    var editButton = document.getElementById("edit-service-trigger");

    var editCancelButton = document.getElementById("cancel-edit-button");

    // get all details and load them into the service editor
    editButton.addEventListener('click', (clickEvent)=>{
        // fill register Area
        fillServiceRegisterEditor();
    });

    // cancel
    editCancelButton.addEventListener('click', (clickEvent)=>{
        // get form
        let serviceForm = document.getElementById("service-register-form");

        // reset form
        serviceForm.reset();

        // revert to normal
        editRegisterModeToggler(2);

    });

});