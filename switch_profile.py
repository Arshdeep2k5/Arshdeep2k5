import os
import shutil
import hashlib
import sys

# Reconfigure stdout to support UTF-8 characters (emojis) on Windows console
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

OPTIONS_DIR = "profile_options"
README_PATH = "README.md"

# Descriptions of each option for display
DESCRIPTIONS = {
    "original": "Original GitHub Profile README",
    "1": "The Fighter Jet Cockpit HUD (Aviation/Tactical) [Dark Mode]",
    "2": "RPG Guild Board & Alchemy Book (Fantasy RPG) [Light/Dark]",
    "3": "The 1980s Retro Arcade Machine (Chiptune/Retro) [Dark Mode]",
    "4": "The Minimalist Sumi-e Ink Scroll (Zen) [Light Mode]",
    "5": "The Steampunk Brass Engine (Mechanical/Industrial) [Dark Mode]",
    "6": "The Cyberpunk Hacker Terminal (CLI Console) [Dark Mode]",
    "7": "The Architectural Blueprint (Engineering Draft) [Light/Dark]",
    "8": "The Mycelial Grid (Ecological Bio-Computer) [Dark Mode]",
    "9": "The Cosmic Gravity Chart (Orbit/Space Probe) [Dark Mode]",
    "10": "The Rosetta Stone Cryptogram (Linguistic Decryption) [Light Mode]",
    "11": "The Bioluminescent Neural Grid (Quantum Lab Deck) [Dark Mode] (Custom Bonus)",
}

def get_file_hash(filepath):
    if not os.path.exists(filepath):
        return None
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def detect_active_profile():
    readme_hash = get_file_hash(README_PATH)
    if not readme_hash:
        return "None", "No README.md exists in the root."

    # Check original first
    orig_path = os.path.join(OPTIONS_DIR, "README_original.md")
    if get_file_hash(orig_path) == readme_hash:
        return "original", DESCRIPTIONS["original"]

    # Check other options
    for i in range(1, 12):
        opt_path = os.path.join(OPTIONS_DIR, f"README_option_{i}.md")
        if get_file_hash(opt_path) == readme_hash:
            return str(i), DESCRIPTIONS[str(i)]

    return "unknown", "Custom or modified version (not matching any standby options)"

def list_options(active_key):
    print("\n" + "=" * 65)
    print(" 🛠️  GITHUB PROFILE THEME MANAGER // STANDBY OPTIONS")
    print("=" * 65)
    
    # Show original
    marker = " -> [ ACTIVE ]" if active_key == "original" else ""
    print(f" [original] {DESCRIPTIONS['original']}{marker}")
    print(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    
    # Show options
    for i in range(1, 12):
        key = str(i)
        marker = " -> [ ACTIVE ]" if active_key == key else ""
        print(f" [{key:8}] {DESCRIPTIONS[key]}{marker}")
        
    print("=" * 65)

def apply_profile(key):
    if key == "original":
        source_path = os.path.join(OPTIONS_DIR, "README_original.md")
    else:
        source_path = os.path.join(OPTIONS_DIR, f"README_option_{key}.md")

    if not os.path.exists(source_path):
        print(f"\n[!] Error: Option '{key}' source file does not exist ({source_path})")
        return False

    try:
        shutil.copy(source_path, README_PATH)
        print(f"\n[+] Successfully applied Option [{key}]: {DESCRIPTIONS.get(key, 'Unknown')}")
        return True
    except Exception as e:
        print(f"\n[!] Failed to copy file: {e}")
        return False

def print_help():
    print("Usage:")
    print("  python switch_profile.py           - Launch interactive mode")
    print("  python switch_profile.py list      - List all available standby options")
    print("  python switch_profile.py status    - Show the currently active profile theme")
    print("  python switch_profile.py <option>  - Directly apply an option (e.g. 'original', '1', '5')")

def main():
    active_key, active_desc = detect_active_profile()

    # If arguments are provided
    if len(sys.argv) > 1:
        cmd = sys.argv[1].strip().lower()
        if cmd == "list":
            list_options(active_key)
        elif cmd == "status":
            print(f"\nActive Profile: [{active_key}] - {active_desc}")
        elif cmd in ["help", "--help", "-h"]:
            print_help()
        elif cmd in DESCRIPTIONS:
            apply_profile(cmd)
        else:
            print(f"\n[!] Unknown option or command: '{sys.argv[1]}'")
            print_help()
        return

    # Interactive Mode
    while True:
        active_key, active_desc = detect_active_profile()
        list_options(active_key)
        print(f"Currently active: [{active_key}] - {active_desc}")
        print("\nEnter option key (1-11, 'original', or 'q' to quit): ", end="")
        try:
            choice = input().strip().lower()
        except KeyboardInterrupt:
            print("\nExiting.")
            break
            
        if choice in ['q', 'quit', 'exit']:
            print("Goodbye!")
            break
        elif choice in DESCRIPTIONS:
            apply_profile(choice)
        else:
            print("\n[!] Invalid choice. Please select from the list or press 'q' to exit.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
