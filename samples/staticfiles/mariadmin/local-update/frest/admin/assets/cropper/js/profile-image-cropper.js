
// globals
var cropperInstance;

var croppedCanvas;

document.querySelector(".account-file-input").addEventListener("change", (event) => {

    // get the file length array
    if (event.target.files.length) {
        // create an uploader instance
        const readerInstance = new FileReader();

        // on getting the data url
        readerInstance.onload = (newEvent) => {
            // if there is a string url for the image
            if (newEvent.target.result) {
                // get the url
                let imageUrl = newEvent.target.result;

                // create an image element
                let imageElement = document.createElement("img");

                // set its attributes
                imageElement.id = 'uploaded-image';

                // load
                imageElement.setAttribute("src", imageUrl);

                // classes
                imageElement.classList.add("img-fluid");

                imageElement.classList.add("rounded");
                

                // clean result area
                let cropperImageHolder = document.getElementById("cropper-result-holder");

                cropperImageHolder.innerHTML = "";

                // display save button
                if (document.getElementById("preview-image-holder").classList.contains("d-none")){
                    // unhide it
                    document.getElementById("preview-image-holder").classList.remove("d-none");
                }

                // hide submit button
                if (!document.getElementById("profile-image-saver").classList.contains("d-none")){
                    // hide submit button
                    document.getElementById("profile-image-saver").classList.add("d-none");

                    // clear previous value
                    document.getElementById("avatar-form-element").value = "";
        
                }

                // add the create image
                cropperImageHolder.appendChild(imageElement);

                // create cropper instance
                cropperInstance = new Cropper(imageElement, {
                    aspectRatio: 1,
                    viewMode: 1

                });


            }

        };

        // resolve the path into an image url
        readerInstance.readAsDataURL(event.target.files[0]);

    } else {

    }

    // track the save button
    document.getElementById("preview-image-button").addEventListener("click", (event) => {
        // selected width
        let selectedWidth = 150;


        // get a new image source
        let newImageSource = cropperInstance.getCroppedCanvas(
            {
                width: selectedWidth,
                height: selectedWidth
            }

        ).toDataURL();

        // load
        document.getElementById("avatar-form-element").value = newImageSource;

        // load
        document.getElementById("uploadedNewAvatar").setAttribute("src", newImageSource);

        if (document.getElementById("profile-image-saver").classList.contains("d-none")){
            document.getElementById("profile-image-saver").classList.remove("d-none");

        }
    });

});