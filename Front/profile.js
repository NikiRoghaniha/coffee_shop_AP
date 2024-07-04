if (!localStorage.getItem("Authorization")) {
  window.location.href = "/index.html";
}
let loginLink = document.getElementById("logout-button");
l;
loginLink.addEventListener("click", (e) => {
  localStorage.removeItem("Authorization");
});

const myHeaders = new Headers();
myHeaders.append("Authorization", localStorage.getItem("Authorization"));
const requestOptions = {
  method: "GET",
  headers: myHeaders,
  redirect: "follow",
};
fetch("http://127.0.0.1:8000/api/profile/", requestOptions)
  .then((response) => {
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    return response.json();
  })
  .then((data) => {
    console.log(data);
  })
  .catch((error) => {
    console.error("There has been a problem with your fetch operation:", error);
    alert("Invalid credentials. Please try again.");
  });
