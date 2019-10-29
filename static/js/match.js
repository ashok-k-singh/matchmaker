d3.json("/testroute", function(matchData) {

    var results = document.getElementById("matchResults");

    if (matchData.length > 0) {

        results.innerHTML += '<h1>Your matches:</h1></br>';

        results.innerHTML += '<div id="matchDeck" class="card-columns">';

        var deck = document.getElementById("matchDeck");

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



