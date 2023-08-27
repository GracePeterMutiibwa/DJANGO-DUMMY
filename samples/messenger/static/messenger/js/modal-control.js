// declare the cropper
var cropperInstance;

// get the input element
document.querySelector("#userimage").addEventListener("change", (event) => {
  if (event.target.files.length) {
    // get selected file
    let selectedFile = event.target.files[0];

    //   create a reader object
    let readerInstance = new FileReader();

    //   track changes
    readerInstance.onload = (fileInstance) => {
      // create image instance
      var imageElement = document.getElementById("image-viewer");

      // status
      var isPresent = false;

      // check if the cropper instance exists yet
      if (cropperInstance) {
        // destroy the cropper
        cropperInstance.destroy();

        // first remove the current source
        imageElement.src = "";

        // update the status
        isPresent = true;
      }

      // wait fo the image creation
      imageElement.onload = () => {
        //
        // console.log(`Status:${isPresent}`);

        // check the status
        if (!isPresent) {
          // make the image visible
          document.querySelector("#image-resizer").classList.remove("d-none");
        } else {
          // clean
          document.querySelector(".cropped-image-viewer").innerHTML = "";

          // create p tag
          var pTag = document.createElement("p");

          // add the classes
          pTag.classList.add("card-text");
          pTag.classList.add("text-muted");
          pTag.textContent = "No Cropped Image yet";

          document.querySelector(".cropped-image-viewer").appendChild(pTag);
        }

        //   initialize the cropper
        cropperInstance = new Cropper(imageElement, {
          aspectRatio: 9 / 9,
          viewMode: 1,
        });

        // add an event listener
        document
          .querySelector("#crop-image")
          .addEventListener("click", (event) => {
            // get the cropped image
            var croppedImageUrl = cropperInstance
              .getCroppedCanvas({
                width: 300,
                height: 300,
              })
              .toDataURL();

            // get the viewer
            var croppedImageElement = document.createElement("img");

            croppedImageElement.src = croppedImageUrl;

            croppedImageElement.id = "cropped-profile-image";

            // add bounding classes
            croppedImageElement.classList.add("img-fluid");

            // display the image
            document.querySelector(".cropped-image-viewer").innerHTML = "";

            document
              .querySelector(".cropped-image-viewer")
              .appendChild(croppedImageElement);
          });
      };

      // update the image
      imageElement.src = fileInstance.target.result;
    };

    // read the selected file
    readerInstance.readAsDataURL(selectedFile);
  }
});
