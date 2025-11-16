import json
import re

# --- CONFIGURATION CONSTANTS ---
path = "clients.json"
ARCHIVO_DATOS = path

# Define regex patterns and display names for client fields.
REGEX_FIELDS = {
    "name": [r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s'-]{2,30}$", "Name"],
    "last_name": [r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s'-]{2,30}$", "Lastd Name"],
    "id": [r"^[VEJGP]-\d{7,9}$", "ID"],
    "email": [r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$", "Email"],
    "phone": [r"^\+\d{10,15}$", "Phone"],
}

# --- DATA PERSISTENCE MODULE (JSON) ---

def load_clients(file_path):
    """
    Loads client data from a JSON file.
    Returns an empty list if the file is not found or corrupted.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            clients = json.load(file)
            return clients
    except FileNotFoundError:
        # Returns empty list if the file doesn't exist yet
        return []
    except json.JSONDecodeError:
        # Handles case where the file is found but not valid JSON
        print(f"WARNING: The file '{file_path}' is corrupt.")
        return []

def save_clients(clients, file_path=path):
    """Persists the list of client dictionaries to the specified JSON file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(clients, file, indent=4)
    except Exception as e:
        print(f"ERROR: Could not save file {path}. Details: {e}")