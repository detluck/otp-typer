import keyring
import getpass
import sys
import os
import subprocess
import platform

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")
OTP_SCRIPT = os.path.join(BASE_DIR, "otp.py")
PYTHON_EXE = sys.executable

try:
    from dotenv import load_dotenv

    load_dotenv(ENV_PATH)
except ImportError:
    print("Failed to load dotenv")


def update_env(account_name, service_name):
    new_entry = f"{service_name}:{account_name}"
    lines = []
    new_content = []
    current_entries = []
    account_found = False

    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, "r") as f:
            lines = f.readlines()

    for line in lines:
        if line.startswith("OTP_ACCOUNT="):
            new_content.append(f"OTP_ACCOUNT={account_name}\n")
            account_found = True

        elif line.startswith("OTP_SERVICES="):
            raw_services = line.split("=")[1].strip()
            current_entries = [s for s in raw_services.split(",") if s]
        else:
            new_content.append(line)

    if not account_found:
        new_content.insert(0, f"OTP_ACCOUNT={account_name}\n")
    if new_entry not in current_entries:
        current_entries.append(new_entry)

    new_content = [line for line in new_content if not line.startswith("OTP_SERVICES=")]
    new_content.append(f"OTP_SERVICES={','.join(current_entries)}\n")

    with open(ENV_PATH, "w") as f:
        f.writelines(new_content)


def update_env_after_edit(old_entry, new_entry):
    if not os.path.exists(ENV_PATH):
        return

    with open(ENV_PATH, "r") as f:
        lines = f.readlines()

    new_content = []
    for line in lines:
        if line.startswith("OTP_SERVICES="):
            raw_services = line.split("=")[1].strip()
            entries = [s for s in raw_services.split(",") if s]

            if old_entry in entries:
                entries.remove(old_entry)
            if new_entry and new_entry not in entries:
                entries.append(new_entry)

            new_content.append(f"OTP_SERVICES={','.join(entries)}\n")
        else:
            new_content.append(line)

        with open(ENV_PATH, "w") as f:
            f.writelines(new_content)


def edit_manager():
    print("Hier will be manager to edit or deleate otps")


def create_shortcut(service_name, account_name):
    current_os = platform.system()

    print("Creating a shortcut")

    if current_os == "Windows":
        try:
            desktop = os.path.join(os.environ["USERPROFILE"], "Desktop")
            shortcut_path = os.path.join(desktop, f"OTP-{service_name}.lnk")

            powershell_cmd = (
                f"$WshShell = New-Object -ComObject WScript.Shell; "
                f"$Shortcut = $WshShell.CreateShortcut('{shortcut_path}'); "
                f"$Shortcut.TargetPath = '{PYTHON_EXE}'; "
                f"$Shortcut.Arguments = '\"{OTP_SCRIPT}\" {service_name} {account_name}'; "
                f"$Shortcut.WorkingDirectory = '{BASE_DIR}'; "
                f"$Shortcut.WindowStyle = 7; "
                f"$Shortcut.Save()"
            )
            subprocess.run(["powershell", "-Command", powershell_cmd], check=True)
            print(f"Windows shortcut created: Desktop/OTP-{service_name}.lnk")

        except Exception as e:
            print(f"Failed to create shortcut: {e}")

    elif current_os == "Darwin":
        print("You dont need a shorcut, see Readme")

    elif current_os == "Linux":
        print("Cant create a shortcut on linux due to number of DEs")
        print(
            f"Paste this command to your .conf or .desktop file: '{PYTHON_EXE}' '{OTP_SCRIPT}' {service_name} {account_name}"
        )


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "edit":
        edit_manager()
        return

    service = sys.argv[1] if len(sys.argv) > 1 else input("Service name: ").strip()
    default_name = os.getenv("OTP_ACCOUNT", getpass.getuser())
    user_input = input(f"Username [Standard: {default_name}]: ").strip()
    user = user_input if user_input else default_name

    existing_secret = keyring.get_password(service, user)

    if existing_secret:
        print(f"Warning! You already have a secret for {service} {user}")
        overwrite = input("Do you want to overwrite your secret? (y/n)").strip().lower()

        if overwrite not in ["y", "yes"]:
            print("Canceled")
            return
        print("Overwrite confirmed...")

    secret = getpass.getpass("Secret (hidden): ").replace(" ", "")

    if secret:
        keyring.set_password(service, user, secret)
        update_env(user, service)
        print(f"Saved for {user}")
        if platform.system() == "Windows":

            print("\nHow do you want to execute the script?")
            print("[1] Windows-Shortcut on Desktop")
            print("[2] AutoHotkey-Code (.ahk)")
            choice = input("(1/2): ").strip()
        
            if choice == "1":
                create_shortcut(service, user)
            elif choice == "2":
                print(f"<Your keys>::Run('\"{PYTHON_EXE}\" \"{OTP_SCRIPT}\" {service} {user}', , \"Hide\")")
                print("Copy this code to your .ahk file and enter the keybinding for it")
    else:
        print("No secret was inserted")


if __name__ == "__main__":
    main()
