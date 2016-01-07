var backBtn = document.getElementById('back');
var forwardBtn = document.getElementById('forward');

backBtn.onclick = function () {
	$.ajax({
  		url:"/history",
  		type:"POST",
  		data: JSON.stringify({ direction : "back" })
	});
}

forwardBtn.onclick = function () {
	$.ajax({
  		url:"/history",
  		type:"POST",
  		data: JSON.stringify({ direction : "forward" })
	});
}