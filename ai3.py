# Healthcare Voice Assistant (simplified version based on your existing app)
import tkinter as tk
from tkinter import scrolledtext, messagebox
import pyttsx3
import threading
import datetime
import speech_recognition as sr
import random

class HealthcareVoiceAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("Healthcare Voice Assistant")
        self.root.geometry("600x500")
        self.root.configure(bg="#2C3E50")

        # Text-to-speech engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 180)

        # Speech recognizer
        self.recognizer = sr.Recognizer()

        # Chat display
        self.chat_display = scrolledtext.ScrolledText(root, font=("Helvetica", 12), bg="#34495E", fg="white", wrap=tk.WORD, state=tk.DISABLED)
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Input box
        self.input_box = tk.Entry(root, font=("Helvetica", 14), bg="#34495E", fg="white")
        self.input_box.pack(fill=tk.X, padx=10, pady=(0, 10))
        self.input_box.bind("<Return>", lambda event: self.process_input())

        # Buttons
        tk.Button(root, text="Send", command=self.process_input, bg="#27AE60", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(root, text="Voice", command=self.voice_input, bg="#2980B9", fg="white").pack(side=tk.LEFT)
        tk.Button(root, text="Exit", command=root.quit, bg="#E74C3C", fg="white").pack(side=tk.RIGHT, padx=10)

        # Healthcare data
        self.qa_data = {
            "what is diabetes": "Diabetes is a chronic condition that affects how your body processes blood sugar.",
            "symptoms of fever": "Common symptoms of fever include high temperature, chills, and sweating.",
            "first aid for burn": "Cool the burn under running water and cover it with a sterile bandage.",
            "how to stay healthy": "Eat balanced meals, exercise regularly, and get enough sleep.",
        }

        self.health_tips = [
            "Drink plenty of water every day.",
            "Get 7-8 hours of sleep regularly.",
            "Take breaks from screens to rest your eyes.",
            "Wash your hands frequently to prevent infections."
        ]

    def speak(self, text):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"Assistant: {text}\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        threading.Thread(target=lambda: self.engine.say(text) or self.engine.runAndWait()).start()

    def process_input(self):
        command = self.input_box.get().strip().lower()
        if command:
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.insert(tk.END, f"You: {command}\n")
            self.chat_display.config(state=tk.DISABLED)
            self.chat_display.see(tk.END)
            self.input_box.delete(0, tk.END)
            self.respond(command)

    def respond(self, command):
        if command in self.qa_data:
            self.speak(self.qa_data[command])
        elif "remind me to take" in command:
            self.set_reminder("your medicine", 1)  # 1 minute for demo
        elif "health tip" in command:
            self.speak(random.choice(self.health_tips))
        elif "time" in command:
            self.speak("Current time is " + datetime.datetime.now().strftime("%I:%M %p"))
        else:
            self.speak("I'm sorry, I don't have information about that yet.")

    def set_reminder(self, medicine, delay_minutes):
        self.speak(f"Reminder set. I will remind you to take {medicine} in {delay_minutes} minute(s).")
        threading.Timer(delay_minutes * 60, lambda: self.speak(f"It's time to take your {medicine}.")).start()

    def voice_input(self):
        self.speak("Listening...")
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, timeout=5)
                command = self.recognizer.recognize_google(audio).lower()
                self.chat_display.config(state=tk.NORMAL)
                self.chat_display.insert(tk.END, f"You: {command}\n")
                self.chat_display.config(state=tk.DISABLED)
                self.chat_display.see(tk.END)
                self.respond(command)
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't catch that.")
        except Exception as e:
            self.speak(f"Error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = HealthcareVoiceAssistant(root)
    root.mainloop()
