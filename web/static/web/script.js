function showPassword() {
  var x = document.getElementById("password");
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
} 
function showR_Password() {
  var x = document.getElementById("r_password");
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
} 

function toggleForm(){
  let register = document.getElementById("registro");
  let login = document.getElementById("login");
  register.classList.toggle("unseen");
  login.classList.toggle("unseen");
}