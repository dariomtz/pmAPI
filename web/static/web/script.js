function toggleForm() {
  let register = document.getElementById("registro");
  let login = document.getElementById("login");
  register.classList.toggle("unseen");
  login.classList.toggle("unseen");
}

function getLoginData() {
  let username = $("#l_username").val();
  let password = $("#l_password").val();
  let test = {
    username: username,
    password: password
  };
  console.log(test);
  console.log(JSON.stringify(test));
  return test;
}

function getSigUpData() {
  let username = $("#username").val();
  let name = $("#name").val();
  let lastname = $("#last_name").val();
  let email = $("#email").val();
  let password = $("#password").val();
  let sigUp = {
    username: username,
    first_name: name,
    last_name: lastname,
    email: email,
    password: password
  };
  console.log(sigUp);
  return sigUp;
}

function passwordMatch() {
  return $("#password").val() === $("#r_password").val() ? true : false;
}

function sendSigUp() {
  if (passwordMatch()) {
    alert("coinciden");
  } else {
    alert("no coinciden");
  }
}
