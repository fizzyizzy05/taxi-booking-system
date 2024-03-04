# General logging for the booking systen. Not needed, but makes things a bit easier by by having a standard library for system logs.

def error(message): # Critical error occured.
    print(f"error: {message}")
    
def info(message): # General information
    print(f"info: {message}")
    
def warning(message): # Warning, or non-critical issue
    print(f"warning: {message}")