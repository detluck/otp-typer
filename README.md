# OTP Typer

A secure, cross-platform CLI tool to manage your 2FA (TOTP) secrets using the system's native keyring. It generates and automatically types your one-time passwords into login fields, eliminating the need for manual typing.

## Features
- **Secure Storage**: Uses system-native keyrings (Windows Credential Manager, macOS Keychain, GNOME Keyring/KWallet).
- **Auto-Typing**: Automatically types the 6-digit code into the active window.
- **Cross-Platform**: Supports Windows, macOS, and Linux (X11 & Wayland).
- **One-Line Setup**: `add_secret.py` saves the secret, updates config, and creates desktop shortcuts in one go.

---

## 🚀 Installation
 
### 1. Clone the repository
```bash
git clone [https://github.com/detluck/otp-typer.git](https://github.com/detluck/otp-typer.git)
cd otp-typer
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

or manually:

* pyotp
* dotenv
* keyring
* pyautogui or wtype if you are using wayland

## Usage

### Add a new service

Register a new 2FA secret and automatically create a desktop shortcut (Windows/macOS):

```bash
python add_secret.py [service_name]
# Example: python add_secret.py github
```
 
### List registered services

```bash
python add_secret.py list
```

### Type a code

over terminal:

```bash
python otp.py [service_name]
```
or just create a keyboard shortcuts for each service, see description below

## Setting Up Global Keybindings

Since operating systems strictly control access to global keybindings for security reasons, a one-time manual setup is required. Here is how you can assign your OTP Paster to a keyboard shortcut.

### Windows
Windows allows assigning keyboard shortcuts directly to desktop shortcuts.

1. **Create Shortcut**: Run `python add_secret.py [service]`. An icon will appear on your desktop.
2. **Open Properties**: Right-click the new desktop icon -> **Properties**.
3. **Set Hotkey**:
   - Click inside the **Shortcut key** field.
   - Press your desired key combination on your keyboard (e.g., `Ctrl` + `Alt` + `G`).
   - Windows will automatically display the combination in the field.
4. **Save**: Click **Apply** and then **OK**.
5. **Test**: Click into a text input field and press your key combination.

---

### macOS
On macOS, the best method is using the built-in **Shortcuts** app.

1. **Open Shortcuts**: Press `Cmd` + `Space`, type "Shortcuts", and open the app.
2. **New Shortcut**: Click the **+** symbol at the top.
3. **Add Action**:
   - Search for **"Run Shell Script"** on the right sidebar and drag it into the main window.
   - Replace the default text in the box with the absolute path to your Python interpreter and the script:
     ```bash
     /usr/bin/python3 /path/to/your/repo/otp.py [service]
     ```
     *(Tip: Type `which python3` in your terminal to find the correct path).*
4. **Assign Hotkey**:
   - Click the **Info symbol** (small "i") on the right sidebar.
   - Click on **"Add Keyboard Shortcut"**.
   - Press your desired key combination (e.g., `Cmd` + `Option` + `G`).
5. **Test**: Close the app and press the combination while focused on a login field.

---

## Linux (Arch / GNOME / KDE)
Linux desktop environments have excellent built-in menus for custom shortcuts.

### For GNOME
1. **Open Settings**: Go to **Settings** -> **Keyboard** -> **View and Customize Shortcuts**.
2. **Custom Shortcuts**: Scroll all the way down to **Custom Shortcuts**.
3. **Add**:
   - **Name**: `OTP [Service]`
   - **Command**: `python /path/to/your/repo/otp.py [service]`
   - **Shortcut**: Press your desired keys (e.g., `Super` + `U`).

### For KDE Plasma
1. **System Settings**: Go to **Shortcuts** -> **Custom Shortcuts**.
2. **New**: Edit -> New -> Global Shortcut -> Command/URL.
3. **Setup**:
   - **Trigger**: Select your key combination.
   - **Action**: Enter the script path: `python /path/to/your/repo/otp.py [service]`.

### For Window Managers (i3 / Sway / Hyprland)
Simply add a line to your configuration file:
- **i3/Sway**: `bindsym $mod+Shift+g exec python /path/to/otp.py [service]`
- **Hyprland**: `bind = $mainMod SHIFT, G, exec, python /path/to/otp.py [service]`

---

## Tips
To ensure the auto-typing works flawlessly, make sure that:
1. Your cursor is already active and blinking in the correct input field.
2. Time on your device matches your time zone
3. You use the **absolute path** to `otp.py` so the system can execute the script regardless of your current working directory.
