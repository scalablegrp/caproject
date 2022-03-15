//Regular expressions to ensure forms can only be submitted using values based on regular expression
const lettersNumbersAndSpacesOnlyRegex = new RegExp("[a-zA-Z1-9]$");
const numberOnlyRegularExpression = new RegExp("[0-9]"); //Ensure only numbers can be used
const fullAndDecimelNumbersOnlyRegex = new RegExp("[0-9]")

//jQuery
$(document).ready(function() {
    // For each property card calculate remaining time for bidding
    $(".propertyCard").each(function() {
        let timerContainer = $(this.querySelector(".remaining_bid_time_seconds"));
        let timerOutput = $(this.querySelector(".remaining_bid_time"))
        let bidForm = $(this.querySelector(".bid_form"))
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
    });

    // Perform form validation using regular expression on the property form
    $("#propertyForm").on("submit", function(event) {
        //Check if user wants to receive bidding notifications
        trackBid = $("input[name= 'trackBid']");
        if(confirm("Would you like to receive notifications for bids made on this property?\nok=yes, cancel=no")) {
            trackBid.val(true);
        } else {
            trackBid.val(false);
        }
        console.log(`Bid track = ${trackBid.val()}`)
        let houseNumber = $("input[name = 'house_number']");
        let street = $("input[name = 'street']");
        let town = $("input[name = 'town']");
        let postCode = $("input[name = 'post_code']");
        let buildYear = $("input[name = 'build_year']");
        let price = $("input[name = 'price']");
        let footage = $("input[name = 'footage']");
        let bathRoomAmount = $("input[name = 'bathroom_amount']");
        let bedroomAmount = $("input[name = 'bedroom_amount']");
        let description = $('textarea')
        console.log(description.val());
        // Regex checkers for form input values
        if(lettersNumbersAndSpacesOnlyRegex.test(houseNumber.val()) && lettersNumbersAndSpacesOnlyRegex.test(street.val()) && lettersNumbersAndSpacesOnlyRegex.test(town.val()) 
            && lettersNumbersAndSpacesOnlyRegex.test(postCode.val()) && (numberOnlyRegularExpression.test(buildYear.val()) && buildYear.val().length == 4) 
            && numberOnlyRegularExpression.test(price.val()) && numberOnlyRegularExpression.test(footage.val()) && numberOnlyRegularExpression.test(bathRoomAmount.val()) 
            && numberOnlyRegularExpression.test(bedroomAmount.val()))  {
                console.log("Everything matches Regex")
            }
    })
});

