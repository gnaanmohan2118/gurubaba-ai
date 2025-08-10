const form = document.getElementById("chat-form");
const messageInput = document.getElementById("message");
const chatContainer = document.getElementById("chat-container");

// Get or create session_id
let sessionId = localStorage.getItem("session_id");
if (!sessionId) {
  sessionId = crypto.randomUUID();
  localStorage.setItem("session_id", sessionId);
}

window.addEventListener("DOMContentLoaded", () => {
  appendMessage("bot", "Speak, wisdom shall follow.");
  messageInput.focus();
});

// Load previous chat history on page load
window.addEventListener("DOMContentLoaded", async () => {
  try {
    const res = await fetch(`/session/${sessionId}`);
    if (res.ok) {
      const data = await res.json(); 
      data.history.forEach(msg => appendMessage(msg.role, msg.content));
    }
  } catch (err) {
    console.error("Failed to load history:", err);
  }

  messageInput.focus();
});

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
      body: JSON.stringify({
        message: userText,
        session_id: sessionId
      })
    });

    const data = await response.json();
    loadingBot.textContent = (data.reply || "🙏 Guru is silent...");
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
  return msg;
}

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
