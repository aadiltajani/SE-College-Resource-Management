import tkinter as tk
from PIL import Image, ImageTk
import hashlib
import pandas as pd


def logmain():
    global log
    log = tk.Toplevel(root)
    log.geometry("350x150")
    log.title('Login')

    global name_entry
    global passw_entry
    global name_var
    global passw_var

    name_var = tk.StringVar()
    passw_var = tk.StringVar()

    name_label = tk.Label(log, text='Username', font=('calibre', 10, 'bold'))
    name_entry = tk.Entry(log, textvariable=name_var, font=('calibre', 10, 'normal'))

    passw_label = tk.Label(log, text='Password', font=('calibre', 10, 'bold'))
    passw_entry = tk.Entry(log, textvariable=passw_var, font=('calibre', 10, 'normal'), show='*')

    sub_btn = tk.Button(log, text='Submit', command=submitlogin)

    exit_btn = tk.Button(log, text='Exit', command=destroyall)

    name_label.grid(row=0, column=1)
    name_entry.grid(row=0, column=2)
    passw_label.grid(row=1, column=1)
    passw_entry.grid(row=1, column=2)
    sub_btn.grid(row=2, column=2)
    exit_btn.grid(row=4, column=2)
    log.mainloop()


def destroyall():
    exit(0)


def deletelog():
    global loggedin
    loggedin = True
    log.destroy()
    root.destroy()


def submitlogin():
    user_id = name_entry.get()
    password = passw_entry.get()
    name_entry.delete(0, tk.END)
    passw_entry.delete(0, tk.END)
    if len(user_id) == 0 or len(password) == 0:
        inv = tk.Label(log, text='Invalid details !', fg='red')
        inv.grid(row=5, column=2)
        return
    pwd_hash = hashlib.sha256(password.encode()).hexdigest()
    global successful
    global logtype
    if user_id == 'admin':
        try:
            data = ''
            with open('admin.txt', 'r') as f:
                data = f.read()
            if data.strip() == pwd_hash:
                successful = tk.Toplevel(log)
                successful.title('Successful')
                successful.geometry('200x80')
                suc = tk.Label(successful, text='Login Successful', fg='green')
                suc.grid(row=1, column=3)
                okb = tk.Button(successful, text='ok', command=deletelog)
                okb.grid(row=2, column=3)
                logtype = 'admin'
                return True
            else:
                suc = tk.Label(log, text='Login Unsuccessful', fg='red')
                suc.grid(row=5, column=2)
                return False

        except FileNotFoundError:
            suc = tk.Label(log, text='User not found !', fg='red')
            suc.grid(row=5, column=2)
            return False
    else:
        try:
            li = []
            with open('credentials.txt', 'r') as f:
                li = f.readlines()
            for i in li:
                if i.strip().split(',')[0] == user_id:
                    if i.strip().split(',')[1] == pwd_hash:
                        name_var.set("")
                        passw_var.set("")
                        successful = tk.Toplevel(log)
                        successful.title('Successful')
                        successful.geometry('200x80')
                        tk.Label(successful, text='Login Successful', fg='green').pack()
                        tk.Button(successful, text='ok', command=deletelog).pack()
                        logtype = 'student'
                        return True
                    else:
                        name_var.set("")
                        passw_var.set("")
                        suc = tk.Label(log, text='Login Unsuccessful', fg='red')
                        suc.grid(row=5, column=2)
                        return False
            name_var.set("")
            passw_var.set("")
            suc = tk.Label(log, text='User not found !', fg='red')
            suc.grid(row=5, column=2)
            return False

        except FileNotFoundError:
            name_var.set("")
            passw_var.set("")
            suc = tk.Label(log, text='User not found !', fg='red')
            suc.grid(row=5, column=2)
            return False


