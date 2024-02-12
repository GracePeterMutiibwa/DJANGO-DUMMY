const bookingButton = document.getElementById('booking-register-trigger');

const bookingButtonText = document.getElementById('booking-button-text');

const bookingButtonIcon = document.getElementById('booking-button-icon');

const confirmationModal = document.getElementById('confirmationModal');

const proceedButton = document.getElementById('proceed-button');

// track clicks
document.addEventListener('DOMContentLoaded', () => {
    // get the booking button
    bookingButton.addEventListener('click', (clickEvent) =>{
        if (bookingButton.classList.contains('collapsed')){
            bookingButtonText.innerHTML = 'Add Booking';

            bookingButton.classList.remove('btn-secondary');

            bookingButton.classList.add('btn-primary');

            bookingButtonIcon.classList.remove('fa-close');

            bookingButtonIcon.classList.add('fa-add');
            

        } else {
            
            bookingButtonText.innerHTML = 'Cancel';

            bookingButton.classList.remove('btn-primary');

            bookingButton.classList.add('btn-secondary');

            bookingButtonIcon.classList.remove('fa-add');

            bookingButtonIcon.classList.add('fa-close');

        }

    });

    document.querySelectorAll('.delete-request-tag').forEach(eachElement => {
        eachElement.addEventListener('click', clickEvent => {
            clickEvent.preventDefault();

            // get the link
            let proceedLink = eachElement.getAttribute('proceed-link');

            // display the modal
            let modalInstance = new bootstrap.Modal(confirmationModal);

            // update the button
            proceedButton.setAttribute('href', `${proceedLink}`);

            modalInstance.show();
        });
    });
});