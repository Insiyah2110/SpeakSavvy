import speech_recognition as sr
import subprocess
import random
import difflib

Common_Sentences = [
    "Bonjour! Comment ça va", 
    "Ça va bien, merci. Et toi" ,
    "Quel est ton nom",
    "Je m'appelle Claude." ,
    "Enchanté",
    "D'où viens-tu",
    "Parles-tu anglais",
    "Oui, je parle un peu anglais",
    "Je ne parle pas bien français",
    "Pourriez-vous parler plus lentement, s'il vous plaît",
    "Où est la salle de bain",
    "Combien ça coûte",
    "Pouvez-vous m'aider",
    "Je voudrais commander poulet, s'il vous plaît",
    "L'addition, s'il vous plaît",
    "Je suis perdu",
    "Pouvez-vous me recommander un bon restaurant",
    "Excusez-moi, où est la gare",
    "Quel temps fait-il aujourd'hui",
    "Je vais visiter le musée demain",
    "Avez-vous des spécialités locales",
    "J'aimerais réserver une table pour deux personnes" ,
    "J'adore la cuisine française!" ,
    "J'aimerais acheter un billet pour France" , 
    "Pouvons-nous avoir le menu, s'il vous plaît?" 
    ]

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
            spoken_text = spoken_text.lower()
            print("You said: " + spoken_text)

            # Calculate the similarity as a number between 0 and 1
            similarity = difflib.SequenceMatcher(None, sentence, spoken_text).ratio()
            print(f"Similarity: {similarity:.2f}")

            # Define a threshold for considering the repetition to be correct
            threshold = 0.8  # For example, 80% similarity

            if similarity > threshold:
                print("The spoken text is a close match to the sentence.")
                done = True
            else:
                print("The spoken text does not match the sentence well enough.")
                speak_text("Let's try again. Please repeat the sentence.", "Samantha")


        except sr.UnknownValueError:
            # If speech is unintelligible
            print("I couldn't understand what you said. Please try again.")
            # Repeat the instruction in English
            speak_text("I couldn't understand what you said. Please try again.")
        except sr.RequestError:
            # If there's a problem with the speech recognition service
            print("Could not request results; check your internet connection.")


# The French sentence you want the user to repeat
count = 0
L = ["voulez-vous coucher avec moi", "je suis une grenouille", "je n'aime pas les chats", "je m'appelle claude", "bonjour", "s'il te plaît"]
size = len(L)
while(count < 10):
    choice = random.randint(0, size-1)
    sentence_to_repeat = L[choice].lower()

    while (not(done)):
        prompt_and_repeat(sentence_to_repeat)
        #if(not(done)):
        #    print("Please Try Again")
    count += 1



prompt_and_repeat(sentence_to_repeat)

#please try again until you get it 
#also loop for different scentences