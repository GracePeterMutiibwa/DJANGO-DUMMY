

/**
 * @param {object} serviceMetaInfo - Retrieved page information
 */
function loadAndDisplayServiceInfo(serviceMetaInfo){
    // get the data
    let serviceName = serviceMetaInfo.name;

    let serviceBrief = serviceMetaInfo.brief;

    let serviceDetailed = serviceMetaInfo.detailed;

    let serviceImage = serviceMetaInfo.image;

    let serviceId = serviceMetaInfo.id;

    
    // load
    document.getElementById("service-name-input").value = serviceName;

    document.getElementById("brief-description-input").value = serviceBrief;

    document.getElementById("detailed-description-input").value = serviceDetailed;

    document.getElementById("service-image-holder").setAttribute("src", serviceImage);

    // track the id of the service to edit
    document.getElementById("service-tag-holder").value = serviceId;


    // debug
    // console.log("So far so good");

    // get viewer
    var pageViewer = new bootstrap.Offcanvas(document.getElementById("view-service-details"));

    // display the viewer
    pageViewer.show();

}

/**
 * 
 * @param {number} serviceId - id of the service to get
 * @param {string} validityToken - token for server validation
 */
function getServiceInformation(serviceId, validityToken){
    // create a form
    var newForm = new FormData();

    // add the data
    newForm.append("service-id", serviceId);

    // prepare to send
    var xmlHttpRequest = new XMLHttpRequest();

    // bridge to the server
    xmlHttpRequest.open("POST", "/get-service-meta/");

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
            // console.log(gottenData.info);

            // load and display page information
            loadAndDisplayServiceInfo(gottenData.info);

        } else {
            // alert network issues
            console.log("Network Issues");
            
        }
    };

    // send
    xmlHttpRequest.send(newForm);

}


// wait for the page to load
document.addEventListener('DOMContentLoaded', ()=>{

    // get all trigger buttons
    var pageViewTriggers = document.querySelectorAll(".service-viewer-trigger");

    // track clicks onto them
    pageViewTriggers.forEach(pageViewerTrigger => {

        // each
        pageViewerTrigger.addEventListener('click', (clickEvent)=>{
            // prevent submission
            clickEvent.preventDefault();

            // get attached id
            let attachedServiceId = pageViewerTrigger.getAttribute("data-service-id");

            // get form associated
            let associatedForm = document.querySelector(`form#fetch-${attachedServiceId}`);

            // get token
            let validationToken = associatedForm.querySelector("input[name='csrfmiddlewaretoken']").value;

            // console.log(`id=${attachedServiceId}, Token=${validationToken}`);

            getServiceInformation(attachedServiceId, validationToken);
        });
    });

});