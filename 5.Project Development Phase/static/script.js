const form = document.querySelector("form");

form.addEventListener("submit", function(e){

const inputs = document.querySelectorAll("input");

for(let input of inputs){

if(input.value===""){

alert("Please fill all fields.");

e.preventDefault();

return;

}

}

});