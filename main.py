import speech_recognition as sr
import subprocess
import random

# Initialize the recognizer
r = sr.Recognizer()

done = False

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
        spoken_text = ""

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
        test = (str(spoken_text).lower().lstrip()).rstrip()
        print(";" + test + ";")
        print(";" + sentence_to_repeat + ";")
        if (test == sentence_to_repeat.lower()):
            done = True


# The French sentence you want the user to repeat
count = 0
L = ["voulez vous coucher avec moi", "je suis une grenouille", "je n'aime pas les chats", "je m'appelle claude", "bonjour", "s'il te plaît"]
size = len(L)
while(count < 10):
    choice = random.randint(0, size-1)
    sentence_to_repeat = L[choice]

    while (not(done)):
        prompt_and_repeat(sentence_to_repeat)
        #if(not(done)):
        #    print("Please Try Again")
    count += 1



prompt_and_repeat(sentence_to_repeat)

#please try again until you get it 
#also loop for different scentences