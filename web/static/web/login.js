function toggleVisible() {
	var inputs = ["email", "r-password", "noAcount", "acount"];

	for (let i = 0; i < inputs.length; i++) {
		let parent = document.getElementById(inputs[i]).parentNode;

		parent.classList.toggle("inactive");
	}
}
