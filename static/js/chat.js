document.addEventListener("DOMContentLoaded", () => {
  const chatBox = document.getElementById("chat-box");
  const userInputEl = document.getElementById("user-input");
  const sendButton = document.getElementById("send-button");
  const loadingIndicator = document.getElementById("loading-indicator");

  sendButton.addEventListener("click", async (event) => {
    event.preventDefault();
    await sendMessage();
  });

  async function sendMessage() {
    const message = userInputEl.value.trim();
    if (!message) return;

    userInputEl.value = "";
    appendMessage(chatBox, message, "user-message");
    showLoading();

    try {
      const response = await fetch("/send_message", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `message=${encodeURIComponent(message)}`
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      hideLoading();
      const showData = data.problem_text || data.explanation_text

      appendMessage(chatBox, showData, "ai-message");

      chatBox.scrollTop = chatBox.scrollHeight;
    } catch (error) {
      console.error("Error:", error);
      hideLoading();
      const errorMessage = "エラーが発生しました。ページをリロードして、もう一度お試しください。";
      appendMessage(chatBox, errorMessage, "error-message");
      chatBox.scrollTop = chatBox.scrollHeight;
    }
  }

  function appendMessage(container, message, cssClass) {
    const messageEl = document.createElement("div");
    messageEl.className = cssClass;

    const html = marked.parse(message || "");
    const safeHtml = DOMPurify.sanitize(html);

    messageEl.innerHTML = safeHtml;
    container.appendChild(messageEl);
    container.scrollTop = container.scrollHeight;
  }

  function showLoading() {
    loadingIndicator.style.display = "flex";
  }

  function hideLoading() {
    loadingIndicator.style.display = "none";
  }
});