def signup():
    global sg
    sg = tk.Toplevel(root)
    sg.geometry("350x150")
    sg.title('Register')

    global name_entry
    global passw_entry
    global name_var
    global passw_var

    name_var = tk.StringVar()
    passw_var = tk.StringVar()

    name_label = tk.Label(sg, text='Username', font=('calibre', 10, 'bold'))
    name_entry = tk.Entry(sg, textvariable=name_var, font=('calibre', 10, 'normal'))

    passw_label = tk.Label(sg, text='Password', font=('calibre', 10, 'bold'))
    passw_entry = tk.Entry(sg, textvariable=passw_var, font=('calibre', 10, 'normal'), show='*')

    sub_btn = tk.Button(sg, text='Submit', command=submitsignup)

    exit_btn = tk.Button(sg, text='Exit', command=destroyall)

    name_label.grid(row=0, column=1)
    name_entry.grid(row=0, column=2)
    passw_label.grid(row=1, column=1)
    passw_entry.grid(row=1, column=2)
    sub_btn.grid(row=2, column=2)
    exit_btn.grid(row=4, column=2)
    sg.mainloop()


def submitsignup():
    user_id = name_entry.get()
    password = passw_entry.get()
    if len(user_id) == 0 or len(password) == 0:
        inv = tk.Label(sg, text='Invalid details !', fg='red')
        inv.grid(row=5, column=2)
        return
    name_entry.delete(0, tk.END)
    passw_entry.delete(0, tk.END)
    pwd_hash = hashlib.sha256(password.encode()).hexdigest()
    flag = 1
    global logtype
    while True:
        global successfulsg
        try:
            li = []
            with open('credentials.txt', 'r') as f:
                li = f.readlines()
            for l in li:
                if user_id == l.strip().split(',')[0]:
                    flag = 0
                    break
            if flag:
                with open('credentials.txt', 'a') as f:
                    f.writelines('{},{}\n'.format(user_id, pwd_hash))
                successfulsg = tk.Toplevel(sg)
                successfulsg.title('Successful')
                successfulsg.geometry('200x80')
                suc = tk.Label(successfulsg, text='Registration Successful', fg='green')
                suc.grid(row=1, column=3)
                okb = tk.Button(successfulsg, text='ok', command=deletesg)
                okb.grid(row=2, column=3)
                logtype = 'student'
                return True
            else:
                suc = tk.Label(sg, text='This user_id is taken try another !', fg='red')
                suc.grid(row=5, column=2)
                return False

        except FileNotFoundError:
            with open('credentials.txt', 'w') as f:
                f.writelines('{},{}\n'.format(user_id, pwd_hash))
            successfulsg = tk.Toplevel(sg)
            successfulsg.title('Successful')
            successfulsg.geometry('200x80')
            suc = tk.Label(successfulsg, text='Registration Successful', fg='green')
            suc.grid(row=1, column=3)
            okb = tk.Button(successfulsg, text='ok', command=deletesg)
            okb.grid(row=2, column=3)
            return True

        except:
            suc = tk.Label(sg, text='Registration Unsuccessfull', fg='red')
            suc.grid(row=5, column=2)
            return False


def deletesg():
    global loggedin
    loggedin = True
    sg.destroy()
    root.destroy()


def viewtt():
    img = Image.open('time_table.jpg')
    img.show()


def att():
    global at
    at = tk.Toplevel(st)
    at.title('Attendance')
    at.geometry('500x300')

    global en_entry
    global en_var

    en_var = tk.StringVar()

    enlab = tk.Label(at, text='Enter your Enrollment Number:', font=('Helvetica', 20))
    en_entry = tk.Entry(at, textvariable=en_var, font=('calibre', 10, 'normal'))
    sub = tk.Button(at, text='Submit', command=checkat)
    nl = tk.Label(at, text='\n\n')
    delb = tk.Button(at, text='<- Go Back', command=deleteat)

    enlab.pack()
    en_entry.pack()
    sub.pack()
    delb.pack()
    nl.pack()


