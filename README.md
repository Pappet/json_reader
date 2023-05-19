# json_reader

## Description
json_reader is a Python utility that allows you to read and analyze JSON files. It's particularly helpful for data analysis and for situations where you need to write SQL queries based on the data contained in JSON files.
The tool works by taking a CSV file as input, where each row should contain a JSON object. The processed data is then output to a designated folder. The CSV should contain a json in each row.

## Installation
To install json_reader, you'll need to run the provided shell script. You can do this by navigating to the directory containing the script and running the following commands:
```
chmod +x install.sh 
./install.sh
```
This will give the script execute permissions and then run it.

## Usage
To use json_reader, you'll need to provide it with the path to a CSV file containing JSON objects, and the name of an output folder where the results should be written. You can do this with the following command:
```
json_reader /path/to/csv/file "name_of_output_folder"
```
Replace `/path/to/csv/file` with the path to your CSV file, and `"name_of_output_folder"` with the name of the folder where you want the output to be written.

## How It Works
json_reader works by iterating over each row in the provided CSV file and processing the JSON object contained in the row. It extracts keys, values, and key paths from the JSON object and calculates the maximum depth of the object. 
The results are then written to a .txt file in the output folder

The key Python functions in this script include:

- read_json(file_path): Reads a JSON file and returns its content as a Python dictionary. If the file is not a valid JSON, it returns None.
- write_txt(file_path, stuff): Writes the provided data into a .txt file.
- find_depth(obj, current_depth=1): Recursively finds the maximum depth of a JSON object.
- extract_keys(obj, keys=None): Recursively extracts all keys from a JSON object.
- extract_values(obj, values=None): Recursively extracts all values from a JSON object.
- extract_key_paths(obj, current_path=None, paths=None): Recursively extracts all key paths from a JSON object.

## Requirements
json_reader is written in Python and requires Python 3.6 or higher. Ensure you have the corresponding Python version installed on your system.

## Support
If you need support or have questions, please create a new issue in this repository.

## License
This project is open-sourced under the MIT License.

