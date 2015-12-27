var button = document.getElementById('checkinbtn');

var resultmessage = document.getElementById('msg');

var score = document.getElementById('score');
var count = document.getElementById('count');
var streak = document.getElementById('streak');

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

