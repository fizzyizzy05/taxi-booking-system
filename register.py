from tkinter import * # Import all components from 'Tkinter'
from tkinter import messagebox

class check():
    def saveCredentials(database, usrIn, passIn, firstNameIn, surnameIn, phoneIn, root):
        
        # Check that the user has put something in
        if usrIn == "":
            messagebox.showerror(title="Notice", message="Failed to create account", detail="No username was provided.")
        elif passIn == "":
            messagebox.showerror(title="Notice", message="Failed to create account", detail="No password was provided.")
        else:
            cursor = database.execute(f"SELECT username from Users where username = '{usrIn}'")

            # Check there isn't already an account with the inserted username
            if len(cursor.fetchall()) == 0:
                # Create the account, if it doesn't cause any collisions
                database.execute(f"INSERT INTO Users (username, password) VALUES ('{usrIn}', '{passIn}')")
                database.execute(f"INSERT INTO Addresses (owner) VALUES ('{usrIn}')")
                database.commit()
                
                if firstNameIn != "":
                    database.execute(f"UPDATE Users SET Firstname = '{firstNameIn}' where username = '{usrIn}'")
                    database.commit()
                    
                if surnameIn != "":
                    database.execute(f"UPDATE Users SET Surname = '{surnameIn}' where username = '{usrIn}'")
                    database.commit()

                if phoneIn != "":
                    database.execute(f"UPDATE Users SET Phone = '{phoneIn}' where username = '{usrIn}'")
                    database.commit()
                    
                messagebox.showinfo(title="Notice", message="Account created", detail=f"Account {usrIn} has been successfully created.")
                root.destroy()
            else:
                # Tell the user they can't use that username, an account already exists with it
                messagebox.showerror(title="Notice", message="Failed to create account", detail=f"There is already a user with the username {usrIn}. Please try again with a different username.")

def newWindow(database):
    # Create a new window called regRoot titled "Register"
    regRoot = Tk()
    regRoot.title("Register")
    
    # Create two frames
    usrFr2 = Frame(regRoot) # frame for the username input
    usrFr2.pack()
    detFr = Frame(regRoot)
    detFr.pack()
    btnFr2 = Frame(regRoot)
    btnFr2.pack()
   
    # Create labels for headers
    topLbl1 = Label(usrFr2, text="Signin details:", font=("Noto Sans", 14, "bold"))
    topLbl1.grid(row=0, column=0, columnspan=2)
    topLbl2 = Label(detFr, text="Account details:", font=("Noto Sans", 14, "bold"))
    topLbl2.grid(row=3, column=0, columnspan=2)
    
    # Create labels for signin details:
    usrLbl2 = Label(usrFr2, text="Username: ")
    usrLbl2.grid(column=0, row=1)
    passLbl2 = Label(usrFr2, text="Password: ")
    passLbl2.grid(column=0, row=2)
    
    # Create labels for account details:
    firstNameLbl = Label(detFr, text="First name:")
    firstNameLbl.grid(column=0, row=4)
    surnameLbl = Label(detFr, text="Last name:")
    surnameLbl.grid(column=0, row=5)
    phoneLbl = Label(detFr, text="Phone Number:")
    phoneLbl.grid(column=0, row=6)

    # Entry boxes for sign in details:
    usrEntry2 = Entry(usrFr2)
    usrEntry2.grid(column=1, row=1)
    passEntry2 = Entry(usrFr2, show="·")
    passEntry2.grid(column=1, row=2)
    
    # Entry boxes for account details
    firstNameEtr = Entry(detFr)
    firstNameEtr.grid(column=1, row=4)
    surnameEtr = Entry(detFr)
    surnameEtr.grid(column=1, row=5)
    phoneEtr = Entry(detFr)
    phoneEtr.grid(column=1, row=6)

    # Create sign-up button
    loginBtn2 = Button(btnFr2, text="Create Account", command=lambda: check.saveCredentials(database, usrEntry2.get(), passEntry2.get(), firstNameEtr.get(), surnameEtr.get(), phoneEtr.get(), regRoot))
    loginBtn2.grid(column=0, row=7, columnspan=2)
        
    regRoot.mainloop()

