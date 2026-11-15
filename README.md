# AeroNotch

**AeroNotch** is a modern, interactive Dynamic Island widget for Windows 10 and 11, built with Python and PyQt6.

It transforms the top edge of your screen into a sleek, compact quick-access hub that stays on top of all windows, never gets in the way, and smoothly expands when hovered over.

## Key Features
* **Minimalist Design:** A dark, translucent pill-shaped widget with rounded corners and smooth 60 FPS animations.
* **Live System Monitoring:** Real-time CPU and RAM usage indicators right at the top of your screen.
* **Media Controls (In Progress):** Displays the currently playing track with quick playback buttons for browsers and media players.
* **Modular Architecture:** Clean, lightweight codebase that is easy to extend with new widgets, a file drop-zone, or a built-in AI mini-chat.
* **Ready-to-Use EXE:** Automatically compiled into a single standalone executable via GitHub Actions — no Python installation required to run.

## Download (Windows EXE)
You don't need to install Python to try AeroNotch:
1. Go to the **Actions** tab (or **Releases**) in this repository.
2. Open the latest successful **Build AeroNotch EXE** workflow run.
3. Download the `AeroNotch-Windows` artifact, extract it, and run `AeroNotch.exe`.

## Run from Source

1. Clone the repository:
   ```bash
   git clone https://github.com/vakarman-dev/AeroNotch?tab=readme-ov-file
   cd AeroNotch
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```
