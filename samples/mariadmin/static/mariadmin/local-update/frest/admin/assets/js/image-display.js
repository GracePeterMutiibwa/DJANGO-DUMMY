// global declaration
var imageDisplayCanvasInstance;

document.addEventListener('DOMContentLoaded', ()=>{
    // var modalCloseButton = document.getElementById("imageViewerCloseButton");

    // get all trigger buttons
    document.querySelectorAll('.image-display-trigger').forEach(eachButton =>{
        eachButton.addEventListener('click', (clickEvent)=>{
            // if its an anchor tag prevent submission
            clickEvent.preventDefault();

            // get the id
            var imageUrl = eachButton.getAttribute('data-image-url');

            // get the modal image element
            document.getElementById("image-to-display-holder").setAttribute("src", imageUrl);

            // get the canvas - image-display-modal
            var previewCanvas = document.getElementById("view-image-data");

            // create a bootstrap offcanvas
            imageDisplayCanvasInstance = new bootstrap.Offcanvas(previewCanvas);

            // display the modal
            imageDisplayCanvasInstance.show();


        });

    });


});

