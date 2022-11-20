from tkinter import *
from tkinter import messagebox
import ast
import hashlib
import base64
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile
from cryptography.fernet import Fernet

root = Tk()
root.title("Login")
root.geometry('925x500+300+200')
root.configure(bg="#fff")
root.resizable(False, False)

def signin():
    username = user.get()

    # encrypt password using md5 hash
    # reference: https://www.geeksforgeeks.org/md5-hash-python/?ref=lbp
    password = code.get()
    pass2hash = hashlib.md5(password.encode())
    password = pass2hash.hexdigest()

    file = open('datasheet.txt', 'r')
    d = file.read()
    r = ast.literal_eval(d)
    file.close()

    # print(r.keys())
    # print(r.values())

    if username in r.keys() and password == r[username]:
        screen=Toplevel(root)
        root.destroy()
       
###mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
        screen = Tk()
        screen.geometry('925x500+300+200')
        screen.configure(bg='#fff')
        screen.resizable(0,0)
        screen.title("Encode dan Decode Text & File Ujian")

        Label(screen, text ='Amankan Dokumen', font = 'Microsoft 20 bold', fg='black', bg='white').pack()
        Label(screen, text ="Aziz's Copyright 2022", font = 'Microsoft 7 bold', fg='black', bg='white').pack(side =BOTTOM)

        Text = StringVar()
        private_key = StringVar()
        mode = StringVar()
        Result = StringVar()
        # set global variables
        global filepath
        global Key
        global keypath

        def Encode(key,message):
            enc=[]
            for i in range(len(message)):
                key_c = key[i % len(key)]
                enc.append(chr((ord(message[i]) + ord(key_c)) % 256))
            return base64.urlsafe_b64encode("".join(enc).encode()).decode()

        def Decode(key,message):
            dec=[]
            message = base64.urlsafe_b64decode(message).decode()
            for i in range(len(message)):
                key_c = key[i % len(key)]
                dec.append(chr((256 + ord(message[i])- ord(key_c)) % 256))
            return "".join(dec)

        def Mode():
            if(mode.get() == 'e'):
                Result.set(Encode(private_key.get(), Text.get()))
            elif(mode.get() == 'd'):
                Result.set(Decode(private_key.get(), Text.get()))
            else:
                Result.set('Invalid Mode')

        def Exit():
            screen.destroy()

        def Reset():
            Text.set("")
            private_key.set("")
            mode.set("")
            Result.set("")

#######FILE BROWSE ENCODE AND DECODE================================================================================================
        # generates the key for encrypting/decrypting
        def Generate():
            # prompts the user to either select a file to print the key to or create one to do so
            keypath = filedialog.askopenfilename()
            # generates key
            key = Fernet.generate_key()

            # writes the key to a file, but if you don't select a file it gives you an error and stops this function
            try:
                with open(keypath, "wb") as filekey:
                    filekey.write(key)
            except FileNotFoundError:
                messagebox.showerror("Error", "no file was selected, try again")
                return
            messagebox.showinfo( "", "Key generated successfully!")

        # function to encrypt files of your choosing
        def Encrypt():
            messagebox.showinfo( "", "select a key")
            # prompts the user to select a file with a key
            keypath = filedialog.askopenfilename()
            # open key file
            try:
                with open(keypath, "rb") as filekey:
                    key = filekey.read()
            except FileNotFoundError:
                messagebox.showerror("Error", "no file was selected, try again")
                return

            # if the file selected doesn't have a key in it, it stops the function and gives the user an error
            try:
                global fernet
                fernet = Fernet(key)
            except ValueError:
                messagebox.showerror("Error", "This is not a key file, try again")
                return

            messagebox.showinfo( "", "select one or more files to encrypt")
            # prompts the user to select a file to encrypt
            filepath = filedialog.askopenfilenames()
            # loops for each file in the list/array filepath and encrypts each file
            for x in filepath:
                # opens each file in filepath 
                with open(x, "rb") as file:
                    original = file.read()
                
                # encrypts the selected file
                global encrypted
                encrypted = fernet.encrypt(original)
            
                # opening the file in write mode and encrypts the data in it
                with open(x, "wb") as encrypted_file:
                    encrypted_file.write(encrypted)
            # if the filepath is empty then it means no file was selected which means that an error is prompted
            if not filepath:
                messagebox.showerror("Error", "no file was selected, try again")
            else:
                messagebox.showinfo( "", "files encrypted successfully!")
            

        # function to decrypt files of your choosing
        def Decrypt():
            messagebox.showinfo( "", "select a key")
            # prompts the user to select a file with a key
            keypath = filedialog.askopenfilename()
            # open key file
            try:
                with open(keypath, "rb") as filekey:
                    key = filekey.read()
            except FileNotFoundError:
                messagebox.showerror("Error", "no file was selected, try again")
                return

            # if the file selected doesn't have a key in it, it stops the function and gives the user an error
            try:
                global fernet
                fernet = Fernet(key)
            except ValueError:
                messagebox.showerror("Error", "This is not a key file, try again")
                return

            messagebox.showinfo( "", "select one or more files to decrypt")
            # prompts the user to select a file to decrypt
            filepath = filedialog.askopenfilenames()
            # loops for each file in the list/array filepath and decrypts each file
            for x in filepath:
                # if no file is selected the function stops and it gives the user an error
                with open(x, "rb") as enc_file:
                    encrypted = enc_file.read()

                # decrypting the file
                decrypted = fernet.decrypt(encrypted)
                # opening the file in write mode and decrypts the file
                with open(x, "wb") as dec_file:
                    dec_file.write(decrypted)
            # if the filepath is empty then it means no file was selected which means that an error is prompted
            if not filepath:
                messagebox.showerror("Error", "no file was selected, try again")
            else:
                messagebox.showinfo( "", "files decrypted successfully!")

