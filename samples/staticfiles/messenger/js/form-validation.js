(function () {
  "use strict";

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  var forms = document.querySelectorAll(".needs-validation");

  // Loop over them and prevent submission
  Array.prototype.slice.call(forms).forEach(function (form) {
    form.addEventListener(
      "submit",
      function (event) {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();

        
          // create an alert
          var alertContent = [
            `<div class="alert alert-info" id="error-alert" role="alert">`,
            ` Please <strong> fill </strong> in all required fields.`,
            ` <button class="btn-close" data-bs-dismiss="alert"></button>`,
            `</div>`
          ].join("");

          // clear current alert
          document.querySelector(".alert-holder").innerHTML = "";

          // add the alert
          document.querySelector(".alert-holder").innerHTML = alertContent;

        } else {
          // stop its submission
          event.preventDefault();

          // prepare image
          var imageData;

          var imageName;

          // check if the files where loaded
          if (
            document.querySelector("#userimage").files.length > 0 &&
            document.querySelector("#cropped-profile-image")
          ) {
            // get the file
            var selectedFile = document.querySelector("#userimage").files[0];

            // get the file extension
            var fileExtension = selectedFile.name.split(".").pop();

            // get the image data
            var rawImage = document.querySelector("#cropped-profile-image");

            // Get the dimensions and position of the image
            const rect = rawImage.getBoundingClientRect();

            // Create a canvas element with the same dimensions as the image
            const canvas = document.createElement("canvas");
            canvas.width = rect.width;
            canvas.height = rect.height;

            // Draw the image onto the canvas
            const ctx = canvas.getContext("2d");
            ctx.drawImage(rawImage, 0, 0, rect.width, rect.height);

            // Get a base64-encoded data URL for the canvas
            imageData = canvas.toDataURL(`image/${fileExtension}`);

            imageName = selectedFile.name;
          } else {
            imageData = "";

            imageName = "";
          }

          // debug
          // console.log(imageData);
          // console.log(imageName);

          // get form
          var formElement = document.querySelector("#signup-form");

          // create a form object
          var formObject = new FormData(formElement);

          // add the image data and the name
          formObject.append("image-data", imageData);

          formObject.append("image-name", imageName);

          // get the token
          var csrfToken = document.querySelector(
            "input[name='csrfmiddlewaretoken']"
          ).value;

          // debug
          // Get the value of a specific form field
          // const username = formObject.get("image-data");
          // console.log("Username:", username);

          // send the form
          const xhr = new XMLHttpRequest();

          // establish connection
          // urls have to end with forward slash
          xhr.open("POST", "/signup/");

          // set a header for the token
          xhr.setRequestHeader("X-CSRFToken", csrfToken);

          // call backs
          xhr.onload = () => {
            if (xhr.status === 200) {
              // get the json data
              const response = JSON.parse(xhr.responseText);

              // console.log(response["message"]);

              // reset the form elements
              formElement.reset();
            }
          };

          xhr.onerror = () => {
            var statusText = xhr.statusText;

            console.log(`Error: ${statusText}`);
          };

          // send the data
          xhr.send(formObject);
        }

        form.classList.add("was-validated");
      },
      false
    );
  });
})();

const passwordInput = document.getElementById("password");

const toggleButton = document.getElementById("toggle-password");

const eyeView = document.getElementById("pass-toggle");

toggleButton.addEventListener("click", () => {
  if (passwordInput.type === "password") {
    passwordInput.type = "text";
    // remove the closed eye
    eyeView.classList.remove("fa-regular");
    eyeView.classList.remove("fa-eye-slash");

    // add the open eye
    eyeView.classList.add("fa-solid");
    eyeView.classList.add("fa-eye");
  } else {
    passwordInput.type = "password";

    // remove the open eye
    eyeView.classList.remove("fa-solid");
    eyeView.classList.remove("fa-eye");

    // add the closed eye
    eyeView.classList.add("fa-regular");
    eyeView.classList.add("fa-eye-slash");
  }
});
