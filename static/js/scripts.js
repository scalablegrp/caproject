//Regular expressions to ensure forms can only be submitted using values based on regular expression
const lettersAndSpacesOnlyRegex = new RegExp("[a-zA-Z ]$");
const lettersNumbersAndSpacesOnlyRegex = new RegExp("[a-zA-Z1-9]$");
const lettersNumbersSpacesAndSomeSpecialCharactersOnlyRegex = new RegExp("[a-zA-Z1-9?.,''()!\r\n\"]$");  //Allow letters,numbers, ?'".,!() symbols and blank lines,
const numberOnlyRegularExpression = new RegExp("[0-9]{4}"); // Only allow a 4 length number sequence
const fullAndDecimelNumbersOnlyRegex = new RegExp("[0-9]")

//jQuery
$(document).ready(function() {
    // For each property card calculate remaining time for bidding
    $(".propertyCard").each(function() {
        let timerContainer = $(this.querySelector(".remaining_bid_time_seconds"));
        let timerOutput = $(this.querySelector(".remaining_bid_time"))
        let bidForm = $(this.querySelector(".bid_form"))
        //Allow user to select if they want to be updated for future bids on a property they have made a bid on
        $(this.querySelector(".bid_form")).on("submit", function() {
            trackBid = $("input[name= 'trackBid']");
            if(confirm("Would you like to receive notifications for bids made on this property?\nok=yes, cancel=no")) {
                trackBid.val(true);
            } else {
                trackBid.val(false);
            }
        })
        if($(this.querySelector(".remaining_bid_time")).html() != "Bid End") {
            let currentTracker = timerContainer.html();
            //Every second update the timer value
            setInterval(function() {  
                // Determine days, hours, minutes and seconds remaining
                let secondTracker = currentTracker--;   //Decrement end bid time seconds by 1 second on each iterval
                let days = Math.floor(secondTracker / 86400) || 0;
                // Subtract the days from secondTracker 
                secondTracker -= days * 86400;
                let hours = Math.floor(secondTracker / 3600) % 24 || 0;
                // Subtract the hours from secondTracker
                secondTracker -= hours * 3600;
                let mins = Math.floor(secondTracker / 60) || 0; 
                // Subtract mins from secondTracker
                secondTracker -= mins * 60 || 0;
                timerOutput.html(`${days} day(s), ${hours} hour(s), ${mins} min(s), ${secondTracker} second(s)`);
                //If the second tracker reaches 0 remove the bid form and remaining bid time details
                if(currentTracker < 0) {
                    bidForm.remove();
                    timerOutput.html('Bid End');
                }
            }, 1000)
        }
    })

    // Perform form validation using regular expression on the property form
    $("#propertyForm").on("submit", function(event) {
        //Check if user wants to receive bidding notifications
        trackBid = $("input[name= 'trackBid']");
        if(confirm("Would you like to receive notifications for bids made on this property?\nok=yes, cancel=no")) {
            trackBid.val(true);
        } else {
            trackBid.val(false);
        }
        let houseNumber = $("input[name = 'house_number']");
        let street = $("input[name = 'street']");
        let town = $("input[name = 'town']");
        let county = $("input[name = 'county']");
        let postCode = $("input[name = 'post_code']");
        let buildYear = $("input[name = 'build_year']");
        let price = $("input[name = 'price']");
        let footage = $("input[name = 'footage']");
        let bathRoomAmount = $("input[name = 'bathroom_amount']");
        let bedroomAmount = $("input[name = 'bedroom_amount']");
        let description = $('textarea')
        let bidEnd = $("input[name = 'bid_end']");
        // Get the current time to ensure bid end isn't being set as a past date
        let bidEndDate = new Date(bidEnd.val())
        let currentDateTime = new Date();
        // Regex checkers for form input values. If all form inputs match regular expression checks submit the form
        if(lettersNumbersSpacesAndSomeSpecialCharactersOnlyRegex.test(description.val()) && lettersNumbersAndSpacesOnlyRegex.test(houseNumber.val()) && 
            lettersNumbersAndSpacesOnlyRegex.test(street.val()) && lettersNumbersAndSpacesOnlyRegex.test(town.val()) && lettersAndSpacesOnlyRegex.test(county.val()) && 
            lettersNumbersAndSpacesOnlyRegex.test(postCode.val()) && (numberOnlyRegularExpression.test(buildYear.val()) && buildYear.val().length == 4 && 
            buildYear.val() <= newDate().getFullYear()) && numberOnlyRegularExpression.test(price.val()) && numberOnlyRegularExpression.test(footage.val()) && 
            numberOnlyRegularExpression.test(bathRoomAmount.val()) && numberOnlyRegularExpression.test(bedroomAmount.val() && currentDateTime < bidEndDate))  {
                return true;
            }
        else {
            // If the form values don't match the regular expression checks prevent the form from being submit
            event.preventDefault();
            letterNumbersAndSpacesOnly = "You have entered invalid characters. Letters, numbers and spaces will only be accepted"
            // Go through each scenario which may fail a regular expression check and provide a message to user. Remove user message if input is adjusted to valid value
            if (!lettersNumbersAndSpacesOnlyRegex.test(houseNumber.val())) {
                displayFormError(houseNumber, letterNumbersAndSpacesOnly);
            } else {
                removeFormError(houseNumber)
            }
            if (!lettersNumbersAndSpacesOnlyRegex.test(street.val())) {
                displayFormError(street, letterNumbersAndSpacesOnly);
            } else {
                removeFormError(street)
            }
            if (!lettersNumbersAndSpacesOnlyRegex.test(town.val())) {
                displayFormError(town, letterNumbersAndSpacesOnly);
            } else {
                removeFormError(town)
            }
            if (!lettersNumbersAndSpacesOnlyRegex.test(postCode.val())) {
                displayFormError(postCode, letterNumbersAndSpacesOnly);
            } else {
                removeFormError(postCode)
            }
            if (!lettersAndSpacesOnlyRegex.test(county.val())) {
                displayFormError(county, "You have entered invalid characters. Letters and spaces will only be accepted");
            } else {
                removeFormError(county)
            }
            if (!numberOnlyRegularExpression.test(buildYear.val() || buildYear.val().length != 4 || buildYear.val() > newDate().getFullYear())) {
                displayFormError(buildYear, "You have entered an invalid year");
            } else {
                removeFormError(buildYear)
            }
            if (!lettersNumbersSpacesAndSomeSpecialCharactersOnlyRegex.test(description.val())) {
                displayFormError(description, "You have entered invalid characters. Letters, numbers, spaces and  ?'\".,!() symbols will only be accepted");
            } else {
                removeFormError(buildYear)
            }
            if(bidEndDate < currentDateTime ) {
                displayFormError(bidEnd, "You must enter a future date");
            } else {
                removeFormError(bidEnd)
            }
        }
    })
});

//Display appropriate error message if property form fails regular expression checks
function displayFormError(element, errorMessage) {
	//Avoid error duplication to check if error message is already present
	if (element.parent().children().last()[0].localName != "p") {
		let formError = document.createElement("p");
		formError.style.color = "red";
		formError.innerHTML = errorMessage;
		element.parent().append(formError);
	}
}

//Remove error message if shown for a valid form value
function removeFormError(element) {
	if (element.parent().children().last()[0].localName == "p") {
		element.parent().children('p').remove();
	}
}

