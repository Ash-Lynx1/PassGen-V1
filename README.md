# PassGen-V1
Professional Password Generator for Termux — Developer edition.

---

> **Disclaimer:**  
> PassGen-V1 is intended for developer and testing purposes only.  
> Do **not** use generated passwords for any sensitive, production, or personal accounts.  
> The authors/maintainers are not responsible for misuse or any consequences arising from the use of this tool.

---

## Features
- Unlimited password generation (random strong + realistic human-like)
- Create variations from your own password
- Save to `passwords.txt`
- Copy to clipboard (Termux) or fallback
- Download generated passwords as a ZIP
- Usage counter (stored in `data/users_count.txt`)
- Installer script clones repo and sets up dependencies
- Disclaimer included: for dev/testing only

## Install (Termux)

Copy and run each command **one by one**:

```bash
pkg update -y
```

```bash
pkg install git python -y
```

```bash
git clone https://github.com/Ash-Lynx1/PassGen-V1
```

```bash
cd PassGen-V1
```

```bash
bash install.sh
```

```bash
python passgen.py
```
