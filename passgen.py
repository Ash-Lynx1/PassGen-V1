#!/usr/bin/env python3
"""
██████╗  █████╗ ███████╗███████╗ ██████╗ ███████╗███╗   ██╗
██╔══██╗██╔══██╗╚══███╔╝██╔════╝██╔═══██╗██╔════╝████╗  ██║
██████╔╝███████║  ███╔╝ █████╗  ██║   ██║█████╗  ██╔██╗ ██║
██╔═══╝ ██╔══██║ ███╔╝  ██╔══╝  ██║   ██║██╔══╝  ██║╚██╗██║
██║     ██║  ██║███████╗███████╗╚██████╔╝███████╗██║ ╚████║
╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝
          PassGen-V1 — Professional Hacker-style Password Generator
          Developer: NEXORA TECH | Termux & Linux Compatible
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

# Channels
WHATSAPP_CHANNEL = "https://whatsapp.com/channel/0029Vb6K4nw96H4LOMaOLF22"
YOUTUBE_CHANNEL_URL = "https://www.youtube.com/@nexoratechn"

# Termux utilities
HAS_TERMUX_API = shutil.which("termux-clipboard-set") is not None or shutil.which("termux-open-url") is not None

# ----------------------------
# Ensure data folder and files exist
# ----------------------------
os.makedirs(DATA_DIR, exist_ok=True)
if not os.path.exists(USERS_COUNT_FILE):
    with open(USERS_COUNT_FILE, "w") as f:
        f.write("0")

DEFAULT_WORDLIST = [
    "admin","user","pass","dev","tech","nexora","next","secure",
    "secret","login","qwerty","alpha","omega","master","access",
    "project","cloud","root","sys","data","code","node","java"
]

def ensure_wordlist():
    """Make sure wordlist file exists and has content"""
    if not os.path.exists(WORDLIST_FILE):
        with open(WORDLIST_FILE, "w") as f:
            f.write("\n".join(DEFAULT_WORDLIST))
    # Load content
    with open(WORDLIST_FILE, "r") as f:
        words = [w.strip() for w in f if w.strip()]
    if not words:
        # fallback if empty
        words = DEFAULT_WORDLIST
    return words

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

# Display banner
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
  ________                      ________                       
 /  _____/_____    _____   ____  \_____  \___  __ ___________   
/   \  ___\__  \  /     \_/ __ \  /   |   \  \/ // __ \_  __ \  
\    \_\  \/ __ \|  Y Y  \  ___/ /    |    \   /\  ___/|  | \/  
 \______  (____  /__|_|  /\___  >\_______  /\_/  \___  >__|     
        \/     \/      \/     \/         \/          \/         
"""
    print("\033[1;36m" + banner_text + "\033[0m")
    print("\033[1;33mTool: PassGen-V1  •  Developer: NEXORA-TECH\033[0m")
    print(f"\033[1;32mUsage count:\033[0m {read_usage_count()}  •  {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    print("\n\033[1;31mDISCLAIMER:\033[0m This tool is for development/testing only. "
          "Do NOT use it for illegal activity. Author not responsible.\n")

# ----------------------------
# Password generation
# ----------------------------
def gen_strong_password(length=12):
    if length < 4:
        length = 4
    sets = [string.ascii_lowercase, string.ascii_uppercase, string.digits, "!@#$%&*?-_"]
    pw = [random.choice(s) for s in sets]
    allchars = string.ascii_letters + string.digits + "!@#$%&*?-_"
    pw += [random.choice(allchars) for _ in range(length - len(pw))]
    random.shuffle(pw)
    return "".join(pw)

def gen_realistic_password():
    words = ensure_wordlist()
    word = random.choice(words)
    year = str(random.randint(1998,2025))
    suffixes = ["!", "123", "@", "#", "_", "2023", "2024"]
    style = random.choice(["word+num", "word+year", "leet+num", "word+symbol", "mixed"])
    if style == "word+num":
        return word + str(random.randint(1,9999))
    if style == "word+year":
        return word + year
    if style == "leet+num":
        tr = str.maketrans("aeios", "43105")
        return word.translate(tr) + str(random.randint(10,99))
    if style == "word+symbol":
        return word + random.choice(suffixes)
    return f"{word}{year}{random.choice(suffixes)}"

def gen_variations_from(base, count=10):
    out = []
    for _ in range(count):
        choice_type = random.choice(["append","prepend","insert","leet","mix"])
        if choice_type=="append":
            token = str(random.randint(0,9999))+random.choice(["!","@","#","_"])
            out.append(base+token)
        elif choice_type=="prepend":
            token = random.choice(["$","dev","x","pro"])
            out.append(token+base)
        elif choice_type=="insert":
            pos=random.randint(0,len(base))
            token=str(random.randint(10,99))
            out.append(base[:pos]+token+base[pos:])
        elif choice_type=="leet":
            tr=str.maketrans("aeios","43105")
            out.append(base.translate(tr))
        else:
            out.append(base+random.choice([gen_realistic_password(),gen_strong_password(4)]))
    return out

def generate_passwords(mode="random", how_many=2000, base=None, realistic_ratio=0.3):
    with open(PASSWORDS_FILE,"w",encoding="utf-8") as f:
        for i in range(how_many):
            if mode=="custom" and base:
                pwd = gen_variations_from(base,1)[0]
            else:
                if random.random()<realistic_ratio:
                    pwd = gen_realistic_password()
                else:
                    length=random.randint(8,16)
                    pwd = gen_strong_password(length)
            f.write(pwd+"\n")
            if (i+1)%500==0:
                spinner(0.15,msg=f"generated {i+1}/{how_many}")
    return PASSWORDS_FILE

# ----------------------------
# Post-generation actions
# ----------------------------
def copy_to_clipboard():
    if shutil.which("termux-clipboard-set"):
        p = subprocess.Popen(["termux-clipboard-set"], stdin=subprocess.PIPE)
        try:
            with open(PASSWORDS_FILE,"rb") as f:
                p.communicate(f.read())
            print("\n[✔] Passwords copied to clipboard (Termux).")
        except Exception as e:
            print("[!] Clipboard failed:", e)
    else:
        try:
            import pyperclip
            with open(PASSWORDS_FILE,"r",encoding="utf-8") as f:
                pyperclip.copy(f.read())
            print("\n[✔] Passwords copied via pyperclip.")
        except Exception:
            print("\n[!] Clipboard unavailable. Install termux-api or pyperclip.")

def open_link(label,url):
    print(f"\nOpening {label} ...")
    if shutil.which("termux-open-url"):
        subprocess.run(["termux-open-url",url])
    else:
        try:
            import webbrowser
            webbrowser.open(url)
        except:
            print(f"[!] Could not open automatically. URL: {url}")

def make_zip():
    zname=os.path.join(BASE_DIR,f"passwords_{int(time.time())}.zip")
    with zipfile.ZipFile(zname,'w',zipfile.ZIP_DEFLATED) as z:
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
        choice=input("\nSelect option: ").strip()
        if choice=="1":
            copy_to_clipboard()
        elif choice=="2":
            open_link("WhatsApp channel",WHATSAPP_CHANNEL)
        elif choice=="3":
            open_link("YouTube channel",YOUTUBE_CHANNEL_URL)
        elif choice=="4":
            make_zip()
        elif choice=="0":
            return
        else:
            print("Invalid option.")

def main_menu():
    increment_usage_count()
    while True:
        banner()
        print("\n\033[1;36mMain features:\033[0m")
        print(" [1] Generate random (Secure & Realistic mix)")
        print(" [2] Suggest / Create variations from my password")
        print(" [0] Exit")

        choice=input("\nChoose feature: ").strip()
        if choice=="1":
            try:
                val=input("\nHow many passwords to generate? (e.g. 2000): ").strip()
                count=int(val)
                if count<=0:
                    print("Must be positive.")
                    continue
            except:
                print("Invalid number.")
                continue
            print(f"\nGenerating {count} passwords...")
            spinner(0.5,"Starting generation")
            generate_passwords(mode="random",how_many=count,realistic_ratio=0.36)
            print(f"\n[✔] Done. Saved to {PASSWORDS_FILE}")
            post_generation_menu()
        elif choice=="2":
            base=input("\nEnter base password: ").strip()
            if not base:
                print("Cannot be empty.")
                continue
            try:
                val=input("How many variations to generate?: ").strip()
                count=int(val)
                if count<=0:
                    print("Must be positive.")
                    continue
            except:
                print("Invalid number.")
                continue
            print(f"\nGenerating {count} variations...")
            spinner(0.5,"Starting generation")
            with open(PASSWORDS_FILE,"w",encoding="utf-8") as f:
                for i in range(count):
                    v=gen_variations_from(base,1)[0]
                    f.write(v+"\n")
                    if (i+1)%500==0:
                        spinner(0.12,msg=f"generated {i+1}/{count}")
            print(f"\n[✔] Done. Saved to {PASSWORDS_FILE}")
            post_generation_menu()
        elif choice=="0":
            print("\nExiting PassGen-V1. Bye.")
            break
        else:
            print("Invalid choice — choose 1, 2, or 0.")

# ----------------------------
# Entry
# ----------------------------
if __name__=="__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting.")
        sys.exit(0)
