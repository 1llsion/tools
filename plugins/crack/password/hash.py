import hashlib
import bcrypt
from assets.colors.colors import colors

def detect_hash_type(password_hash):
    hash_types = [
        ("md2", 32),
        ("md4", 32),
        ("md5", 32),
        ("mysql", 16),
        ("sha1", 40),
        ("sha224", 56),
        ("sha256", 64),
        ("sha384", 96),
        ("sha512", 128),
        ("sha3_256", 64),
        ("blake2b", 128)
    ]

    for hash_name, length in hash_types:
        if len(password_hash) == length:
            return hash_name
    if password_hash.startswith("$2"):
        return "bcrypt"
    return None

def engine(password_hash):
    try:
        crack = open("assets/path/file/wordpass.txt", "r", encoding="utf-8")
    except FileNotFoundError:
        print(f"{colors.red}[{colors.reset}✗{colors.red}]{colors.reset} Oh shit... File not found bro")
        return
    
    hash_type = detect_hash_type(password_hash)
    if hash_type is None:
        print(f"{colors.magenta}[{colors.reset}‽{colors.red}]{colors.reset} Unknown hash type. Cannot crack.")
        return
    
    for passwordCrack in crack:
        trying = passwordCrack.encode("utf-8")
        if hash_type == "bcrypt":
            trying_hash = bcrypt.hashpw(trying.strip(), password_hash.encode())
            if trying_hash.decode() == password_hash:
                print(f"{colors.green}[{colors.reset}✓{colors.green}]{colors.reset} Password has been found: {passwordCrack}")
                return
        else:
            run = getattr(hashlib, hash_type)(trying.strip()).hexdigest().lower()
            if run == password_hash:
                print(f"{colors.green}[{colors.reset}✓{colors.green}]{colors.reset} Password has been found: {passwordCrack}")
                return
    
    print(f"{colors.red}[{colors.reset}✗{colors.red}]{colors.reset} Password not found.")

def HashPass():
    cmd = input(f"{colors.yellow}input your password hash => {colors.reset}")
    engine(cmd.lower())
