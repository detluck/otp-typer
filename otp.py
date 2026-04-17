import pyotp
import keyring
import time
import platform
import os
import sys

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

DEFAULT_ACCOUNT_NAME = os.getenv("OTP_ACCOUNT", "default_user")


def get_otp(service):
    SECRET = keyring.get_password(service, DEFAULT_ACCOUNT_NAME)

    if not SECRET:
        print("No secret found")
        return
    totp = pyotp.TOTP(SECRET.replace(" ", ""))
    code = totp.now()
    time.sleep(0.5)  # Small delay to ensure the user has time to focus the input field
    type_otp(code)


def type_otp(code):
    system = platform.system()
    if system == "Linux":
        # Check if we're running under Wayland or X11
        session_type = os.environ.get("XDG_SESSION_TYPE", "").lower()
        if session_type == "wayland":
            import subprocess

            subprocess.run(["wtype", code])
        else:
            import pyautogui

            pyautogui.write(code)

    elif system in ["Windows", "Darwin"]:
        import pyautogui

        pyautogui.write(code)
    else:
        print(f"Unsupported operating system: {system}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        service = sys.argv[1]
        get_otp(service)
    else:
        print("Usage: otp.py <service_name>")
