# ============================================================
#   Built by: Ssp
#   Project: Alpha - Voice Assistant
#   Description: Custom Python Voice Assistant with multiple tools
#   Date: 2023-24
# ============================================================
import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import sys
import pywhatkit
import time
import psutil
import screen_brightness_control as sbc
import pyautogui
import winshell
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from deep_translator import GoogleTranslator
import speedtest
import pygame
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    print("Alpha:", text)
    engine.say(text)
    engine.runAndWait()

def set_robotic_voice():
    voices = engine.getProperty('voices')
    for voice in voices:
        if "david" in voice.name.lower() or "sam" in voice.name.lower() or "robot" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)
        try:
            query = recognizer.recognize_google(audio, language="en-US")
            print("Ssp:", query)
            return query.lower()
        except sr.UnknownValueError:
            return ""

def set_volume(level):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(level, None)

def translate_text(text, target_language):
    try:
        return GoogleTranslator(source='auto', target=target_language).translate(text)
    except:
        return None

def open_lnk_app(app_name):
    speak(f"Searching for {app_name}")
    paths = [
        os.path.expanduser("~/Desktop"),
        os.path.expanduser("~/Start Menu/Programs"),
        "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs"
    ]
    for path in paths:
        if os.path.exists(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    if app_name.lower() in file.lower() and file.endswith((".lnk", ".exe")):
                        os.startfile(os.path.join(root, file))
                        speak(f"Opening {app_name}")
                        return
    speak(f"Could not find {app_name}")

def check_internet_speed():
    speak("Checking internet speed, please wait.")
    typing_animation("Checking internet speed", 0.05)
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download = round(st.download() / (1024 * 1024), 2)
        upload = round(st.upload() / (1024 * 1024), 2)
        speak(f"Download speed is {download} megabits per second. Upload speed is {upload} megabits per second.")
    except:
        speak("Sorry, I couldn't check your internet speed.")

def open_website(command):
    site = command.replace("open website", "").strip()
    if not site.startswith("http"):
        site = "https://" + site
    speak(f"Opening {site}")
    webbrowser.open(site)

def get_voice_for_language(code):
    for voice in engine.getProperty('voices'):
        langs = getattr(voice, 'languages', [])
        for lang in langs:
            if code in str(lang).lower():
                return voice.id
        if code in voice.name.lower() or code in voice.id.lower():
            return voice.id
    return None

def speak_in_language(text, lang_code):
    original = engine.getProperty('voice')
    new_voice = get_voice_for_language(lang_code)
    if new_voice:
        engine.setProperty('voice', new_voice)
    speak(text)
    engine.setProperty('voice', original)

def typing_animation(text, delay=0.1):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()
def play_custom_audio():
    pygame.mixer.init()
    pygame.mixer.music.load("C:\\Users\\samya\\Downloads\\Nikal laude pehli fursat mein [kQrpynAP9Oc] (mp3cut.net).mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
def system_info():
    battery = psutil.sensors_battery()
    battery_percent = battery.percent if battery else 0
    charging = battery.power_plugged if battery else False
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    total_cores = psutil.cpu_count(logical=True)
    uptime_seconds = time.time() - psutil.boot_time()
    uptime_hours = round(uptime_seconds / 3600, 2)
    cpu_freq = psutil.cpu_freq().current if psutil.cpu_freq() else 0
    disk = psutil.disk_usage('/')
    total_disk = round(disk.total / (1024 ** 3), 1)
    used_disk = round(disk.used / (1024 ** 3), 1)
    free_disk = round(disk.free / (1024 ** 3), 1)
    processes = len(psutil.pids())
    status = f"Battery: {battery_percent}% {'(charging)' if charging else '(not charging)'}. " \
             f"CPU usage: {cpu_usage}%. RAM usage: {ram_usage}%. Total CPU cores: {total_cores}. " \
             f"System uptime: {uptime_hours} hours. CPU Frequency: {cpu_freq} MHz. " \
             f"Disk Total: {total_disk} GB, Used: {used_disk} GB, Free: {free_disk} GB. " \
             f"Active Processes: {processes}."
    speak(status)

def open_system_tool(command):
    if "task manager" in command:
        os.system("taskmgr")
    elif "control panel" in command:
        os.system("control")
    elif "device manager" in command:
        os.system("devmgmt.msc")
    elif "file explorer" in command:
        os.system("explorer")
    speak("Opening system tool.")

def process_command(command):
    if not command:
        return
    if "hello" in command:
        speak("Hello Ssp")
    elif "name" in command:
        speak("My name is Alpha.")
    elif "open notepad" in command:
        os.startfile("notepad.exe")
    elif "open calculator" in command:
        os.startfile("calc.exe")
    elif "open browser" in command:
        webbrowser.open("https://www.google.com")
    elif "search" in command:
        query = command.replace("search", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={query}")
        speak(f"Searching {query}")
    elif "play" in command:
        song = command.replace("play", "").strip()
        speak(f"Playing {song}")
        pywhatkit.playonyt(song)
    elif "terminate" in command or "exit" in command:
        speak("Shutting down.")
        sys.exit()
    elif "set volume" in command:
        try:
            level = float(command.replace("set volume", "").strip())
            if 0.0 <= level <= 1.0:
                set_volume(level)
                speak(f"Volume set to {int(level * 100)}%")
            else:
                speak("Volume must be between 0 and 1.")
        except:
            speak("Invalid volume level.")
    elif "open app" in command:
        open_lnk_app(command.replace("open app", "").strip())
    elif "open website" in command:
        open_website(command)
    elif "translate" in command and "to" in command:
        parts = command.split("to")
        text = parts[0].replace("translate", "").strip()
        lang = parts[1].strip()
        translated = translate_text(text, lang)
        if translated:
            speak_in_language(translated, lang)
        else:
            speak("Translation failed.")
    elif "system info" in command:
        system_info()
    elif "internet speed" in command or "check speed" in command:
        check_internet_speed()
    elif any(x in command for x in ["task manager", "control panel", "device manager", "file explorer"]):
        open_system_tool(command)
    else:
        speak("Sorry couldn't hear")
set_robotic_voice()
speak("Alpha is online.")

while True:
    command = listen()
    process_command(command)
    time.sleep(1)
