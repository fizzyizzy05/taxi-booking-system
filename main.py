# Base script to use as a frame for project. It opens the different window scripts based on the needs of the user. It can also define variables such as the database that is being used. This script is small, but important, and the other scripts depend on it. 

from tkinter import * # Import all components from 'Tkinter'
from tkinter import messagebox

import login
import logging
import sqlite3
acc = ["Login", ""] 

if __name__ == '__main__':
    logging.info(f"Starting booking system...")
    database = sqlite3.connect(database="data")
    acc = login.window.newWindow(database)
    
    logging.info(f"Account type: {acc[0]}")
    
    # This is developed so that the system can be expanded to allow for Driver and Operator accounts. As it stands, this checks if the user is a customer.
    if acc[0] == "Customer":
        import customer
        customer.window.newWindow(database, acc[1])
    
    logging.info(f"Booking system exited")
