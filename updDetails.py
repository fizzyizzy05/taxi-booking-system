import sqlite3
from tkinter import *
from tkinter import messagebox
import logging

def newWindow(user, database):
    root = Tk()
    root.title("Manage Account")
    
    # Set the frame for modifying the user's entries
    detFr = Frame(root)#
    detFr.pack()
    adrFr = Frame(root)
    adrFr.pack()
    delFr = Frame(root)
    delFr.pack()
    
    # Set a stringvar as the user's details
    currentPhone = StringVar(root)
    currentFirstName = StringVar(root)
    currentSurname = StringVar(root)
    
    # Labels for details
    detLbl = Label(detFr, text="User details:", font=("Noto Sans", 14, "bold"))
    detLbl.grid(row=0, column=0, columnspan=2)
    firstNameLbl = Label(detFr, text="First name:")
    firstNameLbl.grid(row=1, column=0)
    surnameLbl = Label(detFr, text="Last name:")
    surnameLbl.grid(row=2, column=0)
    phoneLbl = Label(detFr, text="Phone number:")
    phoneLbl.grid(row=3, column=0)
    
    # Entries for details
    firstNameEtr = Entry(detFr, text="First name:", textvariable=currentFirstName)
    firstNameEtr.grid(row=1, column=1)
    surnameEtr = Entry(detFr, text="Last name:", textvariable=currentSurname)
    surnameEtr.grid(row=2, column=1)
    phoneEtr = Entry(detFr, text="Phone number:", textvariable=currentPhone)
    phoneEtr.grid(row=3, column=1)
    
    # Set the variables for the user's details
    cursor = database.execute(f"SELECT Firstname, Surname, Phone from Users where username = '{user}'")
    for row in cursor:            
        currentFirstName.set(row[0])
        currentSurname.set(row[1])
        currentPhone.set(row[2])
        logging.info(f"Found details for {user}: {row[0]} {row[1]}, {row[2]}") 
    
    # Button to submit Details
    dtlBtn = Button(detFr, text="Save Details", command= lambda: submitDet(database, currentFirstName.get(), currentSurname.get(), currentPhone.get(), user))
    dtlBtn.grid(row=4, column=0, columnspan=2)
    
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
        
    # Labels for updating address
    adrLbl = Label(adrFr, text="Default address details:", font=("Noto Sans", 14, "bold"))
    adrLbl.grid(row=0, column=0, columnspan=2)
    noLbl = Label(adrFr, text="Street Number & Name:")
    noLbl.grid(row=1, column=0)
    postCode = Label(adrFr, text="Postcode:")
    postCode.grid(row=2, column=0)
    city = Label(adrFr, text="City:")
    city.grid(row=3, column=0)
    
    # Entries for updating address
    noEtr = Entry(adrFr, textvariable=currentStreet, text=currentStreet)
    noEtr.grid(row=1, column=1)
    postCodeEtr = Entry(adrFr, textvariable=currentPostCode, text=currentPostCode)
    postCodeEtr.grid(row=2, column=1)
    cityEtr = Entry(adrFr, textvariable=currentCity, text=currentCity)
    cityEtr.grid(row=3, column=1)
    
    adrBtn = Button(adrFr, text="Save Address", command= lambda: submitAdr(database, currentStreet.get(), currentPostCode.get(), currentCity.get(), user))
    adrBtn.grid(row=4, column=0, columnspan=2)
    
    # Labels for deleting the user's account
    delLbl1 = Label(delFr, text="Delete Account", font=("Noto Sans", 14, "bold"))
    delLbl1.grid(row=0, column=0, columnspan=2)
    delLbl2 = Label(delFr, text="Delete this account, including historical bookings and address info. Note that this is irreversible. Please enter your password if you wish to do so:", wraplength=350)
    delLbl2.grid(row=1, column=0, columnspan=2)
    delLbl3 = Label(delFr, text="Password:")
    delLbl3.grid(row=2, column=0)
    delPassEtr = Entry(delFr)
    delPassEtr.grid(row=2, column=1)
    delBtn = Button(delFr, text="Delete Account", fg='#F00', command=lambda: deleteAcc(database, user, delPassEtr.get(), root))
    delBtn.grid(row=3, column=0, columnspan=2)
    
    root.mainloop()

def submitDet(database, first, last, phone, user): 
    # When the user presses submit, update the details of the owner
    database.execute(f"UPDATE Users SET Firstname = '{first}' where username = '{user}'")
    database.execute(f"UPDATE Users SET Surname = '{last}'where username = '{user}'")
    database.execute(f"UPDATE Users SET Phone = '{phone}' where username = '{user}'")
    database.commit()
    logging.info(f"Updated details for {user}: {first} {last}, {phone}")
    messagebox.showinfo(title="Notice", message="Details updated", detail=f"Updated the details for {user}")
    
def submitAdr(database, no, postCode, city, user): 
    # When the user presses submit, update the details of the owner
    database.execute(f"UPDATE Addresses SET City = '{city}' where Owner = '{user}'")
    database.execute(f"UPDATE Addresses SET Postcode = '{postCode}'where Owner = '{user}'")
    database.execute(f"UPDATE Addresses SET StreetNo = '{no}' where Owner = '{user}'")
    database.commit()
    logging.info(f"Updated address for {user}: {no}, {city}, {postCode}")
    messagebox.showinfo(title="Notice", message="Details updated", detail=f"Updated the address for {user}")
    
def deleteAcc(database, user, passIn, root):
    if passIn == "":
        messagebox.showerror(title="Notice", message="Authentication failed", detail="You need to enter a password to delete your account.")
    else:
        cursor = database.execute(f"SELECT password from Users where username = '{user}'")
        pw = ""
        
        for row in cursor:
            pw = row[0]
            
        if pw == passIn:
            confirm = messagebox.askyesno(title="Delete account?", message="Are you sure you want to delete this account?", detail="This will delete all of your data from this system, including account details, bookings and addresses irreversibly. Are you really sure you want to proceed?")
            if confirm:
                database.execute(f"DELETE from Users where username = '{user}'")
                database.execute(f"DELETE from Bookings where owner = '{user}'")
                database.execute(f"DELETE from Addresses where owner = '{user}'")
                database.commit()
                logging.info(f"Deleted account for {user}")
                import customer
                customer.window.close()
                root.destroy()
                messagebox.showinfo(title="Notice", message="Account deleted", detail=f"Account {user} and all related information has been deleted from the database. The booking system will now exit.")
        else:
            print("Wrong password!")