from tkinter import * # Import all components from 'Tkinter'
from tkinter import messagebox
import newBooking
import updDetails
import sqlite3

class window():    
    user = "" # blank user string, used later in the code
    # Create the window
    root = Tk() 
    
    # Create frames
    topFr = Frame(root)
    topFr.pack()
    bookFr = Frame(root, padx=4, pady=4)
    bookFr.pack()
    delFr = Frame(root)
    delFr.pack()
                
    def newWindow(database, user):
        # Button for creating account management
        accBtn = Button(window.topFr, text="My Account", command=lambda: updDetails.newWindow(window.user, database))
        accBtn.grid(row=0, column=2)
        
        # Create labels for each booking
        cursor = database.execute(f"SELECT BookingID, Address, Time, Date from Bookings where owner = '{user}'")
        
        # Headings for the booking table
        Label(window.bookFr, text=f"ID:").grid(row=0, column=0)
        Label(window.bookFr, text="Address").grid(row=0, column=1)
        Label(window.bookFr, text="Time").grid(row=0, column=2)
        Label(window.bookFr, text="Date").grid(row=0, column=3)
        
        for row in cursor:
            Label(window.bookFr, text=row[0]).grid(row=row[0], column=0)
            Label(window.bookFr, text=row[1]).grid(row=row[0], column=1)
            Label(window.bookFr, text=row[2]).grid(row=row[0], column=2)
            Label(window.bookFr, text=row[3]).grid(row=row[0], column=3)
                    
        # Button for creating a new booking
        bookBtn = Button(window.topFr, text="New Booking", command=lambda: newBooking.newWindow(window.user, database))
        bookBtn.grid(row=0, column=3)

        # Label showing the user who they are currently signed in as
        window.user = user
        userVar = StringVar(window.topFr, value=f"Signed in as {user}")
        usrLbl = Label(window.topFr, textvariable=userVar) 
        usrLbl.grid(row=0, column=0)
        
        # Header label for deleting booking
        delLbl1 = Label(window.delFr, text="Delete booking", font=("Noto Sans", 12, "bold"))
        delLbl1.grid(row=0, column=0, columnspan=3)
        # Ask the user which booking to delete by ID
        delLbl2 = Label(window.delFr, text="Enter ID:")
        delLbl2.grid(row=1, column=0)
        # Entry for deleting booking
        delEtr = Entry(window.delFr)
        delEtr.grid(row=1, column=2)
        # Button for deleting booking
        delBtn = Button(window.delFr, command = lambda: window.delete(delEtr.get(), database, user))
        delBtn.grid(row=1, column=3)
        
        # Open new window
        window.root.title(f"Home page for {user}")
        window.root.update()
        window.root.mainloop() 

    def close():
        window.root.destroy()
        
    def delete(id, database, user):
        # Delete the booking from the database
        database.execute(f"DELETE from Bookings where BookingID = '{id}'")
        database.commit()
        window.refresh(database, user)
    
    def refresh(database, user):
        # Clear bookFr of widgets
        for widget in window.bookFr.winfo_children():
            widget.destroy()
        
        # Search through the bookings table
        cursor = database.execute(f"SELECT BookingID, Address, Time, Date from Bookings where owner = '{user}'")
        
        # Headings for the booking table
        Label(window.bookFr, text=f"ID:").grid(row=0, column=0)
        Label(window.bookFr, text="Address").grid(row=0, column=1)
        Label(window.bookFr, text="Time").grid(row=0, column=2)
        Label(window.bookFr, text="Date").grid(row=0, column=3)
        
        # Recreate labels for each booking
        for row in cursor:
            Label(window.bookFr, text=row[0]).grid(row=row[0], column=0)
            Label(window.bookFr, text=row[1]).grid(row=row[0], column=1)
            Label(window.bookFr, text=row[2]).grid(row=row[0], column=2)
            Label(window.bookFr, text=row[3]).grid(row=row[0], column=3)