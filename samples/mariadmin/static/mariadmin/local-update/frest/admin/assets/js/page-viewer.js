
/**
 * 
 * @param {*} whatSection - 1 for category, 2 - for District
 * @param {*} objectToSelect - Either a category or district
 */
function selectGivenOption(whatSection, objectToSelect){
    if (whatSection === 1){
        // get category selector
        var optionSelector = document.getElementById("page-category-input");

    } else {
        // get the district selector
        var optionSelector = document.getElementById("business-location-input");

    }

    // get the category option
    let optionToSelect = optionSelector.querySelector(`option[value="${objectToSelect}"]`);


    // select the category or district
    optionToSelect.selected = true;

}

/**
 * @param {object} pageMetaInfo - Retrieved page information
 */
function loadAndDisplayPageInfo(pageMetaInfo){
    // get the data
    let pageName = pageMetaInfo.name;

    let pageDescription = pageMetaInfo.description;

    let pageCategory = pageMetaInfo.category;

    let businessLocation = pageMetaInfo.district;

    let businessLogo = pageMetaInfo.image;

    // console.log("District:", businessLocation);

    let pageTag = pageMetaInfo.id;

    let pageVisibility = pageMetaInfo.visible;

    

    // load
    document.getElementById("page-name-input").value = pageName;

    document.getElementById("page-description-input").value = pageDescription;

    document.getElementById("page-id-holder").value = pageTag;

    document.getElementById("page-image-holder-input").value = businessLogo;

    // select the category
    selectGivenOption(1, pageCategory);

    // select the district
    selectGivenOption(2, businessLocation);


    // page visibility
    document.getElementById("page-visibility-input").checked = pageVisibility;

    // debug
    // console.log("So far so good");

    // get viewer
    var pageViewer = new bootstrap.Offcanvas(document.getElementById("view-page-details"));

    // display the viewer
    pageViewer.show();

}

/**
 * 
 * @param {number} pageId - id of the page to get
 * @param {string} validityToken - token for server validation
 */
function getPageInformation(pageId, validityToken){
    // create a form
    var newForm = new FormData();

    // add the data
    newForm.append("page-id", pageId);

    // prepare to send
    var xmlHttpRequest = new XMLHttpRequest();

    // bridge to the server
    xmlHttpRequest.open("POST", "/get-page-data/");

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
            loadAndDisplayPageInfo(gottenData.info);

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
    var pageViewTriggers = document.querySelectorAll(".page-viewer-trigger");

    // track clicks onto them
    pageViewTriggers.forEach(pageViewerTrigger => {

        // each
        pageViewerTrigger.addEventListener('click', (clickEvent)=>{
            // prevent submission
            clickEvent.preventDefault();

            // get attached id
            let attachedPageId = pageViewerTrigger.getAttribute("data-page-id");

            // get form associated
            let associatedForm = document.querySelector(`form#fetch-${attachedPageId}`);

            // get token
            let validationToken = associatedForm.querySelector("input[name='csrfmiddlewaretoken']").value;

            // console.log(`id=${attachedPageId}, Token=${validationToken}`);
            getPageInformation(attachedPageId, validationToken);
        });
    });

});