import speech_recognition as sr
import os
import webbrowser
import pyttsx3
import datetime
import requests
from pytube import Search

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Set the voice rate (optional, slows down speech if needed)
engine.setProperty("rate", 150)

# List all available voices and select a female voice
voices = engine.getProperty("voices")
for voice in voices:
    if "female" in voice.name.lower():  # Adjust this based on voice names on your system
        engine.setProperty("voice", voice.id)
        break
else:
    print("Female voice not found. Using default voice.")


def say(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()


def takeCommand():
    """Take voice input from the user."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query.lower()
        except Exception as e:
            say("Sorry, I could not understand. Please try again.")
            return None


def get_weather(city):
    """Fetch and announce live weather information for the given city."""
    api_key = "c234ae7e76b9846b047a3677c80eca07"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()

        if data["cod"] == 200:
            weather = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            say(f"The weather in {city} is {weather} with a temperature of {temp}°C.")
        else:
            say("Sorry, I couldn't fetch the weather information. Please check the city name and try again.")
    except Exception as e:
        say("There was an error fetching the weather data. Please try again later.")


def play_music():
    """Play music or videos from YouTube."""
    say("What song would you like to play?")
    song = takeCommand()
    if song:
        try:
            say("Searching for the song on YouTube...")
            search = Search(song)
            video = search.results[0]  # Get the first search result
            webbrowser.open(video.watch_url)  # Open the video in the web browser
            say("Playing the song on YouTube.")
        except Exception as e:
            say("Sorry, I couldn't fetch the song. Please try again.")


def process_command(command):
    """Process the given voice command."""
    # Command for opening YouTube
    if "open youtube" in command:
        say("Opening YouTube...")
        webbrowser.open("https://www.youtube.com")

    # Command for telling time
    elif "time" in command:
        now = datetime.datetime.now().strftime("%H:%M")
        say(f"The time is {now}")

    # Command for fetching weather
    elif "weather" in command:
        say("Which city's weather would you like to know?")
        city = takeCommand()
        if city:
            get_weather(city)

    # Command for playing music
    elif "play music" in command:
        play_music()

    # Default response for unknown commands
    else:
        say("I'm sorry, I didn't understand that.")

    # Task is completed, exit the program
    say("Task completed. Exiting Jarvis.")
    exit(0)


if __name__ == '__main__':
    while True:
        print("Waiting for wake word...")
        query = takeCommand()
        if query and "hey jarvis" in query:
            say("Jarvis is ready. What can I do for you?")
            command = takeCommand()
            if command:
                process_command(command)
