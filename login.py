from tkinter import * # Import all components from 'Tkinter'
from tkinter import messagebox
import register
import logging
import sqlite3

class check():            
    def readCredentials(usrIn, passIn, database):
        
        # Check the user has entered something
        if usrIn == "" and passIn == "": # if they haven't
            messagebox.showerror(title="Notice", message="Authentication failed", detail="No username or password was entered") 
        else: # If they have
            # Check if there is a user with that username in the database.
            cursor = database.execute(f"SELECT username from Users where username = '{usrIn}'")
            if len(cursor.fetchall()) == 0: # if there isn't
                # Let the user know that there isn't an account with the username they used.
                messagebox.showerror(title="Notice", message="Authentication failed", detail=f"No user exists with the username {usrIn}. You can create one if you need.") 
            else: # If there is
                # Check if the password is correct
                cursor = database.execute(f"SELECT password from Users where username = '{usrIn}'")
                pw = ""
                for row in cursor:
                    pw = row[0]
                
                if pw == passIn:
                    # Sign in to the booking system as a customer. 
                    logging.info(f"Signing in as {usrIn}")
                    window.acc = ["Customer", usrIn]
                    window.close()
                else: 
                    # Let the user know the password was wrong
                    messagebox.showerror(title="Notice", message="Authentication failed", detail="The password you have entered is incorrect. Please try again.")

class window():
    database = None
        
    acc = ["Login", ""]
    # Create the login window as loginRoot using Tk, titled "Login"
    loginRoot = Tk()
    loginRoot.title("Login")

    # String variables
    usrIn = StringVar(loginRoot)
    passIn = StringVar(loginRoot)

    # Create frames
    topFr = Frame(loginRoot) # Frame the top area
    topFr.pack()
    usrFr = Frame(loginRoot) # frame for the username input
    usrFr.pack()
    passFr = Frame(loginRoot) # frame for the password input
    passFr.pack()
    btnFr = Frame(loginRoot) # Frame for the buttons
    btnFr.pack()

    # Explaination labels
    topLbl = Label(topFr, text="Taxi Booking System", font=("Noto Sans", 18, "bold"))
    topLbl.grid(column=0, row=0, columnspan=2)
    caption = Label(topFr, text="Have an account? Sign in here:", font=("Noto Sans", 12, "bold"))
    caption.grid(column=0, row=1, columnspan=2)
    
    # Create labels for username and password entries
    usrLbl = Label(usrFr, text="Username: ")
    usrLbl.grid(column=0, row=2)
    passLbl = Label(passFr, text="Password: ")
    passLbl.grid(column=0, row=3)

    # Create entry boxes for username and password
    usrEntry = Entry(usrFr, textvariable=usrIn)
    usrEntry.grid(column=1, row=2)
    passEntry = Entry(passFr, show="·", textvariable=passIn)
    passEntry.grid(column=1, row=3)

    # Create sign-in button
    loginBtn = Button(btnFr, text="Login", command=lambda: check.readCredentials(window.usrEntry.get(), window.passEntry.get(), window.database))
    loginBtn.grid(column=0, row=4, columnspan=2)
    
    # Let the user register
    regLbl = Label(btnFr, text="Don't have an account?", font=("Noto Sans", 12, "bold"))
    regLbl.grid(column=0, row=5)
    regBtn = Button(btnFr, text="Register", command= lambda: register.newWindow(window.database))
    regBtn.grid(column=0, row=6, columnspan=2)
    
    def newWindow(database):
        # Open the login window
        window.database = database
        window.loginRoot.mainloop()
        return window.acc
    
    def close():
        # Close the login window
        window.loginRoot.destroy()