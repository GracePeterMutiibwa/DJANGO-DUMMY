document.addEventListener("DOMContentLoaded", ()=>{
    // get the search button and the toggle
    var searchButton = document.getElementById("services-search-trigger");

    var searchEnabler = document.getElementById("search-enabler");

    var searchArea = document.getElementById("service-search-area");

    // track toggle
    searchEnabler.addEventListener("change", ()=>{
        // check if its active
        if (searchEnabler.checked){
            searchButton.disabled = false;

            searchArea.disabled = false;

        } else {
            searchButton.disabled = true;

            searchArea.disabled = true;

        }
    });



});
