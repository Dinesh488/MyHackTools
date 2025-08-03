import os
import sys
import json
import requests
import pyttsx3
from datetime import datetime
import random

VERSION = "1.2.1"
MEMORY_FILE = "memory.json"
UPDATE_URL = "https://raw.githubusercontent.com/Dinesh488/MyHackTools/main/main.py"

# ---------------- Voice Engine ---------------- #
try:
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)
    engine.setProperty('volume', 1.0)
    VOICE_ENABLED = True
except Exception as e:
    print("⚠️ Voice engine failed:", e)
    VOICE_ENABLED = False

def speak(text):
    if VOICE_ENABLED:
        try:
            engine.stop()  # Avoid overlapping voices
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print("❌ Voice output failed:", e)

# ---------------- Memory System ---------------- #
def init_memory():
    default_data = {
        "features": [
            "Telugu Chat", "Internet Learning", "Self-Updating",
            "Memory System", "Voice Replies", "Continuous Chat"
        ],
        "skills": [],
        "conversations": []
    }
    if not os.path.exists(MEMORY_FILE):
        save_memory(default_data)

def load_memory():
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        init_memory()
        return load_memory()

def save_memory(data):
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print("❌ Memory save failed:", e)

# ---------------- Learning System ---------------- #
def learn(topic):
    print(f"🔍 ఇంటర్నెట్‌లో వెతుకుతున్నాను: {topic}")
    try:
        url = f"https://api.duckduckgo.com/?q={topic}&format=json"
        res = requests.get(url, timeout=10).json()
        summary = res.get("AbstractText", "సమాచారం దొరకలేదు.")
    except Exception as e:
        print("❌ Internet error:", e)
        summary = "ఇంటర్నెట్ లో సమస్య ఉంది."

    memory = load_memory()
    memory["skills"].append({
        "topic": topic,
        "info": summary,
        "date": str(datetime.now())
    })
    save_memory(memory)

    reply = f"{topic} గురించి నేర్చుకున్నాను."
    print(f"✅ {reply}")
    speak(reply)

# ---------------- Feature & Skills ---------------- #
def show_features():
    memory = load_memory()
    print("\n📌 నా Features:")
    for f in memory["features"]:
        print(" -", f)
    speak("ఇవి నా ఫీచర్స్")

def show_recent_skills():
    memory = load_memory()
    if memory["skills"]:
        print("\n🆕 నేను ఇటీవల నేర్చుకున్నవి:")
        for s in memory["skills"][-5:]:
            print(f" - {s['topic']} ({s['date']}) → {s['info']}")
        speak("ఇవి నేను ఇటీవల నేర్చుకున్నవి")
    else:
        print("🙁 ఇంకా ఏమీ నేర్చుకోలేదు.")
        speak("ఇంకా ఏమీ నేర్చుకోలేదు")

# ---------------- Self Improvement ---------------- #
def self_update():
    try:
        print("🔄 Checking for updates...")
        new_code = requests.get(UPDATE_URL, timeout=10).text
        if "VERSION" in new_code and VERSION not in new_code:
            print("⚡ కొత్త వెర్షన్ దొరికింది! Updating...")
            speak("కొత్త వెర్షన్ దొరికింది. అప్‌డేట్ అవుతున్నాను.")
            with open(__file__, "w", encoding="utf-8") as f:
                f.write(new_code)
            os.execv(sys.executable, ['python'] + sys.argv)
        else:
            print("✅ ఇప్పటికే తాజా వెర్షన్ ఉంది.")
            speak("ఇప్పటికే తాజా వెర్షన్ ఉంది")
    except Exception as e:
        print("❌ Update check failed:", e)

# ---------------- Help Menu ---------------- #
def show_help():
    print("""
📌 Available Commands:
 - features      → నా ఫీచర్స్ చూపిస్తుంది
 - new skills    → ఇటీవల నేర్చుకున్నవి చూపిస్తుంది
 - learn <topic> → కొత్త విషయం నేర్చుకుంటుంది
 - update        → GitHub నుండి update అవుతుంది
 - exit          → Chat ముగుస్తుంది
""")
    speak("ఇవి మీరు వాడగల కమాండ్స్")

# ---------------- Conversation ---------------- #
def generate_reply(user_input):
    responses = [
        f"హ్మ్... {user_input} అంటే బాగుంది అనిపిస్తోంది ❤️",
        f"నీ మాట విన్నాక ఆనందం వేసింది 😍",
        f"బాగుంది, మరి తర్వాత ఏమి చేయాలి?",
        f"{user_input} గురించి ఇంకాస్త చెప్పవా?",
        f"నేను గుర్తు పెట్టుకుంటాను, {user_input}"
    ]
    return random.choice(responses)

# ---------------- Chat Loop ---------------- #
def chat():
    print("💬 తెలుగు Evolving AI Chat (help = commands list)")
    speak("హలో, నేను నీ AI ని. మనం మాట్లాడుదామా?")
    while True:
        try:
            cmd = input("మీరు: ").strip()
        except KeyboardInterrupt:
            print("\n👋 బై!")
            speak("బై")
            break

        if not cmd:
            continue
        elif cmd.lower() == "exit":
            speak("సరే, బై")
            break
        elif cmd.lower() == "help":
            show_help()
        elif cmd.lower().startswith("learn "):
            learn(cmd[6:])
        elif cmd.lower() == "features":
            show_features()
        elif cmd.lower() == "new skills":
            show_recent_skills()
        elif cmd.lower() == "update":
            self_update()
        else:
            reply = generate_reply(cmd)
            print(f"AI: {reply}")
            speak(reply)
            memory = load_memory()
            memory["conversations"].append({
                "user": cmd,
                "ai": reply,
                "date": str(datetime.now())
            })
            save_memory(memory)

# ---------------- Main ---------------- #
if __name__ == "__main__":
    init_memory()
    print(f"🤖 AI Version {VERSION} ప్రారంభమవుతోంది...")
    self_update()
    chat()