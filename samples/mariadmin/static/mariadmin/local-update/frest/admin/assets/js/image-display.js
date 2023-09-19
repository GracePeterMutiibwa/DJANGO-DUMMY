// global declaration
var bootstrapModalInstance;

document.addEventListener('DOMContentLoaded', ()=>{
    var modalCloseButton = document.getElementById("imageViewerCloseButton");

    // get all trigger buttons
    document.querySelectorAll('.image-display-trigger').forEach(eachButton =>{
        eachButton.addEventListener('click', (clickEvent)=>{
            // if its an anchor tag prevent submission
            clickEvent.preventDefault();

            // get the id
            var imageUrl = eachButton.getAttribute('data-image-url');

            // get the modal image element
            document.getElementById("modal-image-display").setAttribute("src", imageUrl);

            // get the modal
            var previewModal = document.getElementById("image-display-modal");

            // create a bootstrap modal
            bootstrapModalInstance = new bootstrap.Modal(previewModal);

            // display the modal
            bootstrapModalInstance.show();


        });

    });

    // get the modal close button
    modalCloseButton.addEventListener('click', (event)=>{
        // close the modal
        bootstrapModalInstance.hide();

        // clean the image preview button
        document.getElementById("modal-image-display").setAttribute("src", "");
    }); 

});

