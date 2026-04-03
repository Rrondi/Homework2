import json
import os

DEFAULT_PATH = "data/gradebook.json"


def load_data(path=DEFAULT_PATH):
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        print("File not found")
        return {
            "students": [],
            "courses": [],
            "enrollments": []
        }

    except json.JSONDecodeError:
        print(
            f"Helpful message: The file '{path}' is not valid JSON. Starting with empty data.")
        return {
            "students": [],
            "courses": [],
            "enrollments": []
        }

    except Exception as e:
        print(f"Unexpected error while loading data: {e}")
        return {
            "students": [],
            "courses": [],
            "enrollments": []
        }


def save_data(data, path=DEFAULT_PATH):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    except Exception as e:
        print(f"Unexpected error while saving data: {e}")
