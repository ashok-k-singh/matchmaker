
// get data from the API route that returns an array of match objects
d3.json("/matchdata", function(matchData) {


    // grab a reference to the DOM element where we'll be displayig the matches
    var results = document.getElementById("matchResults");

    // if there are matches, display them, else display a message
    if (matchData.length > 0) {

        // display a heading
        results.innerHTML += '<h1>Your matches:</h1></br>';

        // create a card columns div
        results.innerHTML += '<div id="matchDeck" class="card-columns">';

        // grab a reference to the newly created card columns 
        var deck = document.getElementById("matchDeck");

            // loop through the array of match objects and create a card for each
            matchData.forEach((match) => {
                    deck.innerHTML += 
                    `
                    <div class="card" style="width:300px">
                        <img class="card-img-top" src="${match['photo']}" alt="${match['screenname']}">
                        <div class="card-body">
                            <h5 class="card-title">${match['screenname']}</h5>
                            <div class="card-text">Age: ${match['age']}</div>
                            <div class="card-text">Email: ${match['email']}</div>
                        </div>
                    </div>
                    `
                    });      
    } else {
        results.innerHTML += '<h4>Sorry! No matches yet. Check back later!</h4><br>'
    };

    });



