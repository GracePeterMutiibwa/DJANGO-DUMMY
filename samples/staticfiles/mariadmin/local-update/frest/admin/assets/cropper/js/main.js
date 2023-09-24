// globals
var cropperInstance;

var croppedCanvas;

// get the file-input
document.querySelector("#my-uploader").addEventListener("change", (event) => {
    // get the file length array
    if (event.target.files.length) {
        // create an uploader instance
        const readerInstance = new FileReader();

        // track its change attribute
        readerInstance.onload = (newEvent) => {
            // if their is a string url for the image
            if (newEvent.target.result) {

                // create an image element
                let imageElement = document.createElement("img");

                // set its attributes
                imageElement.id = 'uploaded';

                imageElement.src = newEvent.target.result;

                // clean result area
                let imageHolder = document.querySelector(".result")

                imageHolder.innerHTML = "";

                // add the create image
                imageHolder.appendChild(imageElement);

                // show the options
                document.querySelector(".options").classList.remove("d-none");


                // create cropper instance
                cropperInstance = new Cropper(imageElement, {
                    aspectRatio: 1,
                    viewMode: 1

                });




            }
        };

        // resolve the path into an image url
        readerInstance.readAsDataURL(event.target.files[0]);


        // track the save button
        document.querySelector("#my-save-button").addEventListener("click", (event) => {
            // selected width
            let selectedWidthElement = document.querySelector("#width");


            // get a new image source
            let newImageSource = cropperInstance.getCroppedCanvas(
                {
                    width: selectedWidthElement.value,
                    height: selectedWidthElement.value
                }

            ).toDataURL();

            // display
            let croppedImageElement = document.querySelector(".cropped");

            // set its path
            croppedImageElement.src = newImageSource;

            // set the download link
            let downloadElement = document.querySelector("#my-downloader");

            // set the download name
            downloadElement.download = 'sample.png'

            // set the link
            downloadElement.setAttribute("href", newImageSource);


        });


    }
});