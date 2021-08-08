from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter.messagebox import *
from sqlite3 import *
import socket
import requests
import bs4
import matplotlib.pyplot as plt

root = Tk()
root.title("Student Management System")
root.geometry("500x600+700+200")
root.configure(bg="skyblue")
root.iconbitmap("sms.ico")

#Funcions
def f1():
	root.withdraw()
	adst.deiconify()
	entAddRno.focus()


def f2():
	adst.withdraw()
	root.deiconify()


##Add Function
def f3():
        con = None
        try:
                con = connect("sms.db")
                print("connected")
                rno = entAddRno.get()
                name = entAddName.get()
                marks = entAddMarks.get()
                if entAddRno.get()=="" or entAddName.get()=="" or entAddMarks.get()=="":
                        messagebox.showerror("No Entry", "All the fields are compulsary!")
                elif not name.isalpha():
                        messagebox.showerror("Invalid Name Entry", "Please enter valid name!")
                elif len(name)<2:
                        messagebox.showerror("Invalid Name Entry", "Entered Name is too short!")
                elif int(rno)<0:
                        messagebox.showerror("Invalid Entry", "Rno cannot be Negative")
                elif float(marks)<0 or float(marks)>100:
                        messagebox.showerror("Invalid Marks Entry", "Please enter valid marks!")
                else:
                        cursor = con.cursor()
                        sql = "insert into student values('%d', '%s', '%f')"
                        args = (int(rno), name, float(marks))
                        cursor.execute(sql % args)
                        con.commit()
                        messagebox.showinfo("Success", "Record Inserted!")
                        entAddRno.delete(0, END)
                        entAddName.delete(0, END)
                        entAddMarks.delete(0, END)
                        entAddRno.focus()
        except ValueError:
                messagebox.showerror("Invalid Entry", "Rno and Marks should not be String")
        except IntegrityError:
                messagebox.showerror("Duplicate Rno", "Rno already exists")
        except DatabaseError as e:
                con.rollback()
                messagebox.showerror("Issue", e)
        finally:
                if con is not None:
                        con.close()

##View function
def f4():
        stdata.delete(1.0, END)
        root.withdraw()
        vist.deiconify()
        con = None

        try:
                con = connect("sms.db")
                cursor = con.cursor()
                sql = "select * from student"
                cursor.execute(sql)
                data = cursor.fetchall()
                msg = ""
                for d in data:
                        msg = msg + "    Rno: " + str(d[0]) + "\t     Name: " + str(d[1]) + "      \tMarks: " + str(d[2]) + "\n"
                        stdata.insert(INSERT, msg)
        except DatabaseError as e:
                con.rollback()
                messagebox.showerror("Issue", e)

        finally:
                if con is not None:
                        con.close()
def f5():
        root.deiconify()
        vist.withdraw()

def f6():
        upst.deiconify()
        root.withdraw()


##Update function
def f7():
        con = None
        try:
                con = connect("sms.db")
                rno = entUpdtRno.get()
                name = entUpdtName.get()
                marks = entUpdtMarks.get()
                if entUpdtRno.get()=="" or entUpdtName.get()=="" or entUpdtMarks.get()=="":
                        messagebox.showerror("No Entry", "All the fields are compulsary!")
                elif not name.isalpha():
                        messagebox.showerror("Invalid Name Entry", "Please enter valid name!")
                elif len(name)<2:
                        messagebox.showerror("Invalid Name Entry", "Entered Name is too short!")
                elif int(rno)<0:
                        messagebox.showerror("Invalid Entry", "Rno cannot be negative!")
                elif float(marks)<0 or float(marks)>100:
                        messagebox.showerror("Invalid Marks Entry", "Please enter valid marks!")
                else:
                        cursor = con.cursor()
                        sql = "select * from student"
                        cursor.execute(sql)
                        data = cursor.fetchall()
                        rollno_found = 0
                        for row in data:
                                if int(row[0])==int(rno):
                                        cursor = con.cursor()
                                        sql = "update student set name='%s', marks='%f' where rno='%d'"
                                        args = (name, float(marks), int(rno))
                                        cursor.execute(sql % args)
                                        con.commit()
                                        messagebox.showinfo("Success", "Record Updated!")
                                        entUpdtRno.delete(0, END)
                                        entUpdtName.delete(0, END)
                                        entUpdtMarks.delete(0, END)
                                        entUpdtRno.focus()
                                        rollno_found = 1
                        if rollno_found == 0:
                                messagebox.showerror("No Entry", "Roll No not found.")
        except DatabaseError as e:
                con.rollback()
                messagebox.showerror("Issue", e)
        except ValueError:
                messagebox.showerror("Invalid Entry", "Rno or Marks should not be String")
        finally:
                if con is not None:
                        con.close()


