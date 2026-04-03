import json
import os
import logging

DEFAULT_PATH = "data/gradebook.json"


def load_data(path=DEFAULT_PATH):
    """Loads data from a JSON file. If the file does not exist, returns an empty gradebook."""
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
            logging.info(f"Loaded data from {path}")
            return data

    except FileNotFoundError:
        logging.warning(f"File not found: {path}")
        return {
            "students": [],
            "courses": [],
            "enrollments": []
        }

    except json.JSONDecodeError:
        logging.error(f"Invalid JSON in {path}. Starting with empty data.")
        print(f"The file '{path}' is not valid JSON.")
        return {
            "students": [],
            "courses": [],
            "enrollments": []
        }

    except Exception as e:
        logging.error(f"Unexpected error loading data: {e}")
        return {
            "students": [],
            "courses": [],
            "enrollments": []
        }


def save_data(data, path=DEFAULT_PATH):
    """Saves data to a JSON file."""

    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        logging.info(f"Data saved successfully to {path}")

    except Exception as e:
        logging.error(f"Error saving data: {e}")
        print(f"Error saving data: {e}")
