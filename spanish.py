import speech_recognition as sr
import subprocess
import random
import difflib

#CHANGE THESE
Common_Sentences = [
    {"original": "Hola cómo estás", "translation": "Hello! How are you?"},
    {"original": "Estoy bien gracias", "translation": "I'm fine, thank you."},
    {"original": "Cuál es tu nombre", "translation": "What is your name?"},
    {"original": "Mucho gusto", "translation": "Nice to meet you"},
    {"original": "De dónde eres", "translation": "Where are you from?"},
    {"original": "Hablas inglés", "translation": "Do you speak English?"},
    {"original": "Sí hablo un poco de inglés", "translation": "Yes, I speak a little English"},
    {"original": "No hablo español muy bien", "translation": "I don't speak Spanish very well"},
    {"original": "Puedes hablar más despacio por favor", "translation": "Can you speak more slowly, please?"},
    {"original": "Dónde está el baño", "translation": "Where is the bathroom?"},
    {"original": "Cuánto cuesta esto", "translation": "How much does this cost?"},
    {"original": "Me puedes ayudar", "translation": "Can you help me?"},
    {"original": "La cuenta por favor", "translation": "The bill, please"},
    {"original": "Estoy perdido", "translation": "I am lost"},
    {"original": "Puedes recomendarme un buen restaurante", "translation": "Can you recommend a good restaurant?"},
    {"original": "Disculpe dónde está la estación de tren", "translation": "Excuse me, where is the train station?"},
    {"original": "Qué tiempo hace hoy", "translation": "What is the weather like today?"},
    {"original": "Mañana voy a visitar el museo", "translation": "Tomorrow I am going to visit the museum"},
    {"original": "Tienen especialidades locales", "translation": "Do you have local specialties?"},
    {"original": "Me gustaría reservar una mesa para dos personas", "translation": "I would like to reserve a table for two people"},
    {"original": "Me encanta la comida española", "translation": "I love Spanish food"},
    {"original": "Puedo ver el menú, por favor", "translation": "May I see the menu, please?"},
    {"original": "Estoy aprendiendo español", "translation": "I am learning Spanish"},
    {"original": "Puedes repetir eso por favor", "translation": "Can you repeat that please?"},
    {"original": "Gracias por tu ayuda", "translation": "Thank you for your help"},
    {"original": "No entiendo", "translation": "I don't understand"},
    {"original": "Puedes escribirlo", "translation": "Can you write it down?"},
    {"original": "Hablo español un poco", "translation": "I speak a little Spanish"},
    {"original": "Dónde puedo comprar boletos", "translation": "Where can I buy tickets?"},
    {"original": "Cuál es la contraseña del wifi", "translation": "What's the wifi password?"},
    {"original": "A qué hora cierran", "translation": "What time do you close?"},
    {"original": "Dónde puedo encontrar un taxi", "translation": "Where can I find a taxi?"},
    {"original": "Este plato lleva carne", "translation": "Does this dish contain meat?"},
    {"original": "Soy vegetariano", "translation": "I am a vegetarian"},
    {"original": "Necesito ir al hospital", "translation": "I need to go to the hospital"}
    ]


# Initialize the recognizer
r = sr.Recognizer()

done = False

def get_random_sentence_es():
    sentence_pair = random.choice(Common_Sentences)
    return sentence_pair

def get_random_sentence():
    sentence_pair = random.choice(Common_Sentences)
    return sentence_pair['original'].lower(), sentence_pair['translation']


def wav_to_text(wav_file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_file_path) as source:
        audio_data = recognizer.record(source)
        return recognizer.recognize_google(audio_data, language='es-ES')
    
# Function to convert text to speech
def speak_text(command, language="en-us"):
    # Select the voice depending on the language
    voice = "Samantha" if language == "en-us" else "Monica"  #CHANGE Monica
    # Using the built-in macOS "say" command for text-to-speech
    subprocess.run(["say", "-v", voice, command])


def prompt_and_repeat(original, translation):
    done = False
    # Instruction in English with the voice Samantha
    instruction = "Please repeat the following sentence:"
    print(instruction)
    speak_text(instruction)
       
    # The Spanish sentence with the voice Monica
    print(original)
    speak_text(original, "Monica")  #CHANGE Monica
    
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
            spoken_text = r.recognize_google(audio, language="es-ES") #CHANGE HERE
            spoken_text = spoken_text.lower()
            print("You said: " + spoken_text)

            # Calculate the similarity as a number between 0 and 1
            similarity = difflib.SequenceMatcher(None, original, spoken_text).ratio()
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


# Only run this part if spanish.py is executed as a script, not when it's imported
if __name__ == "__main__":
    # # The Spanish sentence you want the user to repeat
    # for _ in range(3):
    #     original, translation = get_random_sentence_es()
    #     prompt_and_repeat(original, translation)

    count = 0
    size = len(Common_Sentences)
    while(count < 3):
        original, translation = get_random_sentence()
        ans = False
        while (not(ans)):
            ans = prompt_and_repeat(original, translation)
        count += 1
    pass
