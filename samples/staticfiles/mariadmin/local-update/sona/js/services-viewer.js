
/**
 * 
 * @param {string} selectedServiceName - The name of the selected service
 */
function getAndDisplayServiceDetails(selectedServiceName){
    // get the brief
    let serviceBriefDescription = document.querySelector(`p[data-brief-for="${selectedServiceName}"]`).innerHTML;

    // get detailed description
    let detailedDescription = document.querySelector(`input[name="${selectedServiceName}"]`).value;

    // get the service image
    let servicePreview = document.querySelector(`img[data-image-for="${selectedServiceName}"]`).getAttribute("src");

    // console.log("brief:", serviceBriefDescription);
    // console.log("detailed:", detailedDescription);
    // console.log("preview:", servicePreview);

    // load the details
    document.getElementById("service-image-holder").setAttribute("src", servicePreview);

    document.getElementById("offcanvas-brief-display").innerHTML = serviceBriefDescription;

    document.getElementById("service-name-offcanvas").innerHTML = selectedServiceName;

    document.getElementById("service-detailed-offcanvas").innerHTML = detailedDescription;

    // get the off canvas
    var displayCanvas = new bootstrap.Offcanvas(document.getElementById("service-offcanvas"));

    // show the canvas
    displayCanvas.show();

}

document.addEventListener('DOMContentLoaded', ()=>{
    // get the togglers
    var allTogglers = document.querySelectorAll(".more-details-toggler");

    allTogglers.forEach(eachToggler =>{
        
        // track clicks
        eachToggler.addEventListener('click', (clickEvent)=>{
            
            // stop movement
            clickEvent.preventDefault();

            // get the name of the service
            let serviceName = eachToggler.getAttribute("data-service-name");

            // fetch other details and display them
            getAndDisplayServiceDetails(serviceName);

        });
    });

});