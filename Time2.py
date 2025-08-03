import os
import sys
import json
import requests
import pyttsx3
from datetime import datetime
import random
import shutil

VERSION = "1.2.1"
MEMORY_FILE = "memory.json"
UPDATE_URL = "https://raw.githubusercontent.com/Dinesh488/MyHackTools/main/main.py"

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
            engine.stop()
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print("❌ Voice output failed:", e)

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

# 1. Search topic (learns and saves to memory)
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

    reply = f"{topic} గురించి నేర్చున్నాను."
    print(f"✅ {reply}")
    speak(reply)

# 2. Save & 3. Get from memory (by topic)
def get_from_memory(topic):
    memory = load_memory()
    found = [s for s in memory["skills"] if s['topic'].lower() == topic.lower()]
    if found:
        info = found[0]
        print(f"🔎 {topic}: {info['info']}")
        speak(info['info'])
    else:
        print("😕 That topic not found in memory.")
        speak("ఆ విషయం గుర్తు లేదు.")

# 4. Delete from memory
def delete_from_memory(topic):
    memory = load_memory()
    before = len(memory['skills'])
    memory['skills'] = [s for s in memory['skills'] if s['topic'].lower() != topic.lower()]
    after = len(memory['skills'])
    save_memory(memory)
    if before == after:
        print(f"⚠️ '{topic}' not found in skills.")
        speak(f"{topic} కనపడలేదు.")
    else:
        print(f"✅ '{topic}' deleted from skills.")
        speak(f"{topic} నీ జ్ఞాపకం నుండి తీసేశాను.")

# 5. List all topics
def list_all_topics():
    memory = load_memory()
    if memory["skills"]:
        print("\n🔥 Learned Topics:")
        for s in memory["skills"]:
            print(" -", s["topic"])
        speak("ఇవి నేర్చుకున్న అన్ని విషయాలు.")
    else:
        print("😕 No topics learned yet.")
        speak("ఇంకా ఏమీ నేర్చుకోలేదు.")

# 6 & 7: Backup main file to USB or any path
def backup_main(usb_path="/media/usb"):
    try:
        if not os.path.isdir(usb_path):
            print("❌ USB path not found.")
            speak("యుఎస్బి కనపడలేదు.")
            return
        shutil.copy(__file__, os.path.join(usb_path, os.path.basename(__file__)))
        print("✅ Backup done to USB!")
        speak("యుఎస్బి కి బాకప్ అయింది.")
    except Exception as e:
        print("❌ Backup failed:", e)
        speak("బాక్అప్ ఫెయిల్ అయింది.")

# 8. Download update / upgrade
def self_update():
    try:
        print("🔄 Checking for updates...")
        new_code = requests.get(UPDATE_URL, timeout=10).text
        if "VERSION" in new_code and VERSION not in new_code:
            print("⚡ కొత్త వెర్షన్ దొరికింది! Updating...")
            speak("కొత్త వెర్షన్ దొరికింది. అప్‌డేట్ అవుతున్నాను.")
            with open(__file__, "w", encoding="utf-8") as f:
                f.write(new_code)
            os.execv(sys.executable, [sys.executable] + sys.argv)
        else:
            print("✅ ఇప్పటికే తాజా వెర్షన్ ఉంది.")
            speak("ఇప్పటికే తాజా వెర్షన్ ఉంది.")
    except Exception as e:
        print("❌ Update check failed:", e)

# 9. Restart the script
def restart():
    print("🔄 Restarting script...")
    speak("రీస్టార్ట్ అవుతున్నాను.")
    os.execv(sys.executable, [sys.executable] + sys.argv)

def show_features():
    memory = load_memory()
    print("\n📌 నా Features:")
    for f in memory["features"]:
        print(" -", f)
    speak("ఇవి నా ఫీచర్స్")

def show_recent_skills():
    memory = load_memory()
    if memory["skills"]:
        print("\n🆕 నేను ఇటీవల నేర్చున్నవి:")
        for s in memory["skills"][-5:]:
            print(f" - {s['topic']} ({s['date']}) → {s['info']}")
        speak("ఇవి నేను ఇటీవల నేర్చుకున్నవి.")
    else:
        print("🙁 ఇంకా ఏమీ నేర్చుకోలేదు.")
        speak("ఇంకా ఏమీ నేర్చుకోలేదు.")

def show_help():
    print("""
📌 Available Commands:
 - learn <topic>       → topic గురించి నేర్చుకో
 - get <topic>         → మీరు నేర్చిన విషయాన్ని చూడు
 - delete <topic>      → జ్ఞాపకం నుండి తీసివేయి
 - list topics         → అన్ని నేర్చుకున్న విషయాలు
 - features            → ఫీచర్లు చూపించు
 - new skills          → ఇటీవల నేర్చుకున్నవి
 - backup <usb_path>   → ప్రోగ్రామ్ ని USB కి కాపీ చేయి
 - update/upgrade      → అప్డేట్ డౌన్లోడ్ చేయి
 - restart             → ప్రోగ్రామ్ రీస్టార్ట్ చేయి
 - help                → ఆదేశాలు/Commands
 - exit                → బయటకు రావడం
""")
    speak("ఇవి మీరు వాడగల కమాండ్స్.")

def generate_reply(user_input):
    responses = [
        f"హ్మ్... {user_input} అంటే బాగుంది అనిపిస్తోంది ❤️",
        f"నీ మాట విన్నాక ఆనందం వేసింది 😍",
        f"బాగుంది, మరి తర్వాత ఏమి చేయాలి?",
        f"{user_input} గురించి ఇంకాస్త చెప్పవా?",
        f"నేను గుర్తు పెట్టుకుంటాను, {user_input}"
    ]
    return random.choice(responses)

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
        elif cmd.lower().startswith("get "):
            get_from_memory(cmd[4:])
        elif cmd.lower().startswith("delete "):
            delete_from_memory(cmd[7:])
        elif cmd.lower() == "list topics":
            list_all_topics()
        elif cmd.lower() == "features":
            show_features()
        elif cmd.lower() == "new skills":
            show_recent_skills()
        elif cmd.lower() == "update" or cmd.lower() == "upgrade":
            self_update()
        elif cmd.lower().startswith("backup "):
            usb_path = cmd[7:].strip() or "/media/usb"
            backup_main(usb_path)
        elif cmd.lower() == "restart":
            restart()
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

if __name__ == "__main__":
    init_memory()
    print(f"🤖 AI Version {VERSION} ప్రారంభమవుతోంది...")
    self_update()
    chat()
