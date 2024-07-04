document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("signin-form");

  if (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault(); // Prevent the form from submitting traditionally

      // Create a FormData object to hold the form data
      const formData = new FormData(this);

      // Extract individual form values
      const usernameEmail = formData.get("username-email");
      const password = formData.get("password");

      // Prepare the data for the AJAX request
      const requestData = {
        username: usernameEmail,
        password: password,
      };

      // Send the data to the server using AJAX
      const myHeaders = new Headers();
      myHeaders.append("Content-Type", "application/json");

      const requestOptions = {
        method: "POST",
        headers: myHeaders,
        body: JSON.stringify(requestData),
        redirect: "follow",
      };
      console.log(requestData);
      fetch("http://127.0.0.1:8000/api/token/obtain/", requestOptions)
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then((data) => {
          const accessToken = data.access;
          console.log("Success:", accessToken);
          localStorage.setItem("Authorization", "Bearer " + accessToken); // Store the token in localStorage
          alert("Login successful!");
          window.location.href = "/profile.html"; // Redirect to profile or dashboard page
        })
        .catch((error) => {
          console.error(
            "There has been a problem with your fetch operation:",
            error
          );
          alert("Invalid credentials. Please try again.");
        });
    });
  } else {
    console.error("Sign-in form element not found");
  }
});
