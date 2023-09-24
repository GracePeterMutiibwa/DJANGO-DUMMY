// declare instance for the off canvas
var offCanvasInstance;

var finalReceiver;

// wait for the page to load
document.addEventListener('DOMContentLoaded', ()=>{
    // get all the image selectors
    var allImageSelectors = document.querySelectorAll('.image-selectors');

    // get the image selector
    var imageSelectorButton = document.getElementById("image-sender");

    // capture any clicks on the selector
    allImageSelectors.forEach(imageSelector => {
        // get the clicks
        imageSelector.addEventListener("click", (toggleEvent)=>{

            // get the output field
            var outputFieldId = toggleEvent.target.getAttribute("data-output-receiver");

            // store the receiver
            finalReceiver = document.getElementById(outputFieldId)

            // set the controller
            document.getElementById("image-sender").setAttribute("data-image-receiver", outputFieldId);

            // prepare the off canvas
            var offCanvasElement = document.getElementById("offcanvasEnd");

            // js offcanvas instance
            offCanvasInstance = new bootstrap.Offcanvas(offCanvasElement);

            // display the off canvas
            offCanvasInstance.show();
        });

    });

    // get the selected image
    imageSelectorButton.addEventListener("click", (imageSenderEvent)=>{
        // get the currently selected image
        var currentlySelectedImageContainer = document.querySelector(".swiper-slide.swiper-slide-active").getAttribute("style");

        // get the receiver
        var imageReceiver = document.getElementById(imageSenderEvent.target.getAttribute("data-image-receiver"));

        // extract the image url
        var selectedImageUrl = currentlySelectedImageContainer.slice(currentlySelectedImageContainer.indexOf("(") + 1, currentlySelectedImageContainer.indexOf(")"));

        // close the offcanvas
        offCanvasInstance.hide();

        
        // set the image url
        finalReceiver.value = selectedImageUrl;

        // wipe the data attribute
        document.getElementById("image-sender").setAttribute("data-image-receiver", "");


    });

});