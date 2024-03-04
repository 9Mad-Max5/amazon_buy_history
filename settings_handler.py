import toml
import getpass
import os

from constants import toml_file_path

def load_settings():
    # Lade die Einstellungen aus der TOML-Datei
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

    # Überprüfen, ob der Ordner existiert, andernfalls erstellen
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def update_settings(path):
    with open(toml_file_path, "r") as file:
        settings = toml.load(file)

    # Aktualisiere den Pfad in den Einstellungen
    settings["path"]["output_path"] = path

    # Speichere die aktualisierten Einstellungen zurück in die TOML-Datei
    with open(toml_file_path, "w") as file:
        toml.dump(settings, file)

