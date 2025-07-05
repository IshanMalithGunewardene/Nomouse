# Nomouse - Transparent Grid Overlay for Quick Mouse Positioning

A Python application that provides a transparent overlay grid for quick mouse positioning using two-letter codes.

## Features

- **Global Hotkey**: Press `Ctrl+;` to show the overlay
- **Transparent Overlay**: Always-on-top window covering the entire screen
- **Grid System**: 10x10 grid of two-letter codes (AA, AB, AC, ..., TM)
- **Quick Navigation**: Type any two-letter code to move mouse to that cell
- **Input Blocking**: Overlay blocks mouse/keyboard input to underlying applications
- **Easy Exit**: Press `Escape` to close the overlay

## Installation

### Option 1: Manual Installation
1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application (requires sudo):**
   ```bash
   sudo python3 nomouse.py
   ```

### Option 2: Automatic Service Installation (Recommended)
1. **Run the setup script:**
   ```bash
   sudo ./setup_service.sh
   ```

2. **The app will start automatically on boot and run in the background.**

**Note:** The service installation is recommended as it handles root privileges automatically and starts the app on boot.

## Usage

### If using Manual Installation:
1. **Start the app**: Run `sudo python3 nomouse.py` from the terminal
2. **Show overlay**: Press `Ctrl+;` anywhere on your system
3. **Navigate**: Type any two-letter code (e.g., "AA", "BC", "TM")
4. **Move mouse**: The cursor will automatically move to the center of the selected cell
5. **Close overlay**: Press `Escape` or type a valid code

### If using Service Installation:
1. **The app runs automatically in the background**
2. **Show overlay**: Press `Ctrl+;` anywhere on your system
3. **Navigate**: Type any two-letter code (e.g., "AA", "BC", "TM")
4. **Move mouse**: The cursor will automatically move to the center of the selected cell
5. **Close overlay**: Press `Escape` or type a valid code

### Service Management:
- **Check status**: `sudo systemctl status nomouse`
- **Restart service**: `sudo systemctl restart nomouse`
- **Stop service**: `sudo systemctl stop nomouse`
- **View logs**: `sudo journalctl -u nomouse -f`

## Customization

You can easily modify the app by editing `nomouse.py`:

- **Grid Size**: Change `self.grid_size = 10` in the `NomouseApp.__init__()` method
- **Colors**: Modify the `QColor` values in the `paintEvent()` method
- **Font**: Change the font family and size in the `paintEvent()` method
- **Hotkey**: Modify the hotkey in `keyboard.add_hotkey('ctrl+;', self._show_overlay)`

## Requirements

- Python 3.6+
- Linux Mint (or any Linux distribution)
- X11 display server

## Dependencies

- **PyQt5**: GUI framework for the overlay window
- **keyboard**: Global hotkey detection
- **pyautogui**: Mouse cursor control
- **pynput**: Keyboard input handling

## Troubleshooting

### Permission Issues
If you get permission errors for global hotkeys, you may need to run with sudo:
```bash
sudo python nomouse.py
```

### Display Issues
If the overlay doesn't appear correctly, ensure your display server supports transparency and always-on-top windows.

### Mouse Movement Issues
If mouse movement doesn't work, ensure pyautogui has proper permissions and your display server is compatible.

## License

This project uses only open-source libraries and is provided as-is for educational and personal use. 