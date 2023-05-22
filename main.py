import tkinter as tk
from tkinter import *
import tkinter.messagebox
import sqlite3

root = Tk()
root.title("Bank of Kaushik and Rahul")
root.geometry('360x360')

conn = sqlite3.connect('bank_accounts.db')
c= conn.cursor()

global registerScreen
global servicesScreen
global loginScreen

c.execute("""CREATE TABLE IF NOT EXISTS accounts (
    name text,
    account_no integer,
    pin integer,
    initAmt integer
    )""")

def regSubmit(nname, ppin, iinitAmt):
    if nname != "" and ppin != "" and str.isdigit(ppin) and iinitAmt != "" and str.isdigit(iinitAmt):
        c = conn.cursor()
        c.execute("SELECT MAX(account_no) FROM accounts")
        maxAccountno = c.fetchall()
        conn.commit()
        daccntno = maxAccountno[0][0] + 1
        c.execute("INSERT INTO accounts VALUES (:dname, :daccntno, :dpin, :dinitAmt)",
              {
                  'dname':nname,
                  'daccntno':daccntno,
                  'dpin':int(ppin),
                  'dinitAmt':int(iinitAmt)
              })
        conn.commit()
        tk.messagebox.showinfo("Registration Succesful", "Your account number is: {} \nYou can now close this window.".format(daccntno), parent=registerScreen)
    else:
        tk.messagebox.showerror("Registration Failed", "Invalid entries! Try again.", parent=registerScreen)
        

def displayRegisterScreen():
    global registerScreen
    registerScreen = Toplevel(root) 
    registerScreen.title("Registration Window")
    registerScreen.geometry('360x360')
    
    nameLabel = tk.Label(registerScreen, text="Name")
    nameLabel.grid(row=0, column=0, padx=10, pady=(30,20))
    
    nameEntry = tk.Entry(registerScreen)
    nameEntry.grid(row=0, column=1, padx=20, pady=(30,20))
    
    pinLabel = tk.Label(registerScreen, text="PIN")
    pinLabel.grid(row=1, column=0, padx=10, pady=20)
    
    pinEntry = tk.Entry(registerScreen, show="*")
    pinEntry.grid(row=1, column=1, padx=20, pady=20)
    
    initialDepositLabel = tk.Label(registerScreen, text="Initial deposit (₹)")
    initialDepositLabel.grid(row=2, column=0, padx=10, pady=20)
    
    initialDepositEntry = tk.Entry(registerScreen)
    initialDepositEntry.grid(row=2, column=1, padx=20, pady=20)
    
    def clearAll():
        nameEntry.delete(0, END)
        pinEntry.delete(0, END)
        initialDepositEntry.delete(0, END)
    
    regSubmitButton = tk.Button(registerScreen, text="Submit", command=lambda:[regSubmit(nameEntry.get(), pinEntry.get(), initialDepositEntry.get()), clearAll()])
    regSubmitButton.grid(row=3, column=1, pady=30)
    
    
def loginSubmit(name, accntno, pin):
    if name != "" and accntno != "" and str.isdigit(accntno) and pin != "" and str.isdigit(pin):
        c = conn.cursor()
        c.execute("SELECT * FROM accounts WHERE account_no=:accntno",
              {
                  'accntno':int(accntno)
              })
        account = c.fetchall()
        try:
            if name==account[0][0] and int(pin)==account[0][2]:
                displayServicesScreen(accntno)
            else:
                tk.messagebox.showerror("Login failed", "Invalid Credentials!", parent=loginScreen)
        except:
            tk.messagebox.showerror("Login failed", "Invalid Credentials!", parent=loginScreen)
    else:
        tk.messagebox.showerror("Login failed", "Invalid Credentials!", parent=loginScreen)
    

def displayLoginScreen():
    global loginScreen
    loginScreen = Toplevel(root) 
    loginScreen.title("Login Window")
    loginScreen.geometry('360x360')
    
    nameLabel = tk.Label(loginScreen, text="Name")
    nameLabel.grid(row=0, column=0, padx=10, pady=(30,20))
    
    nameEntry = tk.Entry(loginScreen)
    nameEntry.grid(row=0, column=1, padx=20, pady=(30,20))
    
    accntnoLabel = tk.Label(loginScreen, text="Account No")
    accntnoLabel.grid(row=1, column=0, padx=10, pady=(20,20))
    
    accntnoEntry = tk.Entry(loginScreen)
    accntnoEntry.grid(row=1, column=1, padx=20, pady=(30,20))
    
    pinLabel = tk.Label(loginScreen, text="PIN")
    pinLabel.grid(row=2, column=0, padx=10, pady=20)
    
    pinEntry = tk.Entry(loginScreen, show="*")
    pinEntry.grid(row=2, column=1, padx=20, pady=20)    
    
    def clearAll():
        nameEntry.delete(0, END)
        accntnoEntry.delete(0, END)
        pinEntry.delete(0, END)
    
    c = conn.cursor()
    c.execute("SELECT * FROM accounts")
    accountsData = c.fetchall()
        
    loginSubmitButton = tk.Button(loginScreen, text="Submit", command=lambda:[loginSubmit(nameEntry.get(), accntnoEntry.get(), pinEntry.get()), clearAll()])
    loginSubmitButton.grid(row=3, column=1, padx=(20,25), pady=30)    
    
