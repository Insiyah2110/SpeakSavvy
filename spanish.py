import speech_recognition as sr
import subprocess
import random
import difflib

#CHANGE THESE
Common_Sentences = ["por favor", "hola", "Cómo estás"]

# Initialize the recognizer
r = sr.Recognizer()

done = False

# Function to convert text to speech
def speak_text(command, language="en-us"):
    # Select the voice depending on the language
    voice = "Samantha" if language == "en-us" else "Monica"  #CHANGE THOMAS
    # Using the built-in macOS "say" command for text-to-speech
    subprocess.run(["say", "-v", voice, command])

def prompt_and_repeat(sentence):
    done = False
    # Instruction in English with the voice Samantha
    instruction = "Please repeat the following sentence:"
    print(instruction)
    speak_text(instruction)

    # The French sentence with the voice Thomas
    print(sentence)
    speak_text(sentence, "Monica")  #CHANGE THOMAS

    # Use the microphone as source for input
    with sr.Microphone() as source:
        # Adjust for ambient noise and record the audio
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        spoken_text = ""

        # Try to recognize the speech in French
        try:
            spoken_text = r.recognize_google(audio, language="es-ES") #CHANGE HERE
            spoken_text = spoken_text.lower()
            print("You said: " + spoken_text)

            # Calculate the similarity as a number between 0 and 1
            similarity = difflib.SequenceMatcher(None, sentence, spoken_text).ratio()
            print(f"Similarity: {similarity:.2f}")

            # Define a threshold for considering the repetition to be correct
            #threshold = 0.95  # For example, 80% similarity

            if similarity > 0.95:
                print("Great Job! Next Question")
                done = True
            elif similarity > 0.8:
                print("You're Getting There! Keep Practicing.")
            else:
                print("Don't Lose Hope. You'll Get There!")
                speak_text("Let's try again.")


        except sr.UnknownValueError:
            # If speech is unintelligible
            print("I couldn't understand what you said.")
            # Repeat the instruction in English
            speak_text("I couldn't understand what you said.")
        except sr.RequestError:
            # If there's a problem with the speech recognition service
            print("Could not request results; check your internet connection.")

    return done


# The French sentence you want the user to repeat
count = 0
size = len(Common_Sentences)
while(count < 3):
    choice = random.randint(0, size-1)
    sentence_to_repeat = Common_Sentences[choice].lower()
    ans = False
    while (not(ans)):
        ans = prompt_and_repeat(sentence_to_repeat)
    count += 1



#prompt_and_repeat(sentence_to_repeat)

#please try again until you get it 
#also loop for different scentences