const chat = document.getElementById("chat");
const micBtn = document.getElementById("micBtn");
let wakeEnabled = true;
const WAKE_WORDS = ['lyra', 'hey lyra', 'ok lyra'];

// Add message to chat
function addMessage(text, sender) {
    const msg = document.createElement("div");
    msg.className = "message " + sender;
    msg.innerText = text;
    chat.appendChild(msg);
    chat.scrollTop = chat.scrollHeight;
}


// Send command to Python backend
function sendCommand(text=null) {
    let cmd = text || document.getElementById("commandInput").value;
    if (!cmd) return;
    addMessage(cmd, "user");
    eel.process_command(cmd);
    document.getElementById("commandInput").value = "";
}


// Receive response from Python
eel.expose(show_response);
function show_response(text) {
    addMessage(text, "bot");
    const u = new SpeechSynthesisUtterance(text);
    u.rate = 1.0;
    speechSynthesis.speak(u);
}


// Mic / Speech recognition
function startListening() {
    if (!('webkitSpeechRecognition' in window)) {
        alert("Speech Recognition not supported in this browser. Use Chrome!");
        return;
    }
    const recognition = new webkitSpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onstart = () => { 
        micBtn.classList.add("listening"); 
        micBtn.innerText = "🎙️ Listening...";
    };
    
    recognition.onend = () => { 
        micBtn.classList.remove("listening"); 
        micBtn.innerText = "🎤"; 
    };

    recognition.onresult = (event) => {
        let transcript = event.results[0][0].transcript.toLowerCase().trim();
        
        if (wakeEnabled) {
            const containsWake = WAKE_WORDS.some(w => transcript.includes(w));
            if (!containsWake) {
                addMessage("(Ignored — wake word not found)", "bot");
                return;
            }
            WAKE_WORDS.forEach(w => {
                if (transcript.startsWith(w)) transcript = transcript.slice(w.length).trim();
            });
        }

        if(transcript) {
            addMessage(transcript, "user");
            sendCommand(transcript);
        }
    };

    recognition.start();
}


// Button & input events
micBtn.addEventListener("click", startListening);
document.getElementById("commandInput").addEventListener("keydown", (e) => {
    if(e.key === "Enter") sendCommand();
});


// Wake-word toggle
function toggleWakeWord() {
    wakeEnabled = !wakeEnabled;
    document.getElementById("wakeText").innerText = wakeEnabled ? "On" : "Off";
}


// Dark/light theme toggle
document.getElementById("themeToggle").addEventListener("click", () => {
    if(document.body.classList.contains("light")){
        document.body.classList.replace("light","dark");
        document.getElementById("themeToggle").innerText = "☀️ Light Mode";
    } else {
        document.body.classList.replace("dark","light");
        document.getElementById("themeToggle").innerText = "🌙 Dark Mode";
    }
});