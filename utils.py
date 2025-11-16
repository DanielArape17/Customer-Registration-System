import os

def clear_screen():
    """Clears the console screen based on the operating system."""
    # os.name es 'nt' para Windows, 'posix' para Linux/macOS
    os.system('cls' if os.name == 'nt' else 'clear')