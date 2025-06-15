// Ensure the DOM is fully loaded before running our code
document.addEventListener("DOMContentLoaded", () => {
  // ===== Handle Login =====
  // Retrieve key DOM elements for login functionality
  const loginForm = document.getElementById("loginForm");
  const loginEmail = document.getElementById("loginEmail");
  const loginPassword = document.getElementById("loginPassword");
  const loginResponse = document.getElementById("loginResponse");

  // If all required login elements are present, set up the submit event listener
  if (loginForm && loginEmail && loginPassword && loginResponse) {
    loginForm.addEventListener("submit", async function (event) {
      event.preventDefault(); // Prevent the default form submission

      // Get input values from the email and password fields
      const email = loginEmail.value;
      const password = loginPassword.value;

      try {
        // Send an asynchronous POST request to the login endpoint with JSON data
        const response = await fetch("/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, password })
        });

        // Wait for and parse the JSON response from the server
        const result = await response.json();

        // Display the server's response message in the loginResponse element.
        // It shows 'result.message' if available, otherwise 'result.error'
        loginResponse.innerText = result.message || result.error;
        console.log("Login response:", result);

        // If the response includes a username (indicating a successful login), redirect to the homepage
        if (result.username) {
          window.location.href = "/";
        }
      } catch (error) {
        // Log any errors that occur during the fetch request
        console.error("Login error:", error);
      }
    });
  } else {
    console.error("One or more login elements were not found in the DOM.");
  }

  // ===== Handle Logout =====
  // Retrieve the logout button from the DOM
  const logoutButton = document.getElementById("logoutButton");

  // If the logout button exists, set up a click event listener
  if (logoutButton) {
    logoutButton.addEventListener("click", async function () {
      try {
        // Send an asynchronous GET request to the logout endpoint
        const response = await fetch("/logout");
        // Parse the JSON response from the server
        const result = await response.json();
        console.log("Logout response:", result);
        // Redirect to the homepage after processing the logout
        window.location.href = "/";
      } catch (error) {
        // Log any errors that occur during the logout process
        console.error("Logout error:", error);
      }
    });
  } else {
    console.error("Logout button not found in the DOM.");
  }
});
