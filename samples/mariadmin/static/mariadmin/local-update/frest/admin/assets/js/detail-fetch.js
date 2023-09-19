
/**
 * 
 * @param {string} categoryName - The name of the category
 */
function getCategoryInnerHtmlMint(categoryName){
    let categorySwitchHtml = `
                        <label class="switch switch-primary">
                        <span class="switch-label">${categoryName}</span>
                        <input type="checkbox" class="switch-input" checked disabled>
                        <span class="switch-toggle-slider">
                            <span class="switch-on">
                            <i class="bx bx-check"></i>
                            </span>
                            <span class="switch-off">
                            <i class="bx bx-x"></i>
                            </span>
                        </span>
                        </label>
                        `;

    return categorySwitchHtml

}

/**
 * 
 * @param {object} barePostData - Contains post data
 */

function displayPostDataOnViewer(barePostData){
    // load the heading image and title
    document.getElementById("post-heading-image").setAttribute("src", barePostData.heading_image);

    document.getElementById("post-title-heading").innerHTML = barePostData.heading;

    // load top body
    document.getElementById("top-body-text").innerHTML = barePostData.top_body;

    // load main image
    document.getElementById("post-body-main-image").setAttribute("src", barePostData.main_image);

    // load the left and right images
    if (barePostData.left_image){
        // 
        let leftImage = document.createElement('img');
        
        leftImage.setAttribute("src", barePostData.left_image);

        leftImage.classList.add('img-fluid');

        document.getElementById("left-image-holder").innerHTML = leftImage.outerHTML;

    }

    if (barePostData.right_image){
        // 
        let rightImage = document.createElement('img');
        
        rightImage.setAttribute("src", barePostData.right_image);

        rightImage.classList.add('img-fluid');

        document.getElementById("right-image-holder").innerHTML = rightImage.outerHTML;

    }

    // load lower post body
    document.getElementById("lower-body-text").innerHTML = barePostData.lower_body;

    // console.log("Date:", barePostData.date);
    
    // load the date
    document.getElementById("post-date-show").innerHTML = barePostData.date;


    // get the parent element
    var parentCategoryElement = document.getElementById("post-category-show");

    // clean the element
    parentCategoryElement.innerText = "";

    // load the categories
    if (Array.isArray(barePostData.categories)){
        // collect the categories
        let categoriesToLoad = [];

        barePostData.categories.forEach(eachCategory => {
            // get the inner html
            let categorySwitchHtml = getCategoryInnerHtmlMint(eachCategory);

            // create a div for each one
            let simpleDiv = document.createElement('div');
            
            // add spacing
            simpleDiv.classList.add("mx-1")

            // load the category
            simpleDiv.innerHTML = categorySwitchHtml;

            // store the category
            categoriesToLoad.push(simpleDiv);
            
        });

        // after add them to the div
        categoriesToLoad.forEach(eachFormattedCategory =>{
            parentCategoryElement.appendChild(eachFormattedCategory);
        });



    } else {
        // just load the category
        let categorySwitchHtml = getCategoryInnerHtmlMint(barePostData.categories)
        
        // create a div element
        let holderDiv = document.createElement("div");

        // load its inner html
        holderDiv.innerHTML = categorySwitchHtml;

        parentCategoryElement.appendChild(holderDiv);
    }

    // ensure the first slide is the active one
    let sliderContainer = document.getElementById("sliders-container");

    // get all the sliders
    let selectedSlider = sliderContainer.querySelector(".carousel-item.active");


    selectedSlider.classList.remove('active');

    // get the very first child
    let firstSliderElement = sliderContainer.querySelector(".carousel-item:first-child");

    firstSliderElement.classList.add('active');


}

function clearPostEditor(){
    // load the heading image and title
    document.getElementById("post-heading").value = "";

    document.getElementById("post-header-image").value = "";

    // load top body
    document.getElementById("post-top-body").value = "";

    // load main image
    document.getElementById("main-post-image").value = "";

    // update the left image
    document.getElementById("left-sub-image").value = "";

    // update the left image
    document.getElementById("left-sub-image").value = "";

    // load lower post body
    document.getElementById("post-lower-body").value = "";

    // goto the first section
    document.getElementById("first-section").click();

    
    return;

}

/**
 * 
 * @param {object} barePostData - Contains post data
 */
function displayPostDataInEditor(barePostData){
    // load the heading image and title
    document.getElementById("post-heading").value = barePostData.heading;

    document.getElementById("post-header-image").value = barePostData.heading_image;


    // load top body
    document.getElementById("post-top-body").value = barePostData.top_body;


    // load main image
    document.getElementById("main-post-image").value = barePostData.main_image;

    // load the left and right images
    if (barePostData.left_image){
        // update the left image
        document.getElementById("left-sub-image").value = barePostData.left_image;

    }

    if (barePostData.right_image){
        // update the left image
        document.getElementById("left-sub-image").value = barePostData.right_image;

    }

    // load lower post body
    document.getElementById("post-lower-body").value = barePostData.lower_body;


    return;

}

/**
 * 
 * @param {number} idOfPost - Id of the post data item
 * @param {string} validityToken - Token for validation
 * @param {number} displayArea - Where to display the results fetched
 */