#######END FILE BROWSE ENCODE AND DECODE================================================================================================

        # Add a Label widget
        Label(screen, fg='black', bg='white', text="Browse the Files to Encrypt and Decrypt", font= ('Microsoft YaHei UI Light', 12,'bold'),).place(x= 60,y=280)

        # Create a Button
        # ttk.Button(screen, text="Browse", command=open_file).place(x= 60,y=60)
        Button(screen, font= ('Microsoft YaHei UI Light', 10,'bold'), text = 'Generate'  ,padx =2,bg ='LightGray' ,command = Generate).place(x=60, y = 350)
        Button(screen, font= ('Microsoft YaHei UI Light', 10,'bold'), text = 'Encrypt File'  ,padx =2,bg ='LightGray' ,command = Encrypt).place(x=150, y = 350)
        Button(screen, font= ('Microsoft YaHei UI Light', 10,'bold'), text = 'Decrypt File'  ,padx =2,bg ='LightGray' ,command = Decrypt).place(x=260, y = 350)
        

        img = PhotoImage(file='login.png')
        Label(screen, image=img, bg='white').place(x= 500,y=60)

        Label(screen, font= ('Microsoft YaHei UI Light', 12,'bold'), fg='black', bg='white', text='Catatan Rahasia').place(x= 60,y=60)
        Entry(screen,width=20, font=('Microsoft YaHei UI Light', 10), textvariable = Text, bg = 'ghost white').place(x=290, y = 60)
        Label(screen, font=('Microsoft YaHei UI Light', 12,'bold'), fg='black', bg='white', text ='Key').place(x=60, y = 90)
        Entry(screen,width=20, font=('Microsoft YaHei UI Light', 10), textvariable = private_key , bg ='ghost white').place(x=290, y = 90)
        Label(screen, font=('Microsoft YaHei UI Light', 10,'bold'), fg='black', bg='white', text ='Mode (e-Encode, d-Decode)').place(x=60, y = 120)
        Entry(screen, width=20, font=('Microsoft YaHei UI Light', 10), textvariable = mode , bg= 'ghost white').place(x=290, y = 120)
        Entry(screen, textvariable = Result, bg ='ghost white', width=25).place(x=290, y = 150)
        Button(screen, font=('Microsoft YaHei UI Light', 10,'bold'), text = 'Result'  ,padx =2,bg ='LightGray' ,command = Mode).place(x=60, y = 150)
        Button(screen, font=('Microsoft YaHei UI Light', 10,'bold') ,text ='Reset' ,width =6, command = Reset,bg = 'LimeGreen', padx=2).place(x=60, y = 190)
        Button(screen, font=('Microsoft YaHei UI Light', 10,'bold'),text= 'Exit' , width = 6, command = Exit,bg = 'OrangeRed', padx=2, pady=2).place(x=180, y = 190)
        screen.mainloop()
###mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm

    else:
        messagebox.showerror("Invalid", "Invalid Username or Password")

