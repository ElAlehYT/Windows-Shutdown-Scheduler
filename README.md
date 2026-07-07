# Windows-Shutdown-Scheduler

[![Downloads](https://img.shields.io/github/downloads/ElAlehYT/Windows-Shutdown-Scheduler/total?color=blue&label=Downloads)](https://github.com/ElAlehYT/Windows-Shutdown-Scheduler/releases)
[![Latest Release](https://img.shields.io/github/v/release/ElAlehYT/Windows-Shutdown-Scheduler?label=latest%20release&color=success)](https://github.com/ElAlehYT/Windows-Shutdown-Scheduler/releases/latest)
[![Stars](https://img.shields.io/github/stars/ElAlehYT/Windows-Shutdown-Scheduler?style=social)](https://github.com/ElAlehYT/Windows-Shutdown-Scheduler/stargazers)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Platform](https://img.shields.io/badge/Platform-Windows-informational)
![License](https://img.shields.io/badge/License-MIT-green)

Windows-Shutdown-Scheduler is a lightweight desktop app to **schedule your PC's shutdown** quickly and visually. Features an animated countdown ring, system tray support, fullscreen game detection, and native Windows notifications. No mandatory dependencies, ready to use with a double click.

> ⚠️ **Windows Defender may show a popup** saying "Windows protected your PC" when opening the `.exe`, since it isn't digitally signed. Just click **More info** → **Run anyway**. This is normal for open-source apps without a signing certificate.

## ✨ Features

- **Quick presets**: Now, 1, 5, 15, 30 min, or 1 hour — one click away.
- **Custom time**: set an exact number of hours, minutes, and seconds.
- **Animated countdown**: real-time circular progress ring.
- **System tray support**: minimize the app and it keeps running in the background.
- **Fullscreen game detection**: warns you and lets you postpone the shutdown by 10 minutes if a fullscreen app/game is active, so it won't interrupt your session.
- **Native Windows toast notifications**: on scheduling, cancelling, and when 1 minute is left.
- **Persistent settings**: remembers the last custom time you used.
- **Keyboard shortcut**: `Esc` instantly cancels a running shutdown.

## 🌐 Available languages

- ✅ Spanish (interface)

## 📥 Download

Grab the latest version directly from [**Releases**](https://github.com/ElAlehYT/Windows-Shutdown-Scheduler/releases/latest) — no need to have Python installed.

## 🖥️ Requirements (only if running from source)

- Windows 10/11
- Python 3.x

There are no mandatory external dependencies — the app runs on the standard library alone. For the extra features (system tray and toast notifications):

```bash
pip install pystray pillow win10toast
```

If these aren't installed, the app still runs fine — it just won't show the tray icon or notifications.

## 🚀 Usage

### From source

```bash
python apagado.py
```

### Build your own .exe

1. Install PyInstaller: `pip install pyinstaller`
2. Place `logo.ico` in the same folder as `apagado.py`
3. Run:

```bash
pyinstaller --onefile --windowed --name "Windows-Shutdown-Scheduler" --icon="logo.ico" apagado.py
```

You can also use the included `build.bat` script — just double-click it. The final executable will appear in `dist\Windows-Shutdown-Scheduler.exe`.

## 📸 Screenshots

*(add a GIF or screenshot of the app in action here)*

## 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

## 👤 Author

**ElAlehYT** — [YouTube](https://www.youtube.com/@elalehyt) · [TikTok](https://www.tiktok.com/@elalehyt)
