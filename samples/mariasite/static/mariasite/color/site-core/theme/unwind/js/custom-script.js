// Get all the nav links
const navLinks = document.querySelectorAll('.navbar-nav .nav-link');

// Add event listener to each link
navLinks.forEach(link => {
  link.addEventListener('click', function(event) {
    // Store the ID of the clicked link in local storage
    const linkId = this.getAttribute('data-id');
    localStorage.setItem('activeLinkId', linkId);
  });
});

// Apply the "active" class to the corresponding element when new context is loaded
document.addEventListener('DOMContentLoaded', function() {
    const activeLinkId = localStorage.getItem('activeLinkId');
  
    // If there is an active link ID stored
    if (activeLinkId) {
      // Remove active class from all links
      navLinks.forEach(link => {
        link.classList.remove('active');
      });
  
      // Add the "active" class to the corresponding element
      const elementToActivate = document.querySelector(`[data-id="${activeLinkId}"]`);
      if (elementToActivate) {
        elementToActivate.classList.add('active');
      }
    } else {

    }


  });





