import pymysql
from tkinter import *
from tkinter import messagebox

connection = pymysql.connect("localhost", "raghav", "password", "attendance_system")
cursor = connection.cursor()

def popup_error():
    messagebox.showerror("Error", "Error Occur!!")

def str2date(s_date):
    if(len(s_date)!=8):
        s_date = "0"+s_date
    return s_date[:2]+"."+s_date[2:4]+"."+s_date[4:]+"  "

class table:
    def __init__(self,data,roll_no,dates,_id,subject,frame):
        self.data = data
        self.frame = frame
        self.roll_no = roll_no
        self.dates = dates
        self._id = _id
        self.subject = subject
        self.matrix = []
    
    def on_click(self,i,j):
        self.data[i][j] = "A" if self.data[i][j]=="P" else "P"
        self.matrix[i][j].set(self.data[i][j])
        SQL_QUERY = "UPDATE class SET `%s`=%s WHERE id = %s and roll_no = %s and subject = %s"
        cursor.execute(SQL_QUERY, (int(self.dates[j]),self.data[i][j],self._id,self.roll_no[i],self.subject))
        connection.commit()
    
    def display(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        on_click = lambda i,j : (lambda: self.on_click(i,j))
        meta = ["Roll No.  ", ] + [str2date(x) for x in self.dates]
        for i in range(len(meta)):
            Label(self.frame, text = meta[i]).grid(row=0,column=i)
        for i in range(len(self.roll_no)):
            Label(self.frame, text = self.roll_no[i]).grid(row=i+1,column=0)
        for i in range(len(self.data)):
            row = []
            for j in range(len(self.data[0])):
                txt = StringVar()
                Button(self.frame, textvariable = txt, command = on_click(i,j)).grid(row=i+1,column=j+1)
                txt.set(self.data[i][j])
                row.append(txt)
            self.matrix.append(row)

window = Tk()
window.title("Attendance System")

frame1 = LabelFrame(window, text="Login Section", padx=5, pady=5)
frame1.grid(row=0,column=0)
frame2 = LabelFrame(window, text="Profile Section", padx=5, pady=5)
frame2.grid(row=0,column=1)
frame3 = LabelFrame(window, text="Attendance Section", padx=5, pady=5)
frame3.grid(row=1,column=0,columnspan=2)

Label(frame1, text="Enter your id").grid(column=0, row=0)
e = Entry(frame1)
e.grid(column=1, row=0)

def faculty_func():
    for widget in frame2.winfo_children():
        widget.destroy()
    for widget in frame3.winfo_children():
        widget.destroy()
        
    try:
        _id = int(e.get())
        
        SQL_QUERY_1 = "SELECT * FROM faculty WHERE id = %s"
        cursor.execute(SQL_QUERY_1, (_id,))
        faculty = cursor.fetchone()
        
        SQL_QUERY_2 = "SELECT DISTINCT subject FROM class WHERE id = %s"
        cursor.execute(SQL_QUERY_2, (_id,))
        subject = [sub[0] for sub in cursor.fetchall()]
        
        cred = ["ID", "Name", "Age"]
        
        if faculty!=None:
            for i in range(len(cred)):
                Label(frame2, text = cred[i] + " : ").grid(row=i,column=0)
                Label(frame2, text = str(faculty[i])).grid(row=i,column=1)
        
            if len(subject):
                Label(frame2, text = "Subjects : ").grid(row=3,column=0)
                for i in range(len(subject)):
                    Label(frame2, text = subject[i]).grid(row=3+i,column=1)
                    
            Label(frame3, text  = "Date").grid(row=0,column=0)
            
            query_date = Entry(frame3,width=10)
            query_date.insert(0,"ddmmyyyy")
            query_date.grid(row=0,column=1)
            
            clicked = StringVar()
            clicked.set(subject[0])
            query_subject = OptionMenu(frame3, clicked, *subject).grid(row=0,column=2)
            
            frame4 = Frame(frame3)
            frame4.grid(row=1,column=0,columnspan=4)
            
            def get_attendance():
                try:
                    date = query_date.get()
                    sub = clicked.get()
                    if date == "ddmmyyyy":
                        SQL_QUERY_3 = "SELECT * FROM class WHERE id = %s and subject = %s"
                        cursor.execute(SQL_QUERY_3, (_id, sub))
                        result = cursor.fetchall()
                        roll_no = [x[1] for x in result]
                        data = [list(x[3:]) for x in result]
                        
                        SQL_QUERY_4 = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = %s"
                        cursor.execute(SQL_QUERY_4, ('class',))
                        dates = [x[0] for x in cursor.fetchall()[3:] ]
                        
                    else:
                        SQL_QUERY_3 = "SELECT roll_no, `%s` FROM class WHERE id = %s and subject = %s"
                        cursor.execute(SQL_QUERY_3, (int(date),_id, sub))
                        result = cursor.fetchall()
                        roll_no = [x[0] for x in result]
                        data = [list(x[1]) for x in result]
                        dates = [date, ]
                    
                    t = table(data,roll_no,dates,_id,sub,frame4)
                    t.display()
                except:
                    for widget in frame2.winfo_children():
                        widget.destroy()
                    for widget in frame3.winfo_children():
                        widget.destroy()
                    popup_error()
            
            search_btn = Button(frame3, text = "Search", command = get_attendance).grid(row=0,column=3)
        
        else:
            messagebox.showerror("Error occur", "User not found!!")
    except:
        for widget in frame2.winfo_children():
            widget.destroy()
        for widget in frame3.winfo_children():
            widget.destroy()
        popup_error()

def student_func():
    for widget in frame2.winfo_children():
        widget.destroy()
    for widget in frame3.winfo_children():
        widget.destroy()
    
    try:
        roll_no = int(e.get())
        
        SQL_QUERY_1 = "SELECT * FROM student WHERE roll_no = %s"
        cursor.execute(SQL_QUERY_1, (roll_no,))
        student = cursor.fetchone()
        
        if student!=None:
            SQL_QUERY_2 = "SELECT * FROM class WHERE roll_no = %s"
            cursor.execute(SQL_QUERY_2, (roll_no,))
            result = cursor.fetchall()
            cred = ["ID", "Name", "Age"]
            for i in range(len(cred)):
                Label(frame2, text = cred[i] + " : ", justify = "left").grid(row=i,column=0)
                Label(frame2, text = str(student[i]), justify = "left").grid(row=i,column=1)
            
            Label(frame2, text = "Subjects : ").grid(row=3,column=0)
            for i in range(len(result)):
                Label(frame2, text = result[i][2]).grid(row=3+i,column=1)

            SQL_QUERY_4 = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = %s"
            cursor.execute(SQL_QUERY_4, ('class',))
            dates = [str2date(x[0]) for x in cursor.fetchall()[3:] ]
            Label(frame3, text = "Roll No.  ").grid(row=0,column=0)
            for i in range(len(dates)):
                Label(frame3, text = dates[i]).grid(row=0,column=i+1)
            
            for i in range(len(result)):
                Label(frame3, text = result[i][2]).grid(row=i+1,column=0)
                for j in range(len(result[i][3:])):
                    Label(frame3, text = result[i][3+j]).grid(row=i+1,column=j+1)
            
        else:
            messagebox.showerror("Error occur", "User not found!!")
    except:
        for widget in frame2.winfo_children():
            widget.destroy()
        for widget in frame3.winfo_children():
            widget.destroy()
        popup_error()



student_btn = Button(frame1, text="I am a Faculty", command = faculty_func).grid(column=0,row=1)
student_btn = Button(frame1, text="I am a Student", command = student_func).grid(column=1,row=1)

window.mainloop()
connection.close()