def f8():
        root.deiconify()
        upst.withdraw()

##Delete function
def f9():
        dest.deiconify()
        root.withdraw()

def f10():
        try:
                con = connect("sms.db")
                rno = entDelRno.get()
                if entDelRno.get()=="":
                        messagebox.showerror("No Entry", "Please Enter some rno!")
                elif int(rno)<0:
                        messagebox.showerror("Invalid Entry", "Rno cannot be negative!")
                else:
                        cursor = con.cursor()
                        sql = "select * from student"
                        cursor.execute(sql)
                        data = cursor.fetchall()
                        error = 0
                        for row in data:
                                if int(row[0])==int(rno):
                                        cursor = con.cursor()
                                        sql = "delete from student where rno='%d'"
                                        args = (int(rno))
                                        cursor.execute(sql % args)
                                        con.commit()
                                        messagebox.showinfo("Success", "Record Deleted!")
                                        entDelRno.delete(0, END)
                                        error = 1
                        if error==0:
                                messagebox.showerror("No Entry", "Roll No not found.")
        except DatabaseError as e:
                con.rollback()
                messagebox.showerror("Issue", e)
        except ValueError:
                messagebox.showerror("Invalid Entry", "Rno should not be String")
        finally:
                if con is not None:
                        con.close()
def f11():
        root.deiconify()
        dest.withdraw()

##City & Temp function
def f12():
        try:
        	#city
                socket.create_connection(("www.google.com", 80))
                res = requests.get("https://ipinfo.io")
                data = res.json()
                city = data['city']
                entCity.insert(INSERT, city)
                #temp
                a1 = "http://api.openweathermap.org/data/2.5/weather?units=metric"
                a2 = "&q=" + city
                a3 = "&appid=" + "c6e315d09197cec231495138183954bd"
                api_address = a1 + a2 + a3
                res = requests.get(api_address)
                data = res.json()
                temp = data["main"]["temp"]
                entTemp.insert(INSERT, temp)
        except OSError as e:
                messagebox.showerror("Issue", e)

##Quote of the day function
def f13():
        try:
            res = requests.get("https://www.brainyquote.com/quote_of_the_day")
            soup = bs4.BeautifulSoup(res.text, "html.parser")
            quote = soup.find("img", {"class":"p-qotd"})
            msg = quote["alt"]
            entQuote.insert(INSERT, msg)
            entQuote.config(state=DISABLED)
        except:
                messagebox.showerror("Issue", "No internet")

##Graph function
def f14():
        r = []
        n = []
        m = []
        con = None
        try:
                con = connect("sms.db")
                cursor = con.cursor()
                sql = "select * from student"
                cursor.execute(sql)
                data = cursor.fetchall()
                for d in data:
                	r.append((d[0]))
                	n.append(str(d[1]))
                	m.append((d[2]))
        except DatabaseError as e:
        	con.rollback()
        	messagebox.showerror("Issue", e)
        finally:
        	if con is not None:
        		con.close()
        plt.bar(n, m)
        #plt.bar(n, m, width = 0.5)
        plt.title("Student Report")
        plt.xlabel("Student Names ")
        plt.ylabel("Marks ")
        plt.show()


#GUI
##Parent Window
btnAdd = Button(root, text="Add", background="Light Yellow", font=("comic sans ms", 16, "bold"), width=10, command=f1)
btnView = Button(root, text="View", background="Light Yellow", font=("comic sans ms", 16, "bold"), width=10, command=f4)
btnUpdate = Button(root, text="Update", background="Light Yellow", font=("comic sans ms", 16, "bold"), width=10, command=f6)
btnDelete = Button(root, text="Delete", background="Light Yellow", font=("comic sans ms", 16, "bold"), width=10, command=f9)
btnGraph = Button(root, text="Charts", background="Light Yellow", font=("comic sans ms", 16, "bold"), width=10, command=f14)

btnAdd.place(x=150, y=10)
btnView.place(x=150, y=90)
btnUpdate.place(x=150, y=170)
btnDelete.place(x=150, y=250)
btnGraph.place(x=150, y=330)

lblCity = Label(root, text="City: ", background="Light Yellow", font=("comic sans ms", 12, "bold"))
entCity = Entry(root, bd=1, background="Light Yellow", font=("comic sans ms", 12), width=12)

