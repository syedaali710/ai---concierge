import speech_recognition as sr
import pyttsx3
import requests

# Initialize the speech engine
engine = pyttsx3.init()

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen to user's voice and convert to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = recognizer.listen(source)

    try:
        query = recognizer.recognize_google(audio)
        print(f"👂 You said: {query}")
        return query
    except sr.UnknownValueError:
        print("😕 Could not understand audio")
        speak("Sorry, I did not understand that.")
        return None
    except sr.RequestError:
        print("🔌 Could not request results")
        speak("Network error.")
        return None

def send_to_api(query):
    """Send the voice text to FastAPI endpoint."""
    url = "http://127.0.0.1:8000/ask"
    auth = ("datababe", "drsamah710")  # Basic Auth
    json_data = {"query": query}

    try:
        response = requests.post(url, auth=auth, json=json_data)
        if response.status_code == 200:
            data = response.json()
            if data["results"]:
                return data["results"][0]["answer"]
            else:
                return "Sorry, I couldn't find anything."
        else:
            return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

# MAIN LOOP
while True:
    query = listen()
    if query:
        if "stop" in query.lower():
            speak("Goodbye!")
            break
        else:
            answer = send_to_api(query)
            print(f" Answer: {answer}")
            speak(answer)
