//alert("This alert shows that the js file is linked to base.html")
//jQuery
$( document ).ready(function() {
    // For each property card calculate remaining time for bidding
    $(".propertyCard").each(function() {
        let timerContainer = $(this.querySelector(".remaining_bid_time_seconds"));
        let timerOutput = $(this.querySelector(".remaining_bid_time"))
        // Display the remaining bid time after 1 second so user does not see millisecond timing value
        // setTimeout(function () {
        //     timerContainer.css('visibility', 'visible');
        //   }, 1000)
        // Only adjust bid value if bid is still ongoing
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
             }, 1000)
        }
    })
});

