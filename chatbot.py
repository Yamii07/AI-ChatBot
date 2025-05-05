from groq import Groq
import speech_recognition as sr
import pyttsx3

# Initialize recognizer and Groq client
engine = pyttsx3.init()
recognizer = sr.Recognizer()
client = Groq(api_key="YOUR_API_KEY_HERE")

print("AI Voice Chatbot (say 'exit' to quit)")

while True:
    with sr.Microphone() as source:
        print("\n🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)  # optional: helps with noise
        audio = recognizer.listen(source)

        try:
            # Transcribe speech to text
            text = recognizer.recognize_google(audio)
            print("You:", text)
        except sr.UnknownValueError:
            print("❌ Could not understand audio.")
            continue
        except sr.RequestError as e:
            print(f"❌ Could not request results: {e}")
            continue

    # Exit condition
    if text.strip().lower() == "exit":
        print("👋 Exiting. Goodbye!")
        break

    # Send to Groq (LLaMA model)
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are my personel assitant"},
            {"role": "user", "content": text}
        ]
    )

    ai_reply = response.choices[0].message.content
    print("Bot:", ai_reply)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[2].id)
    engine.say(ai_reply)
    engine.runAndWait()


