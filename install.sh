#!/data/data/com.termux/files/usr/bin/bash
set -e

REPO="https://github.com/Ash-Lynx1/PassGen-V1" #replace with your own
DIR="PassGen-V1"

echo -e "\n[PassGen-V1] Starting installation...\n"

apt update -y && apt upgrade -y
pkg install -y python git
# termux-api is required for clipboard and opening links on device
pkg install -y termux-api || true

if [ -d "$DIR" ]; then
  echo "[PassGen-V1] Directory $DIR already exists. Pulling latest..."
  cd "$DIR" && git pull || true
else
  git clone "$REPO" "$DIR" || {
    echo "[ERROR] Could not clone repo. Create folder locally instead."
    mkdir -p "$DIR"
  }
fi

cd "$DIR" || exit 1

# Ensure data folder and usage file exist
mkdir -p data
if [ ! -f data/users_count.txt ]; then
  echo 0 > data/users_count.txt
fi

# Make main script executable
chmod +x passgen.py

echo -e "\n[✔] Installation complete!"
echo -e "Run the tool with: \033[1;36mpython passgen.py\033[0m\n"
