import speech_recognition as sr
import subprocess

# Initialize the recognizer
r = sr.Recognizer()

# Function to convert text to speech
def speak_text(command, language="en-us"):
    # Select the voice depending on the language
    voice = "Samantha" if language == "en-us" else "Thomas"
    # Using the built-in macOS "say" command for text-to-speech
    subprocess.run(["say", "-v", voice, command])

def prompt_and_repeat(sentence):
    # Instruction in English with the voice Samantha
    instruction = "Please repeat the following sentence:"
    print(instruction)
    speak_text(instruction)

    # The French sentence with the voice Thomas
    print(sentence)
    speak_text(sentence, "Thomas")

    # Use the microphone as source for input
    with sr.Microphone() as source:
        # Adjust for ambient noise and record the audio
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

        # Try to recognize the speech in French
        try:
            spoken_text = r.recognize_google(audio, language="fr-FR")
            print("You said: " + spoken_text)
        except sr.UnknownValueError:
            # If speech is unintelligible
            print("I couldn't understand what you said. Please try again.")
            # Repeat the instruction in English
            speak_text("I couldn't understand what you said. Please try again.")
        except sr.RequestError:
            # If there's a problem with the speech recognition service
            print("Could not request results; check your internet connection.")

# The French sentence you want the user to repeat
sentence_to_repeat = "La pratique rend parfait."

prompt_and_repeat(sentence_to_repeat)
