import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["os", "sys", "PySide6"],  # Add PyQt6 or PySide6 as needed
    "include_files": [
        "audio/",  # Adjust paths as needed
        "resource/",
        "icon.ico"
    ],
    "excludes": [],
    "optimize": 2,
}

# GUI applications require a different base on Windows (the default is for a console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Set base to None for console application

setup(
    name="Thai School Alarm",
    version="1.0",
    description="Thai School Alarm by KruFame",
    options={"build_exe": build_exe_options},
    executables=[Executable("TSAlarm.py", base=base,icon="icon.ico")],
)
