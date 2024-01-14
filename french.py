import speech_recognition as sr
import subprocess
import random
import difflib

#CHANGE THESE
Common_Sentences = [
    "Bonjour Comment ça va", 
    "Ça va bien merci Et toi" ,
    "Quel est ton nom",
    "Je mappelle Claude." ,
    "Enchanté",
    "Doù viens-tu",
    "Parles-tu anglais",
    "Oui je parle un peu anglais",
    "Je ne parle pas bien français",
    "Pourriez-vous parler plus lentement sil vous plaît",
    "Où est la salle de bain",
    "Combien ça coûte",
    "Pouvez-vous maider",
    "Je voudrais commander poulet sil vous plaît",
    "Laddition sil vous plaît",
    "Je suis perdu",
    "Pouvez-vous me recommander un bon restaurant",
    "Excusez-moi où est la gare",
    "Quel temps fait-il aujourd hui",
    "Je vais visiter le musée demain",
    "Avez-vous des spécialités locales",
    "Jaimerais réserver une table pour deux personnes" ,
    "Jadore la cuisine française" ,
    "Jaimerais acheter un billet pour France" , 
    "Pouvons-nous avoir le menu, sil vous plaît", 
	"voulez-vous coucher avec moi", "je suis une grenouille", "je naime pas les chats", "je mappelle claude", "bonjour", "sil te plaît"
    ]

# Initialize the recognizer
r = sr.Recognizer()

done = False

def get_random_sentence():
    return random.choice(Common_Sentences).lower()

def wav_to_text(wav_file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_file_path) as source:
        audio_data = recognizer.record(source)
        try:
            # Using Google Web Speech API to recognize audio
            text = recognizer.recognize_google(audio_data, language='fr-FR')
            return text
        except sr.UnknownValueError:
            # Error handling for unintelligible speech
            return "Speech Recognition could not understand the audio"
        except sr.RequestError as e:
            # Error handling for service request issues
            return f"Could not request results from Speech Recognition service; {e}"
        
# Function to convert text to speech
def speak_text(command, language="en-us"):
    # Select the voice depending on the language
    voice = "Samantha" if language == "en-us" else "Thomas"  #CHANGE THOMAS
    # Using the built-in macOS "say" command for text-to-speech
    subprocess.run(["say", "-v", voice, command])

def prompt_and_repeat(sentence, bloob):
    done = False
    # # Instruction in English with the voice Samantha
    # instruction = "Please repeat the following sentence:"
    # print(instruction)
    # speak_text(instruction)

    # # The French sentence with the voice Thomas
    # print(sentence)
    # speak_text(sentence, "Thomas")  #CHANGE THOMAS
    

    # Use the microphone as source for input
    # with sr.Microphone() as source:
        # Adjust for ambient noise and record the audio
        # r.adjust_for_ambient_noise(source)
        # audio = r.listen(source)
        # spoken_text = ""

        # Try to recognize the speech in French
    try:
        # spoken_text = r.recognize_google(audio, language="fr-FR") 
        spoken_text = wav_to_text(bloob)
        spoken_text = spoken_text.lower()
        print("You said: " + spoken_text)

            # Calculate the similarity as a number between 0 and 1
        similarity = difflib.SequenceMatcher(None, sentence, spoken_text).ratio()
        print(f"Similarity: {similarity:.2f}")

            # Define a threshold for considering the repetition to be correct
            #threshold = 0.95  # For example, 80% similarity

        if similarity > 0.95:
            print("Great Job!")
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


# Only run this part if French.py is executed as a script, not when it's imported
if __name__ == "__main__":
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
    pass