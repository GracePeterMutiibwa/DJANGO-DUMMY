
document.addEventListener('DOMContentLoaded', ()=>{
    
    // get the page
    var allMenuTogglers = document.querySelectorAll('.menu-toggler');

    allMenuTogglers.forEach(menuToggler =>{
        // track clicks
        menuToggler.addEventListener('click', (clickEvent)=>{
            // get the target
            var viewerInstance = new bootstrap.Offcanvas(document.getElementById(menuToggler.getAttribute("data-attached-target")))

            viewerInstance.show();
        });
    });
});