import re
import pywhatkit as kit
from data_manager import load_clients, save_clients, ARCHIVO_DATOS, REGEX_FIELDS
from utils import clear_screen

# --- WHATSAPP UTILITY ---

def send_whatsapp_welcome(phone_number, name):
    """
    Automates sending a welcome message via WhatsApp using pywhatkit.
    Requires an active WhatsApp Web session in the default browser.
    """
    message = f"Hello {name}! 👋\n\nYour registration in our system has been completed successfully. Welcome!"
    
    print("\n[WHATSAPP] Attempting to send welcome message...")
    
    try:
        # Executes the automated send operation with a 25-second wait time.
        kit.sendwhatmsg_instantly(
            phone_no=phone_number, 
            message=message,
            wait_time=300, 
            tab_close=True
        )
        print(f"✅ [WHATSAPP] Message successfully sent to {phone_number}.")
    except Exception as e:
        # Logs the error if automation fails (e.g., WhatsApp Web not logged in or invalid number format).
        print(f"❌ [WHATSAPP] Error sending WhatsApp message. Please ensure WhatsApp Web is open and the number is correct (with country code). Details: {e}")


# --- VALIDATION AND UNIQUENESS MODULE ---

def is_id_unique(client_id, current_client_id=None):
    """Checks if the client ID already exists, excluding the current client's ID during update."""
    clients = load_clients(ARCHIVO_DATOS)
    for client in clients:
        if client.get('id') == client_id:
            if client_id != current_client_id:
                print(f"\n🚫 VALIDATION ERROR: The ID '{client_id}' already exists in the system.")
                return False
    return True

def validate_regex(regex_list, value):
    """Validates a string value against a given regular expression."""
    regex = regex_list[0]
    if re.fullmatch(regex, value):
        return True
    else:
        name_regex = regex_list[1]
        print(f"\n🚫 VALIDATION ERROR: {name_regex}")
        return False

def validate_field(field_key, value, current_id=None):
    """Performs regex validation and uniqueness check (for ID) on a client field."""
    regex_list = REGEX_FIELDS.get(field_key)
    if not regex_list:
        return False
    
    if not validate_regex(regex_list, value):
        return False
    
    if field_key == 'id':
        if not is_id_unique(value, current_id): 
            return False
            
    return True

def get_valid_data(field_name, validation_function):
    """Prompts the user for input repeatedly until validation passes."""
    while True:
        value = input(f"Enter {field_name}: ").strip() 
        if validation_function(value):
            return value

# --- CRUD FUNCTION: CREATE (Includes WhatsApp Call) ---

def create_client():
    """Handles the creation of a new client, including data validation, saving, and sending a welcome message."""
    clear_screen()
    print("\n--- NEW CLIENT REGISTRATION ---")
    
    new_client = {}
    
    # Loop through defined fields to gather and validate data
    for field_key, field_data in REGEX_FIELDS.items():
        input_name = field_data[1].capitalize()
        if field_key == 'id':
            input_name = field_data[1].upper() + " (V-12345678)"
        elif field_key == 'phone':
            input_name += " (+CodeNumber)"
            
        value = get_valid_data(
            input_name, 
            lambda v: validate_field(field_key, v) 
        )
        new_client[field_key] = value

    # Save client to data store
    clients = load_clients(ARCHIVO_DATOS) 
    clients.append(new_client)
    save_clients(clients, ARCHIVO_DATOS)
    
    # Success message
    print(f"\n✅ Client {new_client['name']} {new_client['last_name']} registered successfully! (Total: {len(clients)} saved).")
    
    # Send WhatsApp welcome message
    send_whatsapp_welcome(new_client['phone'], new_client['name'])

# --- SEARCH MODULE ---

def find_matches(all_clients, criterion):
    """Searches client list for matches against the given criterion across all fields."""
    results = []
    normalized_criterion = criterion.strip().lower()
    for client in all_clients:
        searchable_text = " ".join([client.get(k, '') for k in REGEX_FIELDS.keys()]).lower()
        if normalized_criterion in searchable_text:
            results.append(client)
    return results

def display_results(results_list):
    """Prints formatted search results to the console."""
    if not results_list:
        print("\n❌ No clients matched your search criteria.")
        return
    print(f"\n✅ Found {len(results_list)} client(s):")
    separator = "-" * 85
    header = f"| {'#':<3} | {'ID':<12} | {'NAME':<20} | {'EMAIL':<35} |"
    print(separator)
    print(header)
    print(separator)
    for index, client in enumerate(results_list, 1):
        full_name = f"{client.get('name', 'N/A')} {client.get('last_name', '')}"
        line = (
            f"| {index:<3} | {client.get('id', 'N/A'):<12} "
            f"| {full_name:<20} "
            f"| {client.get('email', 'N/A'):<35} |"
        )
        print(line)
    print(separator)

