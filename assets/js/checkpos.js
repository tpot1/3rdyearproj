var button = document.getElementById('checkinbtn');

var resultmessage = document.getElementById('msg');

var score = document.getElementById('score');
var streak = document.getElementById('streak');
var count = document.getElementById('count');

var badges = document.getElementById('badges');

var modalTable = document.getElementById('modalTable');


function getLocation() {
    if(geo_position_js.init()){
      geo_position_js.getCurrentPosition(showPosition,error);
    }
    else {
    	resultmessage.style.color="red";
      resultmessage.innerHTML = "Geolocation is not supported by this browser.";
    }
}
function showPosition(position) {
    $.ajax({
  		url:"/",
  		type:"POST",
  		data: JSON.stringify({ lat : position.coords.latitude, lon : position.coords.longitude })
	}).done(function( data ) {
    data = $.parseJSON(data);
		if(data['valid'] === 1){
			resultmessage.style.color="green";
			resultmessage.innerHTML = "You are now checked in!";
      score.innerHTML = "Score: " + data['score'];
      count.innerHTML = "Number of Check-Ins: " + data['count'];
      streak.innerHTML = "Current Streak: " + data['streak'];

      for(i = 0; i < data['titles'].length; i++){
        //removes the message telling the user how to earn badges
        var nobadge = document.getElementById("nobadge");
        if(nobadge){
          nobadge.remove();
        }        

        var newBadge = document.createElement("img");
        newBadge.setAttribute("src", data['icons'][i]);
        newBadge.setAttribute("height", "42");
        newBadge.setAttribute("width", "42");
        newBadge.setAttribute("alt", "");
        badges.appendChild(newBadge);
        
        var modalBadge = document.createElement("img");
        modalBadge.setAttribute("src", data['icons'][i]);
        modalBadge.setAttribute("height", "42");
        modalBadge.setAttribute("width", "42");
        modalBadge.setAttribute("alt", "");
        var title = document.createTextNode(data['titles'][i]);
        var description = document.createTextNode(data['descriptions'][i]);
        var points = document.createTextNode(data['points'][i]);

        var row = modalTable.insertRow(-1);
        var cell1 = row.insertCell(0);
        var cell2 = row.insertCell(1);
        var cell3 = row.insertCell(2);
        var cell4 = row.insertCell(3);

        cell1.appendChild(modalBadge);
        cell2.appendChild(title);
        cell3.appendChild(description);
        cell4.appendChild(points);

        //shows the modal, with the completed challenges added
        $('#myModal').modal('show');
        //resets the modal table once it is closed, removing the previously completed challenges
        $(".modal").on("hidden.bs.modal", function(){
          $(".table").html("<thead><tr><th>Badge</th><th>Challenge</th><th>Description</th><th>Points</th></tr></thead><tbody></tbody>");
        });
      }
		}
    else if(data['valid'] === 2) {
    	resultmessage.style.color="red";
    	resultmessage.innerHTML = "You must be in the lecture to check in!";
    }
    else if(data['valid'] === 3) {
    	resultmessage.style.color="red";
    	resultmessage.innerHTML = "You do not currently have a lecture to check in to!";
    }
    else if(data['valid'] === 4) {
      resultmessage.style.color="red";
      resultmessage.innerHTML = "You have already checked in to that lecture!";
    }
  });
}
function error(err){
  resultmessage.innerHTML = 'Error(' + err.code + '):' + err.message;
}

button.onclick = function () {
	getLocation();
}

