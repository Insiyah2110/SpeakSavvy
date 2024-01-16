import speech_recognition as sr
import subprocess
import random
import difflib

#CHANGE THESE
Common_Sentences = [
    {"original": "Привет", "translation": "Hello."},
    {"original": "Как дела", "translation": "How are you?"},
    {"original": "Как тебя зовут", "translation": "What is your name?"},
    {"original": "Приятно познакомиться", "translation": "Nice to meet you."},
    {"original": "Откуда ты", "translation": "Where are you from?"},
    {"original": "Ты говоришь по-английски", "translation": "Do you speak English?"},
    {"original": "Да я немного говорю по-английски", "translation": "Yes, I speak a little English."},
    {"original": "Я плохо говорю по-русски", "translation": "I don't speak Russian very well."},
    {"original": "Можешь говорить помедленнее", "translation": "Can you speak more slowly, please?"},
    {"original": "Где туалет", "translation": "Where is the bathroom?"},
    {"original": "Сколько это стоит", "translation": "How much does this cost?"},
    {"original": "Помогите мне пожалуйста", "translation": "Please help me."},
    {"original": "Я потерялся", "translation": "I am lost."},
    {"original": "Можете посоветовать хороший ресторан", "translation": "Can you recommend a good restaurant?"},
    {"original": "Извините где находится станция метро", "translation": "Excuse me, where is the metro station?"},
    {"original": "Какая сегодня погода", "translation": "What's the weather like today?"},
    {"original": "Завтра я пойду в музей", "translation": "Tomorrow I will go to the museum."},
    {"original": "У вас есть местные специальности", "translation": "Do you have any local specialties?"},
    {"original": "Я бы хотел забронировать столик на двоих", "translation": "I would like to reserve a table for two."},
    {"original": "Мне очень нравитсярусская кухня", "translation": "I really like Russian cuisine."},
    {"original": "Можно меню пожалуйста", "translation": "May I have the menu, please?"},
    {"original": "Как вы сказали", "translation": "What did you say?"},
    {"original": "Я учу русский язык", "translation": "I am learning Russian."},
    {"original": "Можете это повторить", "translation": "Could you repeat that, please?"},
    {"original": "Спасибо за помощь", "translation": "Thank you for your help."},
    {"original": "Я не понимаю", "translation": "I don't understand."},
    {"original": "Можете написать это", "translation": "Can you write it down?"},
    {"original": "Я говорю по-русски не очень хорошо", "translation": "I do not speak Russian very well."},
    {"original": "Где я могу купить билеты", "translation": "Where can I buy tickets?"},
    {"original": "Какой пароль от Wi-Fi", "translation": "What is the Wi-Fi password?"},
    {"original": "Во сколько закрываетесь", "translation": "What time do you close?"},
    {"original": "Где я могу найти такси", "translation": "Where can I find a taxi?"},
    {"original": "Содержит ли это блюдо мясо", "translation": "Does this dish contain meat?"},
    {"original": "Я вегетарианец", "translation": "I am a vegetarian."},
    {"original": "Мне нужен врач", "translation": "I need a doctor."}
    ]

# Initialize the recognizer
r = sr.Recognizer()

done = False

def get_random_sentence_ru():
    sentence_pair = random.choice(Common_Sentences)
    return sentence_pair

def get_random_sentence():
    sentence_pair = random.choice(Common_Sentences)
    return sentence_pair['original'].lower(), sentence_pair['translation']

def wav_to_text(wav_file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_file_path) as source:
        audio_data = recognizer.record(source)
        return recognizer.recognize_google(audio_data, language='ru-RU')
    
# Function to convert text to speech
def speak_text(command, language="en-us"):
    # Select the voice depending on the language
    voice = "Samantha" if language == "en-us" else "Yuri"  #CHANGE Yuri
    # Using the built-in macOS "say" command for text-to-speech
    subprocess.run(["say", "-v", voice, command])


def prompt_and_repeat(original, translation):
    done = False
    # Instruction in English with the voice Samantha
    instruction = "Please repeat the following sentence:"
    print(instruction)
    speak_text(instruction)

    # The Russian sentence with the voice Yuri
    print(original)
    speak_text(original, "Yuri")  #CHANGE Yuri
    
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
            spoken_text = r.recognize_google(audio, language="ru-RU") #CHANGE HERE
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


# Only run this part if russian.py is executed as a script, not when it's imported
if __name__ == "__main__":
    # The Russian sentence you want the user to repeat
    count = 0
    size = len(Common_Sentences)
    while(count < 3):
        original, translation = get_random_sentence()
        ans = False
        while (not(ans)):
            ans = prompt_and_repeat(original, translation)
        count += 1
    pass
