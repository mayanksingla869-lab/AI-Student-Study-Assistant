
const chatBox = document.getElementById("chatBox");
const input = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");
const newChat = document.getElementById("newChat");

let history = [];

function addMessage(text, role) {
    const message = document.createElement("div");
    message.className = "message " + role;
    message.textContent = text;
    chatBox.appendChild(message);
    chatBox.scrollTop = chatBox.scrollHeight;
    return message;
}

function showWelcome() {
    chatBox.innerHTML = `
        <div class="welcome">
            <div class="robot">🤖</div>
            <h1>How can I help you today?</h1>
            <p>Ask me anything about AI, ML, DSA and Programming.</p>
            <div class="suggestions">
                <button class="suggestion">What is Artificial Intelligence?</button>
                <button class="suggestion">Explain Machine Learning</button>
                <button class="suggestion">Explain Binary Search</button>
            </div>
        </div>`;
}

async function sendMessage(text) {
    const question = text.trim();

    if (!question || sendBtn.disabled) return;

    chatBox.querySelector(".welcome")?.remove();

    addMessage(question, "user");

    const previousHistory = history.slice();
    history.push({ role: "user", content: question });

    input.value = "";
    sendBtn.disabled = true;

    const loading = addMessage("Thinking...", "bot");

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                message: question,
                history: previousHistory
            })
        });

        const data = await response.json();
        loading.remove();

        if (!response.ok) {
            addMessage(data.error || "Something went wrong.", "bot");
            history = previousHistory;
        } else {
            addMessage(data.answer, "bot");
            history.push({ role: "assistant", content: data.answer });
        }

    } catch (error) {
        loading.remove();
        addMessage("Unable to connect to the server. Please try again.", "bot");
        history = previousHistory;
    }

    sendBtn.disabled = false;
    input.focus();
}

sendBtn.addEventListener("click", () => sendMessage(input.value));

input.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendMessage(input.value);
    }
});

chatBox.addEventListener("click", (event) => {
    if (event.target.classList.contains("suggestion")) {
        sendMessage(event.target.textContent);
    }
});

newChat.addEventListener("click", () => {
    history = [];
    showWelcome();
    input.value = "";
    input.focus();
});
