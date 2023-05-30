import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["tkinter", "requests", "base64", "PIL", "io", "csv"], "include_files": ["logo.ico"]}

base = None
if sys.platform == "win32":
base = "Win32GUI"

setup(name="Image Downloader",
version="1.0",
description="A program to download images from a CSV file",
options={"build_exe": build_exe_options},
executables=[Executable("downloader4.py", base=base, icon="logo.ico")],
)