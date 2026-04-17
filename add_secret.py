import keyring
import getpass
import sys
import os

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


def update_env(account_name):
    env_file = ".env"
    new_line = f"OTP_ACCOUNT={account_name}\n"
    lines = []
    found = False

    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            lines = f.readlines()

    new_content = []
    for line in lines:
        if line.startswith("OTP_ACCOUNT="):
            new_content.append(new_line)
            found = True
        else:
            new_content.append(line)

    if not found:
        new_content.append(new_line)

    with open(env_file, "w") as f:
        f.writelines(new_content)


def add_secret():
    service = sys.argv[1] if len(sys.argv) > 1 else input("Service name: ").strip()
    default_name = os.getenv("OTP_ACCOUNT", getpass.getuser())
    user_input = input(f"Username [Standard: {default_name}]: ").strip()
    user = user_input if user_input else default_name
    secret = getpass.getpass("Secret (hidden): ").replace(" ", "")

    if secret:
        keyring.set_password(service, user, secret)
        update_env(user)
        print(f"Saved for {user}")


if __name__ == "__main__":
    add_secret()