lblTemp = Label(root, text="Temperature: ", background="Light Yellow", font=("comic sans ms", 12, "bold"))
entTemp = Entry(root, bd=1, background="Light Yellow", font=("comic sans ms", 12), width=5)
f12()

lblQuote = Label(root, text="QOTD: ", background="Light Yellow", font=("comic sans ms", 12, "bold"))
entQuote = scrolledtext.ScrolledText(root, bd=1, background="Light Yellow", font=("comic sans ms", 12), width=32, height=3)
f13()

lblCity.place(x=25, y=423)
entCity.place(x=90, y=428)
lblTemp.place(x=268, y=423)
entTemp.place(x=415, y=428)
lblQuote.place(x=10, y=490)
entQuote.place(x=90, y=490)

##Add Window
adst = Toplevel(root)
adst.title("Add Student")
adst.geometry("500x600+600+200")
adst.configure(background="Light Blue")

lblAddRno = Label(adst, text="Enter Rno", font=("comic sans ms", 16, "bold"))
entAddRno = Entry(adst, bd=2, font=("comic sans ms", 16))
lblAddName = Label(adst, text="Enter Name", font=("comic sans ms", 16, "bold"))
entAddName = Entry(adst, bd=2, font=("comic sans ms", 16))
lblAddMarks = Label(adst, text="Enter Marks",
                    font=("comic sans ms", 16, "bold"))
entAddMarks = Entry(adst, bd=2, font=("comic sans ms", 16))

btnAddSave = Button(adst, text="Save", font=(
	"comic sans ms", 16, "bold"), command=f3)
btnAddBack = Button(adst, text="Back", font=(
	"comic sans ms", 16, "bold"), command=f2)

lblAddRno.pack(pady=10)
entAddRno.pack(pady=10)
lblAddName.pack(pady=10)
entAddName.pack(pady=10)
lblAddMarks.pack(pady=10)
entAddMarks.pack(pady=10)

btnAddSave.pack(pady=10)
btnAddBack.pack(pady=10)

adst.withdraw()

##View Window
vist = Toplevel(root)
vist.title("View Students")
vist.geometry("500x600+600+200")
vist.configure(background="Light Blue")

stdata = scrolledtext.ScrolledText(vist, width=40, height=16, font=("comic sans ms", 10))
btnViewBack = Button(vist, text="Back", font=("comic sans ms", 16, "bold"), command=f5)

stdata.pack(pady=35)
btnViewBack.pack(pady=20)

vist.withdraw()

##Update Window
upst = Toplevel(root)
upst.title("Update Student")
upst.geometry("500x600+600+200")
upst.configure(background="Light Blue")

lblUpdtRno = Label(upst, text="Enter Rno", font=("comic sans ms", 16, "bold"))
entUpdtRno = Entry(upst, bd=2, font=("comic sans ms", 16))
lblUpdtName = Label(upst, text="Enter Name",
                    font=("comic sans ms", 16, "bold"))
entUpdtName = Entry(upst, bd=2, font=("comic sans ms", 16))
lblUpdtMarks = Label(upst, text="Enter Marks",
                     font=("comic sans ms", 16, "bold"))
entUpdtMarks = Entry(upst, bd=2, font=("comic sans ms", 16))

btnUpdtUpdate = Button(upst, text="Update", font=(
	"comic sans ms", 16, "bold"), command=f7)
btnUpdtBack = Button(upst, text="Back", font=(
	"comic sans ms", 16, "bold"), command=f8)

lblUpdtRno.pack(pady=10)
entUpdtRno.pack(pady=10)
lblUpdtName.pack(pady=10)
entUpdtName.pack(pady=10)
lblUpdtMarks.pack(pady=10)
entUpdtMarks.pack(pady=10)
btnUpdtUpdate.pack(pady=10)
btnUpdtBack.pack(pady=10)

upst.withdraw()

##Delete Window
dest = Toplevel(root)
dest.title("Delete Student Data")
dest.geometry("500x600+600+200")
dest.configure(background="Light Blue")

lblDelRno = Label(dest, text="Enter Rno", font=("comic sans ms", 16, "bold"))
entDelRno = Entry(dest, bd=2, font=("comic sans ms", 16))
btnDelete = Button(dest, text="Delete", font=(
	"comic sans ms", 16, "bold"), command=f10)
btnDelBack = Button(dest, text="Back", font=(
	"comic sans ms", 16, "bold"), command=f11)

lblDelRno.pack(pady=10)
entDelRno.pack(pady=10)
btnDelete.pack(pady=10)
btnDelBack.pack(pady=10)
dest.withdraw()

root.mainloop()
