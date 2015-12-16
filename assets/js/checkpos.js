var button = document.getElementById('checkinbtn');

var resultmessage = document.getElementById('msg');

var result;

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
		result = data.split(":")[1].split("}")[0];
		if(result === ' 1'){
			resultmessage.style.color="green";
			resultmessage.innerHTML = "You are now checked in!";
		}
    else if(result === ' 2') {
    	resultmessage.style.color="red";
    	resultmessage.innerHTML = "You must be in the lecture to check in.";
    }
    else if(result === ' 3') {
    	resultmessage.style.color="red";
    	resultmessage.innerHTML = "You do not currently have a lecture to check in to";
    }
  });
}
function error(err){
  resultmessage.innerHTML = 'Error(' + err.code + '):' + err.message;
}

button.onclick = function () {
	getLocation();
}

