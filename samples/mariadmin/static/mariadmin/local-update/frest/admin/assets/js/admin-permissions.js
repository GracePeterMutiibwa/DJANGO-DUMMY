
/**
 * 
 * @param {object} detailObject - Get details of the administrator
 */
function loadAndDisplayAdminDetail(detailObject){
    // get the name and email
    let adminName = detailObject.name;

    let adminEmail = detailObject.email;

    // get the permissions
    let websiteAccess = detailObject.permissions.website;

    let blogAccess = detailObject.permissions.blog;

    let pagesAccess = detailObject.permissions.pages;

    let commsAccess = detailObject.permissions.comms;

    // id
    let adminIdTag = detailObject.id;

    // render the data
    document.getElementById("admin-user-name-input").value = adminName;

    document.getElementById("admin-user-email-input").value = adminEmail;

    // load access
    document.getElementById("website-access-input").checked = websiteAccess;

    document.getElementById("website-blog-input").checked = blogAccess;

    document.getElementById("third-parties-input").checked = pagesAccess;

    document.getElementById("site-comms-input").checked = commsAccess;

    // get the associated id
    document.getElementById("id-tag-hold").value = adminIdTag;

    // get viewer
    var adminDetailViewer = new bootstrap.Offcanvas(document.getElementById("admin-permissions-manager"));

    // display the viewer
    adminDetailViewer.show();

}

/**
 * 
 * @param {string} idOfAdmin - Id of the administrator
 * @param {string} validityToken - Token for validation
 */
function fetchAndDisplayAdminDetails(idOfAdmin, validityToken){
    // get the details
    var formToSubmit = new FormData();

    // add the id
    formToSubmit.append('admin-id', idOfAdmin);

    // create a request
    var xmlHttpRequest = new XMLHttpRequest();

    // open the request
    xmlHttpRequest.open("POST", "/get-admin-profile/");

    // add headers
    xmlHttpRequest.setRequestHeader("X-CSRFToken", validityToken);

    xmlHttpRequest.setRequestHeader("Accept", "application/json");

    // wait for the load of request object
    xmlHttpRequest.onload = ()=>{
        if (xmlHttpRequest.status == 200){
            // extract the json data
            var returnedJsonData = JSON.parse(xmlHttpRequest.responseText);

            // debug point
            // console.log('Data:', returnedJsonData);

            // load
            loadAndDisplayAdminDetail(returnedJsonData.info);



        } else {
            // alert
            document.getElementById("error-alert-label").innerHTML = "Ensure that you have internet access!";
        }
    };

    // send the request
    xmlHttpRequest.send(formToSubmit);

}



document.addEventListener('DOMContentLoaded', ()=>{
    // track click
    var allAdminTogglers = document.querySelectorAll(".manage-admin-toggler");

    allAdminTogglers.forEach(eachToggler => {
        // avoid submission
        eachToggler.addEventListener('click', (clickEvent)=>{
            // prevent submission of the form
            clickEvent.preventDefault();

            // get the associated user id
            let associateAdminId = eachToggler.getAttribute("data-admin-id");

            // get validity token
            let attachedForm = document.getElementById(`fetch-${associateAdminId}`);

            let validityToken = attachedForm.querySelector('input[name="csrfmiddlewaretoken"]').value;

            // console.log(`id=${associateAdminId}, Token=${validityToken}`);

            // fetch admin details
            fetchAndDisplayAdminDetails(associateAdminId, validityToken);

        });
    });
});