#!/usr/bin/env python3

import json
import os
import csv
import time
import sys


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
            paths.append(tuple(new_path))
            extract_key_paths(value, new_path, paths)
    elif isinstance(obj, list):
        for item in obj:
            extract_key_paths(item, current_path, paths)

    return paths


def find_list_keys(data, path=''):
    list_keys = []

    if isinstance(data, dict):
        for key, value in data.items():
            new_path = f"{path} -> {key}" if path else key
            result = find_list_keys(value, new_path)
            list_keys.extend(result)
    elif isinstance(data, list):
        return [path]

    return list_keys


def folder_json(data_list, data_list_combined):
    folder_path = '/home/XXX/JSONS'
    # Liste der Dateien im Ordner
    file_list = os.listdir(folder_path)
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
                data_list = key_paths
            else:
                # Vergleiche die Werte für jeden Index in der Liste und speichere den maximalen Wert
                for key in key_paths:
                    data_list.append(key)

            formatted_combined_data = [' -> '.join(path) for path in data_list]
            unique_combined_data = list(set(formatted_combined_data))

            # Speichere die kombinierten Daten in einer neuen Datei
            combined_data_filename = "combined_data.txt"
            combined_data_path = os.path.join(output_folder_path, combined_data_filename)

            write_txt(combined_data_path, unique_combined_data)

            list_keys = find_list_keys(loaded_json)
            if index == 0:
                data_list_combined = list_keys
            else:
                # Vergleiche die Werte für jeden Index in der Liste und speichere den maximalen Wert
                for key in list_keys:
                    data_list_combined.append(key)

            unique_combined_list_keys = list(set(data_list_combined))
            list_keys_filename = "list_keys.txt"
            list_keys_path = os.path.join(output_folder_path, list_keys_filename)
            write_txt(list_keys_path, unique_combined_list_keys)


def csv_json(data_list, data_list_combined, csv_file_path):
    previous_list_keys = set()
    previous_combined_set = set()

    list_keys_filename = "list_keys.txt"
    list_keys_path = os.path.join(output_folder_path, list_keys_filename)
    # Speichere die kombinierten Daten in einer neuen Datei
    combined_data_filename = "combined_data.txt"
    combined_data_path = os.path.join(output_folder_path, combined_data_filename)

    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)

        for index, row in enumerate(reader):
            json_data_str = row['content']
            json_data = json.loads(json_data_str)

            list_keys = find_list_keys(json_data)
            if index == 0:
                data_list_combined = set(list_keys)
            else:
                data_list_combined.update(list_keys)

            unique_combined_list_keys = data_list_combined

            if unique_combined_list_keys != previous_list_keys:
                print(index)
                previous_list_keys = unique_combined_list_keys

            key_paths = extract_key_paths(json_data)
            if index == 0:
                data_list = set(key_paths)
            else:
                data_list.update(key_paths)

            formatted_combined_data = {' -> '.join(path) for path in data_list}

            if formatted_combined_data != previous_combined_set:
                print(index)
                previous_combined_set = formatted_combined_data

    write_txt(list_keys_path, sorted(unique_combined_list_keys))
    write_txt(combined_data_path, sorted(previous_combined_set))


if __name__ == '__main__':
    start_time = time.time()

    if len(sys.argv) > 2:
        input_file_string = sys.argv[1]
        output_folder_name = sys.argv[2]
    else:
        print("Please input the path of a csv file and the name of the output folder.")
        sys.exit(1)

    input_file_path, input_file_name = os.path.split(input_file_string)

    # Erstelle den Pfad für den Ausgabeordner
    output_folder_path = os.path.join(input_file_path, output_folder_name)
    # Erstelle den Ausgabeordner, falls er noch nicht existiert
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
    # Kombinierte Daten speichern
    combined_data = []
    combined_list_keys = []

    csv_json(combined_data, combined_list_keys, input_file_string)
    # folder_json(combined_data, combined_list_keys)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"The program took {elapsed_time:.2f} seconds to run.")