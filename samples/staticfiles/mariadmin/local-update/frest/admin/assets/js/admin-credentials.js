document.addEventListener('DOMContentLoaded', ()=>{
    // track click
    var settingsToggler = document.getElementById("change-admin-password");

    // avoid submission
    settingsToggler.addEventListener('click', (clickEvent)=>{
        // prevent submission of the form
        clickEvent.preventDefault();

        // get the associated admin id
        let associatedAdminId = settingsToggler.getAttribute("data-admin-tag");

        let associateAdminEmail = settingsToggler.getAttribute("data-admin-email");

        let associateAdminName = settingsToggler.getAttribute("data-admin-username");

        // load the data
        document.getElementById("admin-tag-key").value = associatedAdminId;

        document.getElementById("admin-user-name-input").value = associateAdminName;

        document.getElementById("admin-user-email-input").value = associateAdminEmail;


        // get viewer
        var alterPasswordViewer = new bootstrap.Offcanvas(document.getElementById("admin-manage-credentials"));

        // display the viewer
        alterPasswordViewer.show();

    })

});