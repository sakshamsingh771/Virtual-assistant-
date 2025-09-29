import eel
import wikipedia
import pyttsx3
import datetime
import webbrowser
import random
import sys

# Initialize Eel
eel.init('web')

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# ------------------ Conversation Memory ------------------
conversation_history = []
last_user_input = ""

def speak(text):
    """Speak text and return it to frontend."""
    engine.say(text)
    engine.runAndWait()
    return text

# ------------------ Follow-up responses ------------------
greetings = ["Hello!", "Hi there!", "Hey! How are you?", "Hi! Nice to see you."]
follow_ups = ["How's your day going?", "What are you up to today?", "Anything exciting happening?"]
small_talk = ["That's interesting!", "I see!", "Tell me more.", "Oh, really?"]

# ------------------ Command processor ------------------
@eel.expose
def process_command(cmd: str):
    global conversation_history, last_user_input
    cmd_lower = cmd.lower().strip()
    last_user_input = cmd_lower
    response = ""

    # ---------------- Time ----------------
    if "time" in cmd_lower:
        now = datetime.datetime.now()
        response = "The time is " + now.strftime("%I:%M %p")

    # ---------------- Open website ----------------
    elif cmd_lower.startswith("open ") or cmd_lower.startswith("launch "):
        target = cmd.split(" ", 1)[1]
        if "." in target or target.startswith("http"):
            url = target if target.startswith("http") else "https://" + target
        else:
            mappings = {"youtube": "https://www.youtube.com",
                        "google": "https://www.google.com",
                        "gmail": "https://mail.google.com"}
            url = mappings.get(target, "https://www." + target + ".com")
        webbrowser.open(url)
        response = f"Opened {url}"

    # ---------------- Wikipedia search ----------------
    elif cmd_lower.startswith("wikipedia") or cmd_lower.startswith("search wikipedia for"):
        try:
            if "search wikipedia for" in cmd_lower:
                q = cmd_lower.split("search wikipedia for",1)[1].strip()
            else:
                q = cmd_lower.split("wikipedia",1)[1].strip()
            summary = wikipedia.summary(q, sentences=2)
            response = f"Wikipedia: {summary}"
        except:
            response = "Sorry, I couldn't find that on Wikipedia."

    # ---------------- Greetings / conversation ----------------
    elif any(greet in cmd_lower for greet in ["hello","hi","hey"]):
        response = random.choice(greetings)
        # Add a follow-up question
        response += " " + random.choice(follow_ups)

    elif "how are you" in cmd_lower:
        response = "I'm just a virtual assistant, but I'm functioning perfectly! How about you?"

    elif "your name" in cmd_lower:
        response = "I am lyra, your virtual assistant."

    elif "who are you" in cmd_lower or "what can you do" in cmd_lower:
        response = "I am lyra. I can fetch information, open websites, tell time, chat with you, and more!"

    # ---------------- Goodbye / exit ----------------
    elif "goodbye" in cmd_lower or "exit" in cmd_lower or "stop listening" in cmd_lower:
        response = "Goodbye! See you later."
        eel.show_response(response)
        sys.exit(0)

    # ---------------- Small talk ----------------
    elif any(word in cmd_lower for word in ["weather","day","life","fun","movie","food","game"]):
        response = random.choice(small_talk)
        response += " " + random.choice(follow_ups)

    # ---------------- Fallback: general question ----------------
    else:
        try:
            # Try Wikipedia first
            summary = wikipedia.summary(cmd, sentences=2)
            response = f"Wikipedia: {summary}"
        except:
            # Else fallback to Google search link
            response = f"I'm not sure, but you can check this link: https://www.google.com/search?q={cmd.replace(' ','+')}"
        # Add friendly follow-up
        response += " Do you want to ask something else?"

    # ---------------- Update conversation memory ----------------
    conversation_history.append({"user": cmd, "bot": response})

    # ---------------- Send response ----------------
    eel.show_response(response)

# ---------------- Launch Eel ----------------
eel.start('index.html', size=(700,600))