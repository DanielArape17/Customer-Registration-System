from client_actions import create_client, search_client, update_client, delete_client
from utils import clear_screen 

# --- CLIENT ACTION MANAGEMENT FUNCTION ---

def handle_client_action(client):
    """
    Displays the menu for actions (Update/Delete) on a selected client 
    and processes the user's choice.
    """
    clear_screen()
    while True:
        print("\n--- CLIENT ACTION MENU ---")
        print(f"Client Selected: {client.get('name')} {client.get('last_name')} (ID: {client.get('id')})")
        print("1. Update Client (Modificar datos)")
        print("2. Delete Client (Eliminar cliente)")
        print("3. Return to Main Menu")
        
        action_option = input("Select an action: ").strip()

        if action_option == "1":
            update_client(client) 
            return

        elif action_option == "2":
            delete_client(client)
            return

        elif action_option == "3":
            print("Returning to the Main Menu.")
            return 
            
        else:
            print("❌ Invalid option. Please choose 1, 2, or 3.")


# --- MAIN EXECUTION BLOCK ---

def main_menu():
    """
    Displays the main application menu and handles the primary flow 
    of the Customer Registration System.
    """
    clear_screen()
    while True:
        print("\n--- MAIN MENU ---")
        print("1. Create New Client")
        print("2. Search & Select Client (Update/Delete)")
        print("3. Exit Program")
        
        user_option = input("Select an option: ").strip()

        if user_option == "1":
            create_client() 
            
        elif user_option == "2":
            selected_client = search_client() 
            
            if selected_client:
                handle_client_action(selected_client) 
                
        elif user_option == "3":
            clear_screen()
            print("\n👋 You have exited the program. Goodbye!")
            break 
            
        else:
            print(f"\n❌ The option '{user_option}' is not valid. Please choose from 1, 2, or 3.")

if __name__ == "__main__":
    main_menu()