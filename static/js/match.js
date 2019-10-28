// data is from data.js for now, need to call Ashok's route from here
var matches = data;

function displayMatches(matchData) {

    var el = document.getElementById("matchResults");

    if (matchData.length > 0) {

        el.innerHTML += '<h1>Your matches:</h1></br>'

        el.innerHTML += '<div class="card-deck"'
            matchData.forEach((match) => {
                    el.innerHTML += 
                    `
                    <div class="card" style="width:350px">
                        <img class="card-img-top" src="${match['photo']}" alt="${match['screenname']}">
                        <div class="card-body">
                            <h5 class="card-title">${match['screenname']}</h5>
                            <div class="card-text">Age: ${match['age']}</div>
                            <div class="card-text">Email: ${match['email']}</div>
                        </div>
                    </div>
                    </br>
                    `
                    });
        el.innerHTML += '</div></br>'        
    } else {
        el.innerHTML += '<h4>Sorry! No matches yet. Check back later!</h4><br>'
    }
};

displayMatches(matches);
