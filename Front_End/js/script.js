const baseUrl = "http://localhost:8000/api";

document.addEventListener("DOMContentLoaded", function () {
  // Get the menu link and the dropdown
  var menuLink = document.querySelector(".menu");
  var dropdown = document.getElementById("menu-dropdown");

  let loginLink = document.getElementById("login-button");
  if (localStorage.getItem("Authorization")) {
    loginLink.innerHTML = `
  <i class="fas fa-sign-out"></i> Log out
  `;
    loginLink.addEventListener("click", () => {});
  }

  // Add event listener to the menu link
  menuLink.addEventListener("click", function (event) {
    // Prevent the default action (scrolling)
    event.preventDefault();

    // Toggle the dropdown visibility
    dropdown.style.display =
      dropdown.style.display === "none" ? "block" : "none";
  });
  window.addEventListener("click", function (event) {
    // Check if the click was outside the menu
    if (!event.target.closest(".menu")) {
      // Close the dropdown if it's open
      dropdown.style.display = "none";
    }
  });
});

document.getElementById("item2").addEventListener("click", function (event) {
  event.preventDefault(); // Prevents the default action (navigating to the URL)
  alert("You should log in first"); // Shows the alert message
});

document.getElementById("item3").addEventListener("click", function (event) {
  event.preventDefault(); // Prevents the default action (navigating to the URL)
  alert("You should log in first"); // Shows the alert message
});

// automatic slider

var counter = 1;
setInterval(function () {
  document.getElementById("radio" + counter).checked = true;
  counter++;
  if (counter > 3) {
    counter = 1;
  }
}, 3000);
