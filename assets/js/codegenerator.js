button = document.getElementById('generate');

button.onclick = function () {
	code = document.getElementById('code');
	code.innerText = generate(6);
	document.getElementById('submit').disabled = false;
}

function generate(codelength){
	var code = " ";

	var charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";

	for(var i=0; i<codelength; i++)
		code += charset.charAt(Math.floor(Math.random() * charset.length));

	return code;
}



