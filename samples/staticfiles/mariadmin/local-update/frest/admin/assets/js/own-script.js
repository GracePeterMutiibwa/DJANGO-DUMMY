// get the submit event
const uploadButtonElement = document.getElementById("upload-button");

const resetButtonElement = document.getElementById("reset-button");

const fileUploadField = document.getElementById("file-field");

const filesFormElement = document.getElementById("files-form");

const imageParentContainer = document.getElementById("image-container");

function previewResetter(){
    // clear the parent container
    imageParentContainer.innerHTML = "";

    // create a temporary holder
    var temporaryDivElement = document.createElement('div');

    // load the contents
    temporaryDivElement.innerHTML = `
        <div class="d-flex justify-content-center align-items-center">
            <p class="fs-4">Preview Of Selected Image File</p>
        </div>
    `;

    // load the data
    imageParentContainer.appendChild(temporaryDivElement);

    return;


}

function previewLoader(imageFile){
    // create file reader component
    var newFileReader = new FileReader();

    // track loading
    newFileReader.onload = (event)=>{
        // if the file is loaded get the image data url equivalent
        var dataUrlEquivalent = event.target.result;

        // create an image element
        var imageElement = document.createElement('img');

        // add the bootstrap class so that the image fits its container
        imageElement.classList.add('img-fluid');

        // add the image data
        imageElement.src = dataUrlEquivalent;

        // clear the parent container
        imageParentContainer.innerHTML = "";

        // add the image to the container
        imageParentContainer.appendChild(imageElement)

        return;
    };


    // convert file to data url
    newFileReader.readAsDataURL(imageFile);

}

function activationHandler(statusOfElements){
    if (statusOfElements === 0){
        // de-activate
        resetButtonElement.disabled = true;

        uploadButtonElement.disabled = true;

    } else {
        // activate
        resetButtonElement.disabled = false;

        uploadButtonElement.disabled = false;
    }

    return;

}

document.addEventListener('DOMContentLoaded', ()=>{
    // track changes at the file selector
    fileUploadField.addEventListener('change', (event)=>{
        // get the file present
        if (event.target.files.length > 0){
            var selectedFile = event.target.files[0];

            // file extension
            var fileExtension = selectedFile.name.split('.').pop();

            var allowedExtensions = ['png', 'jpeg', 'jpg'];

            if (allowedExtensions.includes(fileExtension)){
                // activate
                activationHandler(1);

                // show a preview of the file
                previewLoader(selectedFile);



            } else {
                // deactivate
                activationHandler(0);

            }

        }
        
    });

    // reset
    resetButtonElement.addEventListener("click", ()=>{
        // reset the form
        filesFormElement.reset();

        // deactivate
        activationHandler(0);

        // clear the preview
        previewResetter();
    });


    // get all buttons
    document.querySelectorAll('.view-button').forEach(eachButton =>{
        eachButton.addEventListener('click', (clickEvent)=>{
            // get the id
            var imageId = clickEvent.target.getAttribute('data-meta-id');

            // Find the corresponding image element src
            var imageSrc = document.getElementById(imageId).getAttribute("src");

            // get the modal image element
            document.getElementById("modal-image-show").setAttribute("src", imageSrc);

            // get the modal
            var previewModal = document.getElementById("displayImage");

            // create a bootstrap modal
            var bootstrapModalInstance = new bootstrap.Modal(previewModal);

            // display the modal
            bootstrapModalInstance.show();


        });
    });



});
