document.addEventListener("DOMContentLoaded", () => {
  const chatBox = document.getElementById("chat-box");
  const userInputEl = document.getElementById("user-input");
  const sendButton = document.getElementById("send-button");

  sendButton.addEventListener("click", async (event) => {
    event.preventDefault();
    await sendMessage();
  });

  async function sendMessage() {
    const message = userInputEl.value.trim();
    if (!message) return;

    userInputEl.value = "";

    appendMessage(chatBox, message, "user-message");

    try {
      const response = await fetch("/send_message", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `message=${encodeURIComponent(message)}`,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      appendMessage(chatBox, data.response, "ai-message");
      chatBox.scrollTop = chatBox.scrollHeight;
    } catch (error) {
      console.error("Error:", error);
    }
  }

  function appendMessage(container, message, cssClass) {
    const messageEl = document.createElement("div");
    messageEl.className = cssClass;
    messageEl.textContent = message;
    container.appendChild(messageEl);
  }
});
