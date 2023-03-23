import json
import os


def read_json(file_path):
    try:
        # JSON von einer Datei laden
        with open(file_path, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
            return data
    except json.JSONDecodeError as e:
        print(f'Fehler beim Laden der JSON-Datei "{file_path}": {e}')
        return None


def write_txt(file_path, stuff):
    stuff.sort()
    list_to_print = manipulate_list(stuff)
    # JSON in eine Datei schreiben
    with open(file_path, "w", encoding="utf-8") as txt_file:
        txt_file.write(list_to_print)


def manipulate_list(list):
    # Zeilenumbruch zwischen Listeneinträgen einfügen
    content = '\n'.join(list)
    return content

def find_depth(obj, current_depth=1):
    if isinstance(obj, dict):
        max_depth = current_depth
        for key in obj:
            depth = find_depth(obj[key], current_depth + 1)
            max_depth = max(max_depth, depth)
        return max_depth
    elif isinstance(obj, list):
        max_depth = current_depth
        for item in obj:
            depth = find_depth(item, current_depth + 1)
            max_depth = max(max_depth, depth)
        return max_depth
    else:
        return current_depth


def extract_keys(obj, keys=None):
    if keys is None:
        keys = set()

    if isinstance(obj, dict):
        for key, value in obj.items():
            keys.add(key)
            extract_keys(value, keys)
    elif isinstance(obj, list):
        for item in obj:
            extract_keys(item, keys)

    return keys


def extract_values(obj, values=None):
    if values is None:
        values = []

    if isinstance(obj, dict):
        for value in obj.values():
            extract_values(value, values)
    elif isinstance(obj, list):
        for item in obj:
            extract_values(item, values)
    else:
        values.append(obj)

    return values


def extract_key_paths(obj, current_path=None, paths=None):
    if current_path is None:
        current_path = []
    if paths is None:
        paths = []

    if isinstance(obj, dict):
        for key, value in obj.items():
            new_path = current_path + [key]
            paths.append(new_path)
            extract_key_paths(value, new_path, paths)
    elif isinstance(obj, list):
        for item in obj:
            extract_key_paths(item, current_path, paths)

    return paths


if __name__ == '__main__':
    folder_path = '/home/peter/Schreibtisch/JSONS'
    output_folder_name = 'output'

    # Erstelle den Pfad für den Ausgabeordner
    output_folder_path = os.path.join(folder_path, output_folder_name)
    # Erstelle den Ausgabeordner, falls er noch nicht existiert
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # Liste der Dateien im Ordner
    file_list = os.listdir(folder_path)
    # Kombinierte Daten speichern
    combined_data = []
    # Durch die Dateien im Ordner iterieren
    for index, filename in enumerate(file_list):
        # Dateipfad erstellen
        file_path = os.path.join(folder_path, filename)
        # Prüfen, ob der Pfad eine Datei ist
        if os.path.isfile(file_path):
            # Erstelle den Ausgabepfad im Ausgabeordner
            filename_without_extension, _ = os.path.splitext(filename)
            txt_filename = f"{filename_without_extension}.txt"
            txt_path = os.path.join(output_folder_path, txt_filename)

            loaded_json = read_json(file_path)
            if loaded_json is None:
                # JSON konnte nicht geladen werden, überspringen
                continue

            keys = extract_keys(loaded_json)

            key_paths = extract_key_paths(loaded_json)
            formatted_key_paths = ['.'.join(path) for path in key_paths]
            unique_key_paths = list(set(formatted_key_paths))

            values = extract_values(loaded_json)
            # Write the Files
            write_txt(txt_path, unique_key_paths)

            if index == 0:
                combined_data = key_paths
            else:
                # Vergleiche die Werte für jeden Index in der Liste und speichere den maximalen Wert
                for key in key_paths:
                    combined_data.append(key)

            formatted_combined_data = [' -> '.join(path) for path in combined_data]
            unique_combined_data = list(set(formatted_combined_data))

            # Speichere die kombinierten Daten in einer neuen Datei
            combined_data_filename = "combined_data.txt"
            combined_data_path = os.path.join(output_folder_path, combined_data_filename)

            write_txt(combined_data_path, unique_combined_data)
