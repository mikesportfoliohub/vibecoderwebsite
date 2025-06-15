// Ensure the DOM is fully loaded before running our code
document.addEventListener("DOMContentLoaded", () => {
  // ===== Handle Registration =====
  // Retrieve necessary DOM elements for registration functionality
  const registerForm = document.getElementById("registerForm");
  const usernameInput = document.getElementById("username");
  const emailInput = document.getElementById("email");
  const passwordInput = document.getElementById("password");
  const registerResponseElem = document.getElementById("registerResponse");

  // Check if all the registration elements exist to avoid runtime errors
  if (registerForm && usernameInput && emailInput && passwordInput && registerResponseElem) {
    // Attach a submit event listener to handle user registration
    registerForm.addEventListener("submit", async (event) => {
      event.preventDefault(); // Prevent the default browser form submission

      // Retrieve and (optionally) trim input values from the form fields
      const username = usernameInput.value.trim();
      const email = emailInput.value.trim();
      const password = passwordInput.value;

      try {
        // Send an asynchronous POST request to the /register_user endpoint
        const response = await fetch("/register_user", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, email, password })
        });

        // Parse the JSON response from the server
        const result = await response.json();

        // Update the registration response element with either a success or error message
        registerResponseElem.innerText = result.message || result.error;
        console.log("Registration response:", result);
      } catch (error) {
        // Log any errors that occur during the process
        console.error("Registration error:", error);
      }
    });
  } else {
    console.error("One or more registration elements were not found in the DOM.");
  }

  // ===== Show Registered Users =====
  // Retrieve the show users button and the element that will list users
  const showUsersButton = document.getElementById("showUsers");
  const usersList = document.getElementById("usersList");

  // Ensure both the button and the list element exist
  if (showUsersButton && usersList) {
    // Attach a click event listener to the 'Show Registered Users' button
    showUsersButton.addEventListener("click", async () => {
      console.log("Show Registered Users button clicked");
      try {
        // Send a GET request to the /get_users endpoint to fetch user data
        const response = await fetch("/get_users");
        console.log("Fetch response received", response);

        // Parse the response JSON to get the list of users
        const users = await response.json();
        console.log("Fetched users:", users);

        // Clear any existing content in the users list
        usersList.innerHTML = "";

        // If no users are returned, display a message
        if (users.length === 0) {
          console.log("No users returned from the endpoint.");
          const li = document.createElement("li");
          li.textContent = "No registered users found.";
          usersList.appendChild(li);
        } else {
          // For each user, create a list item with their username and email, then add it to the list
          users.forEach(user => {
            console.log("Displaying user:", user);
            const li = document.createElement("li");
            li.textContent = `${user.username} (${user.email})`;
            usersList.appendChild(li);
          });
        }
      } catch (error) {
        // Log any errors that occur during the user fetch process
        console.error("Error fetching users:", error);
      }
    });
  } else {
    console.error("Show Users button or users list element not found in the DOM.");
  }
});