def checkat():
    en = en_entry.get()
    df = pd.read_csv('attendance.csv')
    roll = int(en)
    try:
        attendance = str(df[df['enrollment'] == roll].attendance.values[0])
        string = 'Attendance for enrollment number {} is {}%'.format(en, attendance)
        tk.Label(at, text=string, font=('Helvetica', 12)).pack()
    except:
        tk.Label(at, text='Student Not Found !', fg='red', font=('Helvetica', 12)).pack()


def deleteat():
    at.destroy()


def givefeed():
    global feed
    feed = tk.Toplevel(st)
    feed.title('Give Feedback')
    feed.geometry('500x300')
    tk.Label(feed, text="You can leave you feedbacks regarding the institute here.\nNOTE:- All the details will "
                        "remain anonymous\n", font=('Helvetica', 10), fg='blue').pack()
    global fst
    global fst_entry

    fst = tk.StringVar()

    fst_entry = tk.Entry(feed, textvariable=fst, font=('calibre', 10, 'normal'))
    fst_entry.pack()
    tk.Button(feed, text='Submit Feedback', command=feedsub).pack()
    tk.Button(feed, text='<- Go Back', command=deletefeed).pack()


def feedsub():
    feedback_str = fst_entry.get()
    with open("feedback.txt", 'a') as f:
        f.write(feedback_str + '\n')
    fst_entry.delete(0, tk.END)
    tk.Label(feed, text="Your response has been recorded...Thank You!", fg='green').pack()


def deletefeed():
    feed.destroy()


logtype = None
loggedin = False
while not loggedin:
    global root
    root = tk.Tk()
    root.title('College Resource Management')
    root.geometry('500x400')
    img = Image.open('scet.png')
    img = img.resize((380, 60), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(img)
    w = tk.Label(root, image=photo)
    w.photo = photo
    w.pack()
    tk.Label(root, text="Welcome, please login/register to continue", font=("Helvetica", 16), pady=20).pack()
    frame = tk.Frame(root)
    frame.pack()

    button1 = tk.Button(frame, text="Login", fg="blue", padx=9, pady=4, font=("Helvetica", 10), command=logmain)
    button1.pack(side=tk.TOP)
    tk.Label(frame, text="").pack()
    button2 = tk.Button(frame, text="Register", fg='blue', pady=4, font=("Helvetica", 10), command=signup)
    button2.pack(side=tk.TOP)

    tk.Label(frame, text="\n\n").pack()
    exit_btn = tk.Button(frame, text='Exit', command=destroyall)
    exit_btn.pack(side=tk.BOTTOM)

    root.mainloop()

while loggedin:
    if logtype == 'admin':
        admin = tk.Tk()
        admin.title('Admin Page')
        admin.geometry('500x400')
        tk.Label(admin, text='Welcome Admin\n', font=('Helvetica', 25)).pack()
        feedback = ''
        s = ''
        try:
            with open('feedback.txt', 'r') as f:
                feedback = f.readlines()
            feedback.reverse()
            for i in range(len(feedback)):
                s = s + str(i + 1) + ') ' + feedback[i] + '\n'
            tk.Label(admin, text='Here are the feedbacks received:', font=('Helvetica', 10)).pack()
            tk.Label(admin, text=s, font=('Helvetica', 10)).pack()
        except:
            tk.Label(admin, text='No feedbacks present !', font=('Helvetica', 10)).pack()
        finally:
            tk.Button(admin, text='Exit', command=destroyall).pack()
            admin.mainloop()

    elif logtype == 'student':
        global st
        st = tk.Tk()
        st.title('Admin Page')
        st.geometry('500x400')
        tk.Label(st, text='Welcome Student\n', font=('Helvetica', 25)).pack()
        tk.Button(st, text='View Time Table', font=('Helvetica', 10), command=viewtt).pack()
        tk.Button(st, text='View Attendance', font=('Helvetica', 10), command=att).pack()
        tk.Button(st, text='Submit Feedback', font=('Helvetica', 10), command=givefeed).pack()
        tk.Label(st, text='\n').pack()
        tk.Button(st, text='Exit', command=destroyall).pack()
        st.mainloop()

    else:
        exit(0)
