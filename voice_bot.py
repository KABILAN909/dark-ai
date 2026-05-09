import speech_recognition as sr
import pyttsx3
from groq import Groq
import os
import webbrowser

# GROQ API
client = Groq(
    api_key="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"
)

# Voice engine
engine = pyttsx3.init()

# Speech recognizer
recognizer = sr.Recognizer()

def speak(text):

    print("Bot:", text)

    engine.say(text)

    engine.runAndWait()

while True:

    try:

        with sr.Microphone() as source:

            print("Listening... 🎤")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=5
            )

            user_text = recognizer.recognize_google(audio)

            print("You:", user_text)

            # STOP
            if "stop" in user_text.lower():

                speak("Goodbye")

                break

            # OPEN CHROME
            if "open chrome" in user_text.lower():

                speak("Opening Chrome")

                os.system("start chrome")

                continue

            # OPEN YOUTUBE
            if "open youtube" in user_text.lower():

                speak("Opening YouTube")

                webbrowser.open("https://youtube.com")

                continue

            # OPEN GOOGLE
            if "open google" in user_text.lower():

                speak("Opening Google")

                webbrowser.open("https://google.com")

                continue

            # OPEN VS CODE
            if "open vs code" in user_text.lower():

                speak("Opening VS Code")

                os.system("code")

                continue

            # AI CHAT
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": user_text
                    }
                ]
            )

            reply = completion.choices[0].message.content

            speak(reply)

    except Exception as e:

        print("Error:", e)

        continue