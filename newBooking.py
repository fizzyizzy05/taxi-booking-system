from tkinter import *
import logging
from tkinter import messagebox
from datetime import datetime

def newWindow(user, database):
    logging.info(f"Creating new booking for {user}")
    
    # New window
    root = Tk()
    root.title(f"New booking for {user}")
    
    # Create frames
    destFr = Frame(root) 
    destFr.pack()
    dtlFrame = Frame(root) 
    dtlFrame.pack()
    timeFr = Frame(root)
    timeFr.pack()
    bookFr = Frame(root)
    bookFr.pack()
    
    # Create labels for headers
    destLbl = Label(destFr, text="Destination Details", font=("Noto Sans", 14, "bold"))
    destLbl.grid(row=0, column=0, columnspan=2)
    dtlLbl = Label(dtlFrame, text="Your Details", font=("Noto Sans", 14, "bold"))
    dtlLbl.grid(row=0, column=0, columnspan=2)
    timeLbl = Label(timeFr, text="Time & Date", font=("Noto Sans", 14, "bold"))
    timeLbl.grid(row=0, column=0, columnspan=4)

    # Create labels for destination
    streetLbl = Label(destFr, text="Street & Number:")
    streetLbl.grid(row=1, column=0)
    cityLbl = Label(destFr, text="City:")
    cityLbl.grid(row=2, column=0)
    postcodeLbl = Label(destFr, text="Postcode:")
    postcodeLbl.grid(row=3, column=0)

    # Set a stringvar as the user's address
    currentPostCode = StringVar(root)
    currentStreet = StringVar(root)
    currentCity = StringVar(root)
    
    # Set the variables for the user's address
    cursor = database.execute(f"SELECT StreetNo, City, Postcode, Owner from Addresses where owner = '{user}'")
    for row in cursor:            
        currentStreet.set(row[0])
        currentCity.set(row[1])
        currentPostCode.set(row[2])
        logging.info(f"Found address {row[0]}: {row[1]}, {row[2]} for user {user}") 

    # Create entries for user details
    streetEtr = Entry(destFr, textvariable=currentStreet)
    streetEtr.grid(row=1, column=1)
    cityEtr = Entry(destFr, textvariable=currentCity)
    cityEtr.grid(row=2, column=1)
    postcodeEtr = Entry(destFr, textvariable=currentPostCode)
    postcodeEtr.grid(row=3, column=1)

    # Create labels for details
    firstnameLbl = Label(dtlFrame, text="First name:")
    firstnameLbl.grid(row=1, column=0)
    surnameLbl = Label(dtlFrame, text="Surname:")
    surnameLbl.grid(row=2, column=0)
    phoneLbl = Label(dtlFrame, text="Phone number:")
    phoneLbl.grid(row=3, column=0)

    # Set a stringvar as the user's details
    currentPhone = StringVar(root)
    currentFirstName = StringVar(root)
    currentSurname = StringVar(root)

    cursor = database.execute(f"SELECT Firstname, Surname, Phone from Users where username = '{user}'")
    for row in cursor:            
        currentFirstName.set(row[0])
        currentSurname.set(row[1])
        currentPhone.set(row[2])
        logging.info(f"Found details for {user}: {row[0]} {row[1]}, {row[2]}") 
    
    # Create entries for user details
    firstnameEtr = Entry(dtlFrame, textvariable=currentFirstName)
    firstnameEtr.grid(row=1, column=1)
    surnameEtr = Entry(dtlFrame, textvariable=currentSurname)
    surnameEtr.grid(row=2, column=1)
    phoneEtr = Entry(dtlFrame, textvariable=currentPhone)
    phoneEtr.grid(row=3, column=1)
    
    # Create labels for time and date
    dayLbl = Label(timeFr, text="Date")
    dayLbl.grid(row=1, column=0)
    timeLbl = Label(timeFr, text="Time:")
    timeLbl.grid(row=2, column=0)
    
    # Dropdown for day
    days = []
    for x in range (32):
        days.append(x)     
    day = StringVar(root)
    dayEtr = OptionMenu(timeFr, day, *days)
    dayEtr.grid(row=1, column=1)
    
    # Dropdown for month
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    month = StringVar(root)
    monthEtr = OptionMenu(timeFr, month, *months)
    monthEtr.grid(row=1, column=2)
    
    # Create entry for year
    yearEtr = Entry(timeFr, width=7)
    yearEtr.grid(row=1, column=3)
    
    # Create entries for time
    hourEtr = Entry(timeFr, width=4)
    hourEtr.grid(row=2, column=1)
    minEtr = Entry(timeFr, width=4)
    minEtr.grid(row=2, column=2)
    
    # Button to save the booking
    saveBtn = Button(bookFr, text="Make booking", command= lambda: saveBooking(database, user, currentStreet.get(), currentCity.get(), currentPostCode.get(), currentFirstName.get(), currentSurname.get(), currentPhone.get(), month.get(), day.get(), yearEtr.get(), hourEtr.get(), minEtr.get()))
    saveBtn.grid(row=0, column=0, columnspan=3)
 
    # Program mainloop
    root.mainloop()
    
def saveBooking(database, user, street, city, postcode, firstName, surname, phone, month, day, year, hour, minute):
    # Strings for address, name, date, and time
    address = f"{street}, {city}, {postcode}"
    name = f"{firstName} {surname}, {phone}"
    date = f"{month}-{day}-{year}"
    time = f"{hour}:{minute}"
    
    if address.strip() == ",," or name.strip() == "," or date.strip() == "--" or time.strip() == "":
        messagebox.showerror(title="Notice", message="Booking failed", detail="One or more inputs was blank. Please fill out the form entirely.")
    else:
        # Make sure the database doesn't use any existing Booking IDs
        cursor = database.execute(f"SELECT BookingID from Bookings")
        id = 0
        for row in cursor:
            id = row[0]
        
        # Save the booking to the database
        database.execute(f"INSERT INTO Bookings (BookingID, owner, Customer, Address, Date, Time) VALUES ('{id + 1}', '{user}', '{name}', '{address}', '{date}', '{time}')")
        database.commit()
        
        # Refresh bookFr in the customer window
        import customer
        customer.window.refresh(database, user)
        
        # Notify the user
        messagebox.showinfo(title="Notice", message="Booking successful", detail="Your booking was created successfully. Stand by for futher information.")