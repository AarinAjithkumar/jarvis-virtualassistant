import pyttsx3
import speech_recognition as sr
import wikipedia
from decouple import config
from datetime import datetime
from random import choice
from conv import random_text
engine=pyttsx3.init('sapi5')
engine.setProperty('volume',1.5)
engine.setProperty('rate',225)
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)

USER = config('USER')
HOSTNAME = config('BOT')

def speak(text):
    engine.say(text)
    engine.runAndWait()


def search_wikipedia(query):
    try:
        # Set the language (default is English)
        wikipedia.set_lang("en")

        # Search and get summary (first 2 sentences)
        result = wikipedia.summary(query, sentences=2)
        return result
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple results found: {e.options[:5]}... Please specify further."
    except wikipedia.exceptions.PageError:
        return "No Wikipedia page found for your query."
    except Exception as e:
        return f"An error occurred: {e}"

def greet_me():
    hour=datetime.now().hour
    if (hour>=6) and (hour<12):
        speak(f"Good Morning {USER}")
    elif (hour>=12) and (hour<=16):
        speak(f"Good Afternoon {USER}")
    elif (hour>=16) and (hour <19):
        speak(f"Good Evening {USER}")
    speak(f"I am {HOSTNAME}.How may i help you?{USER}")

def take_command():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold=1
        audio=r.listen(source)

    try:
        print("Recognizing...")
        queri=r.recognize_google(audio,language='en-in')
        print(queri)
        if not 'stop' in queri or'exit'in queri:
            speak(choice(random_text))
        else:
            hour=datetime.now().hour
            if (hour >= 21) and (hour<6):
                speak("Good Night sir,take care!")
            else:
                speak("Have a good day!")
            exit()

    except Exception:
         speak("Sorry, I didn't understand that.Can you please repeat?")
         queri='None'
    return queri

if __name__ ==  '__main__':
    greet_me()
    while True:
        query=take_command().lower()
        if "how are you" in query:
            speak("I am absolutely fine sir .What about you")
        else:
            break
    query = input("What would you like to search on Wikipedia? ")
    response = search_wikipedia(query)
    print("\nWikipedia Summary:\n", response)
