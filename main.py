import os
import requests
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import pywhatkit
import webbrowser
from openai import OpenAI

# ================================
#       API KEYS (EDIT THIS)
# ================================
OPENAI_API_KEY = ""

os.environ["HF_TOKEN"] = HF_TOKEN

# ---------------- CHATGPT SETUP ----------------
client = OpenAI(api_key=OPENAI_API_KEY)

# ---------- Hugging Face Chat Completion ---------
HF_API_URL = "https://router.huggingface.co/v1/chat/completions"
hf_headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def ask_huggingface(question):
    try:
        response = requests.post(
            HF_API_URL,
            headers=hf_headers,
            json={
                "messages": [{"role": "user", "content": question}],
                "model": "deepseek-ai/DeepSeek-V3.2:novita"
            }
        ).json()

        return response["choices"][0]["message"]["content"]

    except Exception as e:
        return f"HuggingFace Error: {str(e)}"


# ------------ ChatGPT Function ------------
def ask_chatgpt(question):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"OpenAI Error: {e}"


# ================================
#       SPEECH ENGINE
# ================================
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 170)

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()


# ================================
#      VOICE INPUT FUNCTION
# ================================
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        engine.stop()
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}")
        return query.lower()
    except:
        speak("Please say that again...")
        return "none"


# ================================
#       MAIN PROGRAM
# ================================
speak("Hello! Your voice assistant is ready.")

while True:
    query = take_command()

    # ===== User asks questions =====
    if any(word in query for word in ["what", "who", "explain", "define"]):

        speak("Should I use ChatGPT or Hugging Face?")
        choice = take_command()

        if "chatgpt" in choice:
            answer = ask_chatgpt(query)
        else:
            answer = ask_huggingface(query)

        speak(answer)

    # ======= WhatsApp ==========
    elif "send message" in query:
        speak("Whom do you want to message?")
        name = take_command()

        speak("What should I say?")
        message = take_command()

        phone = "+91XXXXXXXXXX"
        speak("Sending message...")
        pywhatkit.sendwhatmsg_instantly(phone, message)
        speak("Message sent successfully.")

    # ========= Time ==========
    elif "time" in query:
        time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {time}")

    # ========= Open Websites ==========
    elif "open youtube" in query:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif "open google" in query:
        speak("Opening Google")
        webbrowser.open("https://google.com")

    # ========= Wikipedia ==========
    elif "wikipedia" in query:
        speak("Searching...")
        topic = query.replace("wikipedia", "")
        result = wikipedia.summary(topic, sentences=2)
        speak(result)

    # ========= Play Song ==========
    elif "play" in query:
        song = query.replace("play", "")
        speak(f"Playing {song}")
        pywhatkit.playonyt(song)

    # ========= Exit ==========
    elif "exit" in query or "stop" in query:
        speak("Goodbye!")
        break
