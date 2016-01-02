var add = document.getElementById('addbtn');

var remove1 = document.getElementById('removebtn1');
var remove2 = document.getElementById('removebtn2');
var remove3 = document.getElementById('removebtn3');
var remove4 = document.getElementById('removebtn4');

var moduleList = document.getElementById('moduleList');

var selected = [false, false, false, false];		//determines whether each of the 4 options have been selected

var module1 = document.getElementById('mod1');
var module2 = document.getElementById('mod2');
var module3 = document.getElementById('mod3');
var module4 = document.getElementById('mod4');

var modules = [module1, module2, module3, module4];

for(i = 0; i < 4; i++){
	selected[i] = modules[i].innerHTML !== '*Module ' + (i+1).toString() + '*';
}

add.onclick = function () {
	for (var i = 0; i < selected.length; i++) {
		if(!selected[i]){
			modules[i].innerHTML = moduleList.options[moduleList.selectedIndex].value;
			moduleList.remove(moduleList.selectedIndex);
			selected[i] = true;
			return;
		}
	};
}

remove1.onclick = function () {
	if(selected[0]){
		var option = document.createElement('option');
		option.text = option.value = module1.innerHTML;
		moduleList.add(option,moduleList.length);
		module1.innerHTML = '*Module 1*';
		selected[0] = false;
	}
}
remove2.onclick = function () {
	if(selected[1]){
		var option = document.createElement('option');
		option.text = option.value = module2.innerHTML;
		moduleList.add(option,moduleList.length);
		module2.innerHTML = "*Module 2*";
		selected[1] = false;
	}
}
remove3.onclick = function () {
	if(selected[2]){
		var option = document.createElement('option');
		option.text = option.value = module3.innerHTML;
		moduleList.add(option,moduleList.length);
		module3.innerHTML = "*Module 3*";
		selected[2] = false;
	}
}
remove4.onclick = function () {
	if(selected[3]){
		var option = document.createElement('option');
		option.text = option.value = module4.innerHTML;
		moduleList.add(option,moduleList.length);
		module4.innerHTML = "*Module 4*";
		selected[3] = false;
	}	
}


