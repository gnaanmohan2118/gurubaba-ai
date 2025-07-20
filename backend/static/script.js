const form = document.getElementById("chat-form");
const messageInput = document.getElementById("message");
const chatContainer = document.getElementById("chat-container");

// Submit on Enter, newline with Shift+Enter
messageInput.addEventListener("keydown", function (e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    form.dispatchEvent(new Event("submit"));
  }
});

// Handle form submit
form.addEventListener("submit", async function (e) {
  e.preventDefault();
  const userText = messageInput.value.trim();
  if (!userText) return;

  appendMessage("user", userText);
  messageInput.value = "";

  const loadingBot = appendMessage("bot", "🧘 Baba is thinking...");

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message: userText })
    });

    const data = await response.json();

    loadingBot.textContent = "🧘 Gurubaba says: " + (data.reply || "🙏 Baba is silent...");
  } catch (error) {
    loadingBot.textContent = "⚠️ Gurubaba error: " + error.message;
  }
});

// Append messages and return the element created
function appendMessage(sender, text) {
  const msg = document.createElement("div");
  msg.classList.add("message", sender);
  msg.textContent = text;
  chatContainer.appendChild(msg);
  msg.scrollIntoView({ behavior: "smooth" });
  return msg; // So we can modify this if needed
}

// On first load
window.addEventListener("DOMContentLoaded", () => {
  appendMessage("bot", "🧘 Welcome to Gurubaba's wisdom chat! Ask your questions and receive guidance.");
  messageInput.focus();
});

// Click to focus
chatContainer.addEventListener("click", () => messageInput.focus());

// Placeholder UX
messageInput.addEventListener("click", () => {
  if (messageInput.placeholder) messageInput.placeholder = "";
});

messageInput.addEventListener("keyup", () => {
  if (!messageInput.value.trim()) messageInput.placeholder = "Ask Gurubaba...";
});

window.addEventListener("resize", () => {
  chatContainer.scrollTop = chatContainer.scrollHeight;
});