######+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Sign Up Section
def signup_command():
    window=Toplevel(root)
    window.title("Sign up")
    window.geometry('925x500+300+200')
    window.configure(bg='#fff')
    window.resizable(False, False)

    def signup():
        username = user.get()

        password = code.get()
        pass2hash = hashlib.md5(password.encode())  # encrypt password using md5 hash
        password = pass2hash.hexdigest()

        confirm_password = confirm_code.get()
        confirm2hash = hashlib.md5(confirm_password.encode())  # encrypt confirma password using md5 hash
        confirm_password = confirm2hash.hexdigest()

        if password == confirm_password:
            # jika file ada, akan read file nya, dan memasukkan data
            try:
                file = open('datasheet.txt', 'r+')
                d = file.read()
                r = ast.literal_eval(d)

                dict2 = {username:password}
                r.update(dict2)
                file.truncate(0)
                file.close()

                file = open('datasheet.txt', 'w')
                w = file.write(str(r))

                messagebox.showinfo('Sign up', "Successfully Sign Up")
                window.destroy()

            except:
                file = open('datasheet.txt', 'w')
                pp = str({'b2eg2hev2ev28evg83yg3y73r':'yefgg2ef82fghbhweygwyegf282fg'})
                file.write(pp)
                file.close()
        else:
            messagebox.showerror('Invalid', 'Both Password Should Match')

    def sign():
        window.destroy()
        

    img = PhotoImage(file='register.png')
    Label(window, image=img, bg='white').place(x=50, y=90)

    frame = Frame(window, width=350, height=390, bg='white')
    frame.place(x=480, y=50)

    heading=Label(frame, text='Sign up', fg='#57a1f8', bg='white',font=('Microsoft YaHei UI Light', 23,'bold'))
    heading.place(x=100, y=5)

    ##====================================================
    def on_enter(e):
        user.delete(0, 'end')

    def on_leave(e):
        name=user.get()
        if name=='':
            user.insert(0, 'Username')

    user = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11) )
    user.place(x=30, y=80)
    user.insert(0, 'Username')
    user.bind('<FocusIn>', on_enter)
    user.bind('<FocusOut>', on_leave)

    Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

    ##====================================================
    def on_enter(e):
        code.delete(0, 'end')

    def on_leave(e):
        name=code.get()
        if name=='':
            code.insert(0, 'Password')

    code = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11) )
    code.place(x=30, y=150)
    code.insert(0, 'Password')
    code.bind('<FocusIn>', on_enter)
    code.bind('<FocusOut>', on_leave)

    Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

    ##====================================================
    def on_enter(e):
        confirm_code.delete(0, 'end')

    def on_leave(e):
        name=confirm_code.get()
        if name=='':   
            confirm_code.insert(0, 'Confirm Password')

    confirm_code = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11) )
    confirm_code.place(x=30, y=220)
    confirm_code.insert(0, 'Confirm Password')
    confirm_code.bind('<FocusIn>', on_enter)
    confirm_code.bind('<FocusOut>', on_leave)

    Frame(frame, width=295, height=2, bg='black').place(x=25, y=247)

    ##====================================================
    Button(frame, width=39, pady=7, text='Sign up', bg='#57a1f8', fg='white', border=0, command=signup).place(x=35, y=280)
    label = Label(frame, text="I have an account", fg='black', bg='white', font=('Microsoft YaHei UI Light', 9))
    label.place(x=90, y=340)

    sign_in = Button(frame,width=6,text='Sign in',border=0, bg='white' ,cursor='hand2', fg='#57a1f8', command=sign)
    sign_in.place(x=200,y=340)

    window.mainloop()
######++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    

img = PhotoImage(file='login.png')
Label(root, image=img, bg='white').place(x=50, y=50)

frame = Frame(root, width=350, height=350, bg='white')
frame.place(x=480, y=70)

heading=Label(frame, text='Sign in', fg='#57a1f8', bg='white',font=('Microsoft YaHei UI Light', 23,'bold'))
heading.place(x=100, y=5)

#=====================================
def on_enter(e):
    user.delete(0, 'end')

def on_leave(e):
    name=user.get()
    if name=='':
        user.insert(0, 'Username')

user = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11) )
user.place(x=30, y=80)
user.insert(0, 'Username')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)

Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

#======================================
def on_enter(e):
    code.delete(0, 'end')

def on_leave(e):
    name=code.get()
    if name=='':
        code.insert(0, 'Password')

code = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11) )
code.place(x=30, y=150)
code.insert(0, 'Password')
code.bind('<FocusIn>', on_enter)
code.bind('<FocusOut>', on_leave)

Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

#=======================================
Button(frame, width=39, pady=7, text='Sign in', bg='#57a1f8', fg='white', border=0, command=signin).place(x=35, y=204)
label = Label(frame, text="Don't have an account?", fg='black', bg='white', font=('Microsoft YaHei UI Light', 9))
label.place(x=75, y=270)

sign_up = Button(frame,width=6,text='Sign up',border=0, bg='white' ,cursor='hand2', fg='#57a1f8', command=signup_command)
sign_up.place(x=215,y=270)



root.mainloop()