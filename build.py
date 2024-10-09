import os
import PyInstaller.__main__

# from subprocess import run
from version import version

main_file = "show_ui.py"
script_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), main_file)


PyInstaller.__main__.run(
    [
        script_path,
        # "--onefile",
        "--name",
        f"amazon_buy_history_{version}",
        "--noconsole",
        # "--add-data",
        # "amazon_buy_history/img",
        "--add-data",
        "settings-example.toml;.",
        "--noconfirm",
    ]
)

# # Create the command for PyInstaller
# cmd = [
#     "pyinstaller",
#     "--onefile",
#     "--name",
#     f"amazon_buy_history_{version}",
#     script_path,
# ]
# # Run PyInstaller and add the version number to the executable
# run(cmd, check=True)
