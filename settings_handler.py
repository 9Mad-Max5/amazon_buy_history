import toml
import getpass
import os
import shutil

from constants import toml_file_path

def load_settings():
    # Lade die Einstellungen aus der TOML-Datei
    if not os.path.exists(toml_file_path):
        if not os.path.exists("settings-example.toml"):
            shutil.copyfile(os.path.join("_internal","settings-example.toml"), toml_file_path)
        else:
            shutil.copyfile("settings-example.toml", toml_file_path)

    with open(toml_file_path, "r") as file:
        settings = toml.load(file)

    # Zugriff auf den Pfad zur Amazon-Kaufhistorie
    path = settings["path"]["output_path"]

    # Benutzernamen des aktuellen Benutzers erhalten
    current_user = getpass.getuser()

    if "DeinBenutzer" in path:
        # Ersetze "DeinBenutzer" durch den aktuellen Benutzernamen
        path = path.replace("DeinBenutzer", current_user)
        update_settings(path)
    return path

def update_settings(path):
    with open(toml_file_path, "r") as file:
        settings = toml.load(file)

    create_folders(path)
    
    # Aktualisiere den Pfad in den Einstellungen
    settings["path"]["output_path"] = path

    # Speichere die aktualisierten Einstellungen zurück in die TOML-Datei
    with open(toml_file_path, "w") as file:
        toml.dump(settings, file)

def create_folders(path):
    # Überprüfen, ob der Ordner existiert, andernfalls erstellen
    paths = [path, os.path.join(path, "img"), os.path.join(path, "logs")]
    for p in paths:
        if not os.path.exists(p):
            os.makedirs(p)