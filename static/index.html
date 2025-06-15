// Log that the script has been loaded
console.log("script.js is loaded");

// Wait until the DOM is fully loaded before running our code
document.addEventListener("DOMContentLoaded", () => {
  console.log("DOM fully loaded");

  // Retrieve key DOM elements and check if they exist
  const userForm = document.getElementById("userForm");
  const userInput = document.getElementById("userInput");
  const responseText = document.getElementById("responseText");

  // If any of the elements are missing, log an error and end execution
  if (!userForm || !userInput || !responseText) {
    console.error("Required DOM elements not found.");
    return;
  }

  // Add an event listener for form submission to handle user input
  userForm.addEventListener("submit", (event) => {
    // Prevent the default browser form submission action
    event.preventDefault();

    // Retrieve the value the user entered into the input box
    const inputValue = userInput.value;
    console.log("Form submitted; user input:", inputValue);

    // Send a POST request to the root URL with the user input data.
    // The data is URL encoded to ensure proper transmission.
    fetch("/", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: `user_input=${encodeURIComponent(inputValue)}`
    })
    .then((response) => response.json()) // Parse the JSON response from the server
    .then((data) => {
      // Update the page with the server's response message
      responseText.innerText = data.message;
      console.log("Server responded:", data);
    })
    .catch((error) => {
      // Log any error that occurred during the fetch process
      console.error("Error:", error);
    });
  });
});