def deposit(accntno, amount):
    if accntno != "" and amount != "" and str.isdigit(amount):
        c = conn.cursor()
        c.execute("UPDATE accounts SET initAmt=(initAmt + :amount) WHERE account_no=:accntno",
              {
                  'accntno':accntno,
                  'amount':int(amount)
              })
        c.execute("SELECT initAmt FROM accounts WHERE account_no=:accntno",
                  {
                      'accntno':accntno
                  })
        bal = c.fetchall()
        bal = bal[0][0]
        conn.commit()
        tk.messagebox.showinfo("Success", "You have deposited ₹ {}\n Updated balance: ₹ {}".format(amount, bal), parent=servicesScreen)
    else:
        tk.messagebox.showerror("Error", "Invalid amount entered!", parent=servicesScreen)
        
def withdraw(accntno, amount):
    if accntno != "" and amount != "" and str.isdigit(amount):
        c = conn.cursor()
        c.execute("SELECT initAmt FROM accounts WHERE account_no=:accntno",
                  {
                      'accntno':accntno
                  })
        bal = c.fetchall()
        bal = bal[0][0]        
        conn.commit()
        if int(amount) > bal:
            tk.messagebox.showerror("Error", "Insufficient funds!", parent=servicesScreen)
        else:
            if int(amount)<10:
                tk.messagebox.showerror("Error", "Minimum withdrawal amount is ₹ 10!", parent=servicesScreen)
                return
            else:
                c.execute("UPDATE accounts SET initAmt=(initAmt - :amount) WHERE account_no=:accntno",
                        {
                            'accntno':accntno,
                            'amount':int(amount)
                        })
                c.execute("SELECT initAmt FROM accounts WHERE account_no=:accntno",
                        {
                            'accntno':accntno
                        })
                bal = c.fetchall()
                bal = bal[0][0]        
                conn.commit()
                tk.messagebox.showinfo("Success", "You have withdrawn ₹ {}\n Updated balance: ₹ {}".format(amount, bal), parent=servicesScreen)
    else:
        tk.messagebox.showerror("Error", "Invalid amount entered!", parent=servicesScreen)
        
def checkBalance(accntno):
    c = conn.cursor()
    c.execute("SELECT initAmt FROM accounts WHERE account_no=:accntno",
              {
                  'accntno':accntno
              })
    bal = c.fetchall()
    tk.messagebox.showinfo("Balance", "Your account balance is: ₹ {}".format(bal[0][0]), parent=servicesScreen) 

    
def displayServicesScreen(accntno):
    global servicesScreen
    c = conn.cursor()
    c.execute("SELECT name FROM accounts WHERE account_no = :accntno",
              {
                  'accntno':int(accntno)
              })
    name = c.fetchall()
    conn.commit()
    servicesScreen = Toplevel(root)
    servicesScreen.title("Welcome {}".format(name[0][0]))
    servicesScreen.geometry('360x360')
    
    def clearDeposit():
        depositEntry.delete(0, END)
        
    def clearWithdraw():
        withdrawEntry.delete(0, END)
    
    depositLabel = tk.Label(servicesScreen, text="Deposit (₹)")
    depositLabel.grid(row=0, column=0, padx=10, pady=(30,20))
    
    depositEntry = tk.Entry(servicesScreen)
    depositEntry.grid(row=0, column=1, padx=20, pady=(30,20))
    
    depositButton = tk.Button(servicesScreen, text="Deposit", command=lambda:[deposit(accntno, depositEntry.get()), clearDeposit()])
    depositButton.grid(row=1, column=1, padx=(20,25), pady=10)
    
    withdrawLabel = tk.Label(servicesScreen, text="Withdraw (₹)")
    withdrawLabel.grid(row=2, column=0, padx=10, pady=(30,20))
    
    withdrawEntry = tk.Entry(servicesScreen)
    withdrawEntry.grid(row=2, column=1, padx=20, pady=(30,20))
    
    withdrawButton = tk.Button(servicesScreen, text="Withdraw", command=lambda:[withdraw(accntno, withdrawEntry.get()), clearWithdraw()])
    withdrawButton.grid(row=3, column=1, padx=(20,25), pady=10)    
    
    balanceButton = tk.Button(servicesScreen, text="Check Balance", command=lambda:checkBalance(accntno))
    balanceButton.grid(row=4, column=1, padx=(20,25), pady=20)
    
                       
       
loginLabel = tk.Label(root, text="Login using your existing netbanking account:")
loginLabel.grid(row=0, column=0, pady=20)
loginButton = tk.Button(root, text="Log in", command=displayLoginScreen)
loginButton.grid(row=1, column=0, padx=140, pady=(0,40))

registerLabel = tk.Label(root, text="Or register for a new account:")
registerLabel.grid(row=2, column=0, pady=20)
registerButton = tk.Button(root, text="Register", command=displayRegisterScreen)
registerButton.grid(row=3, column=0, padx=140, pady=(0,20))

root.mainloop()
