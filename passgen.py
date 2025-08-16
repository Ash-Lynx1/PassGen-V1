#!/usr/bin/env python3
"""
PassGen-V1
Professional Password Generator for Termux (developers edition)
Author: NEXTGEN (remake)
"""

import os
import sys
import time
import random
import string
import zipfile
import shutil
import subprocess
from datetime import datetime

# ----------------------------
# Config & file locations
# ----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
USERS_COUNT_FILE = os.path.join(DATA_DIR, "users_count.txt")
PASSWORDS_FILE = os.path.join(BASE_DIR, "passwords.txt")
WORDLIST_FILE = os.path.join(DATA_DIR, "wordlist.txt")
BANNER_FILE = os.path.join(BASE_DIR, "assets", "banner.txt")

# Channels (labels shown in menu; link opens when selected)
WHATSAPP_CHANNEL = "https://whatsapp.com/channel/0029Vb6K4nw96H4LOMaOLF22"
YOUTUBE_CHANNEL_URL = "https://www.youtube.com/@nexoratechn"

# Termux utilities
HAS_TERMUX_API = shutil.which("termux-clipboard-set") is not None or shutil.which("termux-open-url") is not None

# Ensure data folder and files exist
os.makedirs(DATA_DIR, exist_ok=True)
if not os.path.exists(USERS_COUNT_FILE):
    with open(USERS_COUNT_FILE, "w") as f:
        f.write("0")

# Provide a small wordlist to create 'realistic' passwords
DEFAULT_WORDLIST = [
    "admin", "user", "pass", "dev", "tech", "nexora", "next", "secure",
    "secret", "login", "qwerty", "alpha", "omega", "master", "access",
    "project", "cloud", "root", "sys", "data", "code", "node", "java"
]
if not os.path.exists(WORDLIST_FILE):
    with open(WORDLIST_FILE, "w") as f:
        f.write("\n".join(DEFAULT_WORDLIST))

# ----------------------------
# Utilities
# ----------------------------
def clear():
    os.system("clear" if os.name == "posix" else "cls")

def read_usage_count():
    try:
        with open(USERS_COUNT_FILE, "r") as f:
            return int(f.read().strip() or 0)
    except Exception:
        return 0

def increment_usage_count():
    cnt = read_usage_count() + 1
    with open(USERS_COUNT_FILE, "w") as f:
        f.write(str(cnt))

def load_wordlist():
    try:
        with open(WORDLIST_FILE, "r") as f:
            return [w.strip() for w in f if w.strip()]
    except Exception:
        return DEFAULT_WORDLIST

# Small spinner for UX
def spinner(duration=0.8, msg="Processing"):
    end = time.time() + duration
    spin = "|/-\\"
    i = 0
    while time.time() < end:
        sys.stdout.write(f"\r{msg}... {spin[i % len(spin)]}")
        sys.stdout.flush()
        time.sleep(0.06)
        i += 1
    sys.stdout.write("\r" + " " * (len(msg) + 10) + "\r")

