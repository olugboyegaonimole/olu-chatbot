const chatbox = document.getElementById("chatbox");
const userInput = document.getElementById("userInput");

function sendMessage() {
    let message = userInput.value.trim();
    if (message === "") return;

    // Display user message
    displayMessage("You", message);
    userInput.value = "";

    // Send message to chatbot API
    fetch("https://olu-chatbot.onrender.com/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        displayMessage("Bot", data.response);
    })
    .catch(error => {
        displayMessage("Bot", "Error: Unable to connect to chatbot.");
    });
}

function displayMessage(sender, message) {
    let msgDiv = document.createElement("div");
    msgDiv.classList.add("message");
    msgDiv.innerHTML = `<strong>${sender}:</strong> ${message}`;
    chatbox.appendChild(msgDiv);
    chatbox.scrollTop = chatbox.scrollHeight;
}

// Send message when user presses Enter
userInput.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});
