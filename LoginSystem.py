#imports
from tkinter import *
import sqlite3
import hashlib


def mainScreen():#main menu screen
    global screen
    screen = Tk()
    screen.geometry("300x200")
    screen.title("LoginSystemV2")
    Label(text="Login System", bg="grey", width="70", height="1", font=("Calibri", 13)).pack()
    Label(text = "").pack()
    Button(text = "Login", bg="grey", height = "2", width = "30", command = loginScreen).pack()
    Label(text = "").pack()
    Button(text = "Register", bg="grey", height = "2", width = "30", command = registerScreen).pack()

def loginScreen():
    #global Login variables
    global username_verify
    global password_verify
    global username_entry1
    global password_entry1
    global salt_verifyLog
    #setting variables as string variables
    username_verify = StringVar()
    password_verify = StringVar()
    salt_verifyLog = StringVar()

    Loginscreen = Tk()
    Loginscreen.geometry("300x200")
    Loginscreen.title("Login Page")

    #main format and entry box code
    Label(Loginscreen, text="Please Enter Details Below to Login : ").pack()
    Label(Loginscreen, text="").pack()

    Label(Loginscreen, text="Username * ").pack()
    username_entry1 = Entry(Loginscreen, textvariable=username_verify)
    username_entry1.pack()

    Label(Loginscreen, text = "Password * ").pack()
    password_entry1 = Entry(Loginscreen, textvariable = password_verify, show = "*")
    password_entry1.pack()

    salt_label = Label(Loginscreen, text="Salt * ")
    salt_label.pack()
    salt_entry = Entry(Loginscreen, textvariable=salt_verifyLog, show = "*")
    salt_entry.pack()

    Label(Loginscreen, text = "").pack()

    Button(Loginscreen, text = "Login", width = 10, height = 1, command = login_verify).pack()

def registerScreen():
    # global register variables
    global register_screen
    global password
    global username
    global salt
    global username_entry
    global password_entry
    global salt_entry

    register_screen = Toplevel(screen)
    register_screen.title("Register")
    register_screen.geometry("300x200")

    #setting variables as string variables
    username = StringVar()
    password = StringVar()
    salt = StringVar()

    # main format and entry box code
    Label(register_screen, text="Please enter details below", bg="grey").pack()
    Label(register_screen, text="").pack()

    username_label = Label(register_screen, text="Username * ")
    username_label.pack()
    username_entry = Entry(register_screen, textvariable=username)
    username_entry.pack()

    password_label = Label(register_screen, text="Password * ")
    password_label.pack()
    password_entry = Entry(register_screen, textvariable=password, show='*')
    password_entry.pack()

    salt_label = Label(register_screen, text="Salt * ")
    salt_label.pack()
    salt_entry = Entry(register_screen, textvariable=salt)
    salt_entry.pack()

    Label(register_screen, text="").pack()

    Button(register_screen, text="Register", width=10, height=1, bg="grey", command=register).pack()


def register():
    #gets username and password from entry boxes on register page
    usernameReg = username.get()
    passwordReg = password.get()
    salt_info = salt.get()#gets the salt the user chooses
    salted = (passwordReg + salt_info)#adds salt to password
    hashedRegister = hashlib.sha256(salted.encode()).hexdigest() #hashes salted password with SHA256 and encodes in UTF-8 then turned into hexidecimal

    #connects to database using SQL lite
    connection = sqlite3.connect("users.db")
    c = connection.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS user (Username TEXT, Hashed TEXT, Salt TEXT)')#if tables not in Users database it will make them
    c.execute('INSERT INTO user (Username, Hashed, Salt) VALUES(?,?,?)', (usernameReg, hashedRegister, salted))#adds data entered for user to register to database
    connection.commit()# commits these changes
    connection.close()# closes database


    username_entry.delete(0, END)#deletes content of entry boxes
    password_entry.delete(0, END)
    salt_entry.delete(0, END)


def login_verify():
    usernameLog = username_verify.get()#gets passwords, usernames and salt
    passwordLog = password_verify.get()
    logSalt = salt_verifyLog.get()
    salted = (logSalt + passwordLog)
    LogPassHash = hashlib.sha256(salted.encode()).hexdigest()#hashes salted password with SHA256 and encodes in UTF-8 then turned into hexidecimal
                                                             #this will be used for comparing hash stored in database to ensure correct password match

    # connects to database using SQL lite
    connection = sqlite3.connect("users.db")
    c = connection.cursor()
    c.execute("SELECT * FROM user WHERE Username = '%s' AND Hashed = '%s' " % (usernameLog, LogPassHash))
    print(c.fetchone())

mainScreen()
screen.resizable(False, False)
screen.mainloop()