# Display banner (attempt to load assets/banner.txt)
def banner():
    clear()
    banner_text = None
    if os.path.exists(BANNER_FILE):
        try:
            with open(BANNER_FILE, "r", encoding="utf-8") as f:
                banner_text = f.read()
        except Exception:
            banner_text = None

    if not banner_text:
        banner_text = r"""
 ____                                 ____  _____  __   __
|  _ \ __ _ ___ ___  ___  _ __ ___   / ___|| ____| \ \ / /
| |_) / _` / __/ __|/ _ \| '__/ _ \  \___ \|  _|    \ V / 
|  __/ (_| \__ \__ \ (_) | | |  __/   ___) | |___    | |  
|_|   \__,_|___/___/\___/|_|  \___|  |____/|_____|   |_|  
               Professional Password Generator - PassGen-V1
"""
    print("\033[1;36m" + banner_text + "\033[0m")
    print("\033[1;33mTool: PassGen-V1  •  Developer: NEXTGEN TECH\033[0m")
    print(f"\033[1;32mUsage count:\033[0m {read_usage_count()}  •  {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    print("\n\033[1;31mDISCLAIMER:\033[0m This tool is for development/testing only. Do NOT use it to breach accounts, "
          "attack systems, or for illegal activity. The author is not responsible for misuse.\n")

# ----------------------------
# Password generation strategies
# ----------------------------

# 1) Strong random password generator (secure)
def gen_strong_password(length=12):
    if length < 4:
        length = 4
    # ensure at least one from each set
    sets = [
        string.ascii_lowercase,
        string.ascii_uppercase,
        string.digits,
        "!@#$%&*?-_"
    ]
    pw = [random.choice(s) for s in sets]
    allchars = string.ascii_letters + string.digits + "!@#$%&*?-_"
    pw += [random.choice(allchars) for _ in range(length - len(pw))]
    random.shuffle(pw)
    return "".join(pw)

# 2) "Realistic" password generator (mimics common human patterns)
def gen_realistic_password():
    words = load_wordlist()
    word = random.choice(words)
    year = random.choice([str(y) for y in range(1998, 2026)])
    suffixes = ["!", "!", "123", "@", "#", "_", "2023", "2024", "01"]
    leet_map = str.maketrans("aeiosg", "43105g")
    style = random.choice(["word+num", "word+year", "leet+num", "word+symbol", "mixed"])
    if style == "word+num":
        return word + str(random.randint(1, 9999))
    if style == "word+year":
        return word + year
    if style == "leet+num":
        return word.translate(leet_map) + str(random.randint(10,999))
    if style == "word+symbol":
        return word + random.choice(suffixes)
    # mixed: word + Year + Symbol + digit
    return f"{word}{year}{random.choice(suffixes)}"

# 3) Create variations from a base password (user-specified)
def gen_variations_from(base, count=10):
    out = []
    for _ in range(count):
        # randomly insert or append small random tokens
        choice_type = random.choice(["append", "prepend", "insert", "leet", "mix"])
        if choice_type == "append":
            token = str(random.randint(0, 9999)) + random.choice(["!", "@", "#", "_"])
            out.append(base + token)
        elif choice_type == "prepend":
            token = random.choice(["$", "dev", "x", "pro"])
            out.append(token + base)
        elif choice_type == "insert":
            pos = random.randint(0, len(base))
            token = str(random.randint(10,99))
            out.append(base[:pos] + token + base[pos:])
        elif choice_type == "leet":
            tr = str.maketrans("aeios", "43105")
            out.append(base.translate(tr))
        else:
            # mix with a realistic
            out.append(base + random.choice([gen_realistic_password(), gen_strong_password(4)]))
    return out

# 4) Bulk generation wrapper that yields (streaming to file)
def generate_passwords(mode="random", how_many=2000, base=None, realistic_ratio=0.3):
    """
    mode: 'random' or 'custom'
    realistic_ratio: fraction of outputs generated using 'realistic' patterns
    """
    if how_many <= 0:
        return []

    # We'll write directly to file to handle millions without memory blow-up
    with open(PASSWORDS_FILE, "w", encoding="utf-8") as f:
        for i in range(how_many):
            if mode == "custom" and base:
                # produce one variation for each slot (keeps variety)
                pwd = gen_variations_from(base, 1)[0]
            else:
                # decide whether to produce realistic or strong random
                if random.random() < realistic_ratio:
                    pwd = gen_realistic_password()
                else:
                    length = random.randint(8, 16)
                    pwd = gen_strong_password(length)
            f.write(pwd + "\n")
            # optional tiny spinner for big jobs every N items
            if (i + 1) % 500 == 0:
                spinner(0.15, msg=f"generated {i+1}/{how_many}")
    return PASSWORDS_FILE

# ----------------------------
# Post-generation utilities
# ----------------------------
def copy_to_clipboard():
    if shutil.which("termux-clipboard-set"):
        # Use termux cli to set clipboard
        p = subprocess.Popen(["termux-clipboard-set"], stdin=subprocess.PIPE)
        try:
            with open(PASSWORDS_FILE, "rb") as f:
                p.communicate(f.read())
            print("\n[✔] Passwords copied to clipboard (Termux clipboard).")
        except Exception as e:
            print("[!] Failed to copy via termux-clipboard-set:", e)
    else:
        # fallback: try python clipboard via pyperclip if available
        try:
            import pyperclip
            with open(PASSWORDS_FILE, "r", encoding="utf-8") as f:
                data = f.read()
            pyperclip.copy(data)
            print("\n[✔] Passwords copied to clipboard via pyperclip.")
        except Exception:
            print("\n[!] Clipboard not available. Install termux-api or pyperclip to enable copy.")

def open_link(label, url):
    print(f"\nOpening {label} ...")
    if shutil.which("termux-open-url"):
        subprocess.run(["termux-open-url", url])
    else:
        # fallback to webbrowser
        try:
            import webbrowser
            webbrowser.open(url)
        except Exception as e:
            print("[!] Unable to open link automatically. URL:", url)

def make_zip():
    zname = os.path.join(BASE_DIR, f"passwords_{int(time.time())}.zip")
    with zipfile.ZipFile(zname, 'w', zipfile.ZIP_DEFLATED) as z:
        z.write(PASSWORDS_FILE, arcname=os.path.basename(PASSWORDS_FILE))
    print(f"\n[✔] Zipped passwords to: {zname}")
    return zname

# ----------------------------
# Menus
# ----------------------------
def post_generation_menu():
    while True:
        print("\n\033[1;36mPost-generation options:\033[0m")
        print(" [1] Copy passwords")
        print(" [2] Follow WhatsApp channel")
        print(" [3] See YouTube channel")
        print(" [4] Download as ZIP")
        print(" [0] Back to main menu / Exit")
        choice = input("\nSelect option: ").strip()
        if choice == "1":
            copy_to_clipboard()
        elif choice == "2":
            # label only shown; then redirect
            print("Redirecting to WhatsApp channel ...")
            open_link("WhatsApp channel", WHATSAPP_CHANNEL)
        elif choice == "3":
            print("Opening YouTube channel ...")
            open_link("YouTube channel", YOUTUBE_CHANNEL_URL)
        elif choice == "4":
            make_zip()
        elif choice == "0":
            return
        else:
            print("Invalid option. Try again.")

def main_menu():
    increment_usage_count()
    while True:
        banner()
        # Professional-sounding labels (as requested)
        print("\n\033[1;36mMain features:\033[0m")
        print(" [1] Generate random (Secure & Realistic mix)")
        print(" [2] Suggest / Create variations from my password")
        print(" [0] Exit")

        choice = input("\nChoose feature: ").strip()
        if choice == "1":
            # ask how many
            try:
                val = input("\nHow many passwords do you want to generate? (enter any positive number, e.g. 2000): ").strip()
                count = int(val)
                if count <= 0:
                    print("Number must be positive.")
                    continue
            except Exception:
                print("Invalid number. Try again.")
                continue

            print(f"\nGenerating {count} passwords — this may take a moment for very large numbers.")
            spinner(0.5, "Starting generation")
            generate_passwords(mode="random", how_many=count, realistic_ratio=0.36)
            print(f"\n[✔] Done. Saved to {PASSWORDS_FILE}")
            post_generation_menu()

        elif choice == "2":
            base = input("\nEnter your base password (will be used to create variations): ").strip()
            if not base:
                print("Base password cannot be empty.")
                continue
            try:
                val = input("How many variations to generate? (enter any positive number): ").strip()
                count = int(val)
                if count <= 0:
                    print("Number must be positive.")
                    continue
            except Exception:
                print("Invalid number.")
                continue

            print(f"\nGenerating {count} variations based on your password ...")
            spinner(0.5, "Starting generation")
            # If count is small we can do them via gen_variations_from; for large, write progressively
            with open(PASSWORDS_FILE, "w", encoding="utf-8") as f:
                for i in range(count):
                    # produce 1 variation per loop to get variety
                    v = gen_variations_from(base, 1)[0]
                    f.write(v + "\n")
                    if (i + 1) % 500 == 0:
                        spinner(0.12, msg=f"generated {i+1}/{count}")

            print(f"\n[✔] Done. Variations saved to {PASSWORDS_FILE}")
            post_generation_menu()

        elif choice == "0":
            print("\nExiting PassGen-V1. Bye.")
            break
        else:
            print("Invalid option — choose 1, 2, or 0.")

# ----------------------------
# Entry
# ----------------------------
if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting.")
        sys.exit(0)
