import speech_recognition as sr
import os
import subprocess
import random
import difflib
import tempfile

#CHANGE THESE
Common_Sentences = [
    {"original": "Bonjour Comment ça va", "translation": "Hello, how are you?"},
    {"original": "Ça va bien merci Et toi", "translation": "Im fine, thank you. And you?"},
    {"original": "Quel est ton nom", "translation": "What is your name?"},
    {"original": "Je mappelle Claude.", "translation": "My name is Claude."},
    {"original": "Enchanté", "translation": "Pleased to meet you."},
    {"original": "Doù viens-tu", "translation": "Where are you from?"},
    {"original": "Parles-tu anglais", "translation": "Do you speak English?"},
    {"original": "Oui je parle un peu anglais", "translation": "Yes, I speak a little English."},
    {"original": "Je ne parle pas bien français", "translation": "I do not speak French well."},
    {"original": "Pourriez-vous parler plus lentement sil vous plaît", "translation": "Could you speak more slowly, please?"},
    {"original": "Où est la salle de bain", "translation": "Where is the bathroom?"},
    {"original": "Combien ça coûte", "translation": "How much does it cost?"},
    {"original": "Pouvez-vous maider", "translation": "Can you help me?"},
    {"original": "Je voudrais commander poulet sil vous plaît", "translation": "I would like to order chicken, please."},
    {"original": "Laddition sil vous plaît", "translation": "The check, please."},
    {"original": "Je suis perdu", "translation": "I am lost."},
    {"original": "Pouvez-vous me recommander un bon restaurant", "translation": "Can you recommend a good restaurant?"},
    {"original": "Excusez-moi où est la gare", "translation": "Excuse me, where is the train station?"},
    {"original": "Quel temps fait-il aujourdhui", "translation": "What is the weather like today?"},
    {"original": "Je vais visiter le musée demain", "translation": "I am going to visit the museum tomorrow."},
    {"original": "Avez-vous des spécialités locales", "translation": "Do you have any local specialties?"},
    {"original": "Jaimerais réserver une table pour deux personnes", "translation": "I would like to reserve a table for two people."},
    {"original": "Jadore la cuisine française", "translation": "I love French cuisine."},
    {"original": "Jaimerais acheter un billet pour France", "translation": "I would like to buy a ticket to France."},
    {"original": "Pouvons-nous avoir le menu, sil vous plaît", "translation": "May we have the menu, please?"},
    {"original": "je suis une grenouille", "translation": "I am a frog."},
    {"original": "je naime pas les chats", "translation": "I do not like cats."},
    {"original": "je mappelle claude", "translation": "My name is Claude."},
    {"original": "bonjour", "translation": "hello."},
    {"original": "sil te plaît", "translation": "please."}
]

# Initialize the recognizer
r = sr.Recognizer()

done = False


def get_random_sentence():
    sentence_pair = random.choice(Common_Sentences)
    return sentence_pair['original'].lower(), sentence_pair['translation']

def get_random_sentence_fr():
    sentence_pair = random.choice(Common_Sentences)
    return sentence_pair

def wav_to_text(wav_file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_file_path) as source:
        audio_data = recognizer.record(source)
        return recognizer.recognize_google(audio_data, language='fr-FR')
    
# Function to convert text to speech
def speak_text(command, language="en-us"):
    # Select the voice depending on the language
    voice = "Samantha" if language == "en-us" else "Thomas"  #CHANGE THOMAS
    # Using the built-in macOS "say" command for text-to-speech
    subprocess.run(["say", "-v", voice, command])


def prompt_and_repeat(original, sentence):
    done = False
    # Instruction in English with the voice Samantha
    instruction = "Please repeat the following sentence:"
    print(instruction)
    speak_text(instruction)

    # The French sentence with the voice Thomas
    print(original)
    speak_text(original, "THOMAS")  #CHANGE THOMAS
    
    # The English translation
    print(f"The English translation is: {translation}")


    # Use the microphone as source for input
    with sr.Microphone() as source:
        # Adjust for ambient noise and record the audio
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        spoken_text = ""

        # Try to recognize the speech in French
        try:
            spoken_text = r.recognize_google(audio, language="fr-FR") #CHANGE HERE
            spoken_text = spoken_text.lower()
            print("You said: " + spoken_text)

            # Calculate the similarity as a number between 0 and 1
            similarity = difflib.SequenceMatcher(None, original, spoken_text).ratio()
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




# Only run this part if French.py is executed as a script, not when it's imported
if __name__ == "__main__":
    # The French sentence you want the user to repeat
    count = 0
    size = len(Common_Sentences)
    while(count < 3):
        original, translation = get_random_sentence()
        ans = False
        while (not(ans)):
            ans = prompt_and_repeat(original, translation)
        count += 1
    pass