function fetchAndDisplayPostDetails(idOfPost, validityToken, displayArea){
    // get the details
    var formToSubmit = new FormData();

    // add the id
    formToSubmit.append('post-id', idOfPost);

    // create a request
    var xmlHttpRequest = new XMLHttpRequest();

    // open the request
    xmlHttpRequest.open("POST", "/get-post-data/");

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

            // display the data in display area
            if (displayArea === 1){ 
                displayPostDataOnViewer(returnedJsonData.info);

            } else {
                displayPostDataInEditor(returnedJsonData.info);
            }


            


        } else {
            console.log('Failed');
        }
    };

    // send the request
    xmlHttpRequest.send(formToSubmit);

}

/**
 * 
 * @param {string} postId - The id of a form that holds a csrf token
 * @returns 
 */

/**
 * @param {string} postId - Gets the validation token for that given id
 */
function getValidationTokenForId(postId){
    let attachedForm = document.querySelector(`form[data-post-form="${postId}"]`);

    let attachedToken = attachedForm.querySelector('input[name="csrfmiddlewaretoken"]').value;

    return attachedToken;

}

/**
 * 
 * @param {number} toMode - The mode to switch to 0 - default, 1 - edit
 * @returns 
 */
function toggleSubmitModes(toMode){
    // get the button
    var postSubmitButton = document.getElementById("post-form-submitter");

    // get left pane
    var leftPane = document.getElementById("change-color-holder");

    // get cancel button
    var editCancelButton = document.getElementById("edit-cancel-button");

    // get post button text container
    var postButtonTextHolder = document.getElementById("post-button-text");

    if (toMode === 0){
        postSubmitButton.classList.remove("btn-info");

        leftPane.classList.remove("bg-light");

        editCancelButton.classList.add('d-none');

        var colorCode = "btn-success";

        var buttonText = 'Save'

    } else {
        postSubmitButton.classList.remove("btn-success");

        leftPane.classList.add("bg-light");

        editCancelButton.classList.remove('d-none');

        var colorCode = "btn-info";
        
        var buttonText = 'Save Changes'
    }

    // add the new color code
    postSubmitButton.classList.add(colorCode);

    postButtonTextHolder.innerHTML = buttonText;

    return;
}

/**
 * 
 * @param {string} idToUse - The id of the element edited
 * @returns 
 */
function createAndLoadEditInput(idToUse){
    // add the edit button
    var temporaryInput = document.createElement("input");

    temporaryInput.setAttribute("type", "hidden");

    temporaryInput.setAttribute("name", "edited-post");

    temporaryInput.setAttribute("value", idToUse);

    document.getElementById("operation-category").innerHTML = "";

    document.getElementById("operation-category").appendChild(temporaryInput);

    return;
}

// goto viewer
function scrollToViewer(){
    // get the entry section
    var postViewer = document.getElementById("posts-entry-section");

    postViewer.scrollIntoView(
        {
            behavior: "smooth"
        }
    ); 
}

// scrolling to editor
function scrollToEditor(){
    var targetElement = document.getElementById("post-editor-section");

    targetElement.scrollIntoView(
        {
            behavior: "smooth"
        }
    );

    return;
}

// wait for the dom to load
document.addEventListener('DOMContentLoaded', ()=>{
    // get the element
    var postModalElement = document.getElementById("postDataModal");

    // get all click buttons
    var postEditTriggers = document.querySelectorAll(".post-editors");

    // cancel button
    var editModeToggler = document.getElementById("edit-cancel-button");

    // handle edit mode cancel
    editModeToggler.addEventListener('click', ()=>{
        // clean the edit field container
        document.getElementById("operation-category").innerHTML = "";

        // clear editor
        clearPostEditor();

        // change the interface mode
        toggleSubmitModes(0);


        // goto viewer
        scrollToViewer();


    });

    // track the show event on the modal after click
    postModalElement.addEventListener("show.bs.modal", (triggerEvent)=>{
        // get button that triggered the modal to be shown
        var clickedButtonInstance = triggerEvent.relatedTarget;

        // get the associated data
        var postGetId = clickedButtonInstance.getAttribute("data-get-tag");

        // get validation token
        let validationToken = getValidationTokenForId(postGetId);


        // console.log("Token:", validationToken, " PostId:", postGetId);

        // get and display the details
        fetchAndDisplayPostDetails(postGetId, validationToken, 1);

    });

    // listen for clicks
    postEditTriggers.forEach(eachTriggerElement =>{
        // listen for clicks
        eachTriggerElement.addEventListener('click', (clickEvent)=>{
            // prevent the fetching of a url
            clickEvent.preventDefault();

            // get the associated id
            let idOfPostToEdit = eachTriggerElement.getAttribute("data-post-edit");

            let validationToken = getValidationTokenForId(idOfPostToEdit);

            // load the details
            fetchAndDisplayPostDetails(idOfPostToEdit, validationToken, 2);

            // update the edit area
            createAndLoadEditInput(idOfPostToEdit);

            // then change the interface look
            toggleSubmitModes(1);

            // scroll to editor
            scrollToEditor();

        });

    });
    
});