def search_client(): 
    """Provides an interactive loop for searching clients and selecting one for action."""
    clear_screen()
    print("\n--- INTERACTIVE SEARCH MODE ---")
    print("Tip: Enter text to search, 'q' to quit, or press Enter to cancel.")
    
    all_clients = load_clients(ARCHIVO_DATOS)
    if not all_clients:
        print("INFO: No clients registered. Returning to main menu.")
        return None

    while True:
        criterion = input("\nSearch > ").strip()
        if criterion.lower() == 'q':
            print("Exiting search mode.")
            return None 
        if not criterion:
            continue
            
        found_clients = find_matches(all_clients, criterion)
        display_results(found_clients)
        
        if not found_clients:
            continue

        print("\nEnter the number of the client to select (or press Enter to continue searching):")
        selection_input = input("Selection > ").strip()
        
        if not selection_input:
            continue
            
        try:
            selection_index = int(selection_input)
            if 1 <= selection_index <= len(found_clients):
                selected_client = found_clients[selection_index - 1]
                print(f"\n✅ Client selected: {selected_client.get('name')} {selected_client.get('last_name')}")
                return selected_client 
            else:
                print("Invalid number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number or press Enter.")

# --- CRUD FUNCTION: DELETE ---

def delete_client(client_to_delete):
    """Removes a client from the data store after confirmation."""
    client_id = client_to_delete.get('id')
    
    confirmation = input(f"\n⚠️ CONFIRMATION: Are you sure you want to delete client {client_id}? (yes/no): ").strip().lower()
    
    if confirmation != 'yes':
        print(f"Deletion of client {client_id} cancelled.")
        return

    clients = load_clients(ARCHIVO_DATOS)
    new_clients_list = [client for client in clients if client.get('id') != client_id]
    
    if len(new_clients_list) < len(clients):
        save_clients(new_clients_list, ARCHIVO_DATOS)
        print(f"\n✅ SUCCESS: Client {client_id} has been permanently deleted. (Total: {len(new_clients_list)} saved).")
    else:
        print(f"\n❌ ERROR: Client {client_id} was not found in the database. Deletion failed.")

# --- CRUD FUNCTION: UPDATE ---

def update_client(client_to_update):
    """Handles the interactive modification and saving of client data."""
    clear_screen()
    client_id = client_to_update.get('id')
    print(f"\n--- UPDATE CLIENT: {client_to_update.get('name')} {client_to_update.get('last_name')} ({client_id}) ---")
    
    editable_fields = list(REGEX_FIELDS.keys())
    
    while True:
        print("\nFields available for update:")
        
        for i, key in enumerate(editable_fields, 1):
            print(f"  {i}. {REGEX_FIELDS[key][1]}: {client_to_update.get(key)}")
            
        print("  6. SAVE CHANGES and RETURN")
        print("  7. CANCEL and RETURN (Discard changes)")
        
        choice = input("Select a field to edit (1-5) or an action (6/7): ").strip()
        
        if choice == '6':
            break 
        
        if choice == '7':
            print("❌ Update cancelled. Discarding changes.")
            return

        try:
            choice_index = int(choice) - 1
            
            if 0 <= choice_index < len(editable_fields):
                field_key = editable_fields[choice_index]
                field_name = REGEX_FIELDS[field_key][1]
                
                input_prompt = field_name.capitalize()
                if field_key == 'id':
                    input_prompt = field_name.upper() + " (V-12345678)"
                elif field_key == 'phone':
                    input_prompt += " (+CodeNumber)"

                # Pass current_client_id for ID uniqueness check during update
                current_client_id_for_validation = client_id if field_key == 'id' else None
                
                new_value = get_valid_data(f"Enter new {input_prompt}", 
                lambda v: validate_field(field_key, v, current_id=current_client_id_for_validation))
                
                client_to_update[field_key] = new_value
                print(f"✅ Field '{field_name}' updated locally to: {new_value}")

            else:
                print("❌ Invalid selection.")
                
        except ValueError:
            print("❌ Invalid input. Please enter a number.")

    # Persist updated data to the file
    clients = load_clients(ARCHIVO_DATOS)
    
    for i, client in enumerate(clients):
        if client.get('id') == client_id:
            clients[i] = client_to_update
            break
            
    save_clients(clients, ARCHIVO_DATOS)
    print(f"\n✅ SUCCESS: Client {client_to_update.get('name')} {client_to_update.get('last_name')} saved successfully with all changes. (Total: {len(clients)} saved).")