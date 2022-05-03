from ast import excepthandler
from tkinter import *
from PIL import ImageTk, Image
from typing import final
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="db_praktikum"
)

dbcursor = mydb.cursor()

root = Tk()
root.title("Praktikum DPBO")


# Fungsi untuk mengambil data
def getMhs():
    global mydb
    global dbcursor

    dbcursor.execute("SELECT * FROM mahasiswa")
    result = dbcursor.fetchall()

    return result


# Window Input Data
def inputs():
    # Hide root window
    global root
    root.withdraw()

    top = Toplevel()
    top.title("Input")
    dframe = LabelFrame(top, text="Input Data Mahasiswa", padx=10, pady=10)
    dframe.pack(padx=10, pady=10)
    # Input 1
    label1 = Label(dframe, text="Nama Mahasiswa").grid(row=0, column=0, sticky="w")
    input_nama = Entry(dframe, width=30)
    input_nama.grid(row=0, column=1, padx=20, pady=10, sticky="w")
    # Input 2
    label2 = Label(dframe, text="NIM").grid(row=1, column=0, sticky="w")
    input_nim = Entry(dframe, width=30)
    input_nim.grid(row=1, column=1, padx=20, pady=10, sticky="w")
    
    # Input 3
    input_jk = StringVar(root)
    input_jk.set("0")
    values = {"Laki-Laki" : "Laki-Laki",
               "Perempuan" : "Perempuan"}

    label3 = Label(dframe, text="Jenis Kelamin").grid(row=2, column=0, sticky="w")
    i = 20
    for (text, value) in values.items():
        input3 = Radiobutton(dframe, text = text, variable = input_jk, value = value)
        input3.grid(row=2, column=1, padx=i, pady=10, sticky="w")
        i += 100

    # input 4
    options = ["Filsafat Meme", "Sastra Mesin", "Teknik Kedokteran", "Pendidikan Gaming"]
    input_jurusan = StringVar(root)
    input_jurusan.set(options[0])
    label4 = Label(dframe, text="Jurusan").grid(row=3, column=0, sticky="w")
    dropdown = OptionMenu(dframe, input_jurusan, *options)
    dropdown.grid(row=3, column=1, padx=20, pady=10, sticky='w')

    #input 5
    def isChecked():
        hobby_value = []
        if(input_hobi1.get() == 1):
            hobby_value.append("Main Game")
        if(input_hobi2.get() == 1):
            hobby_value.append("Sepak Bola")
        if(input_hobi3.get() == 1):
            hobby_value.append("Bulu Tangkis")

        return hobby_value        

    input_hobi1 = IntVar()
    input_hobi2 = IntVar()
    input_hobi3 = IntVar()
    
    label5 = Label(dframe, text="Hobi").grid(row=4, column=0, sticky='w')

    checkme = Checkbutton(dframe, text='Main Game',variable = input_hobi1, onvalue=1, offvalue=0)
    checkme.grid(row=4, column=1, padx=20, pady=10, sticky='w')
    checkme = Checkbutton(dframe, text='Sepak Bola',variable = input_hobi2, onvalue=1, offvalue=0)
    checkme.grid(row=4, column=1, padx=120, pady=10, sticky='w')
    checkme = Checkbutton(dframe, text='Bulu Tangkis',variable = input_hobi3, onvalue=1, offvalue=0)
    checkme.grid(row=4, column=1, padx=220, pady=10, sticky='w')

    # Button Frame
    frame2 = LabelFrame(dframe, borderwidth=0)
    frame2.grid(columnspan=2, column=0, row=10, pady=10)

    # Submit Button
    btn_submit = Button(frame2, text="Submit Data", anchor="s", command=lambda:[insertData(top, input_nama, input_nim, input_jk, input_jurusan, isChecked()), top.withdraw()])
    btn_submit.grid(row=4, column=0, padx=10)

    # Cancel Button
    btn_cancel = Button(frame2, text="Gak jadi / Kembali", anchor="s", command=lambda:[top.destroy(), root.deiconify()])
    btn_cancel.grid(row=4, column=1, padx=10)

# Untuk memasukan data
def insertData(parent, p_nama, p_nim, p_jenis_kel, p_jurusan, p_hobby):
    flag_validation = True
    top = Toplevel()
    # Get data
    nama = p_nama.get()
    nim = p_nim.get()
    jurusan = p_jurusan.get()
    jenis_kel = p_jenis_kel.get()
    hobby = ", ".join(p_hobby)

    if((nama == "") or (nim == "") or (jenis_kel == "0")):
        flag_validation = False
    
    if(flag_validation == True):    
        # Input data disini
        try:
            sql = "INSERT INTO mahasiswa (nim, nama, jenis_kel, jurusan, hobi) VALUES (%s, %s, %s, %s, %s)"
            val = (nim, nama, jenis_kel, jurusan, hobby)
            dbcursor.execute(sql, val)
            mydb.commit()
        
            label5 = Label(top, text="Record Successfully Inserted into mahasiswa table", anchor="s", fg='green').pack(padx=10, pady=10)
            btn_ok = Button(top, text="Syap!", anchor="s", command=lambda:[top.destroy(), root.deiconify()])
            btn_ok.pack(padx=10, pady=10)
        except mysql.connector.Error as error:
            label5 = Label(top, text="Failed to Insert record into mahasiswa table {}".format(error), anchor="s", fg='red').pack(padx=10, pady=10)
            btn_back = Button(top, text="Back", anchor="s", command=lambda:[top.destroy(), parent.deiconify()])
            btn_back.pack(padx=10, pady=10)    
    else:
        label5 = Label(top, text="Input Not Valid!", anchor="s", bg='yellow', fg='red').pack(padx=10, pady=10)
        btn_back = Button(top, text="Back", anchor="s", command=lambda:[top.destroy(), parent.deiconify()])
        btn_back.pack(padx=10, pady=10)    

  
# Window Semua Mahasiswa
def viewAll():
    global root
    root.withdraw()

    top = Toplevel()
    top.title("Semua Mahasiswa")
    frame = LabelFrame(top, borderwidth=0)
    frame.pack()

    # Cancel Button
    btn_cancel = Button(frame, text="Kembali", anchor="w", command=lambda:[top.destroy(), root.deiconify()])
    btn_cancel.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    # Head title
    head = Label(frame, text="Data Mahasiswa")
    head.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    tableFrame = LabelFrame(frame)
    tableFrame.grid(row=1, column = 0, columnspan=2)

    # Get All Data
    result = getMhs()

    # Title
    title1 = Label(tableFrame, text="No.", borderwidth=1, relief="solid", width=3, padx=5).grid(row=0, column=0)
    title2 = Label(tableFrame, text="NIM", borderwidth=1, relief="solid", width=15, padx=5).grid(row=0, column=1)
    title3 = Label(tableFrame, text="Nama", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=2)
    title4 = Label(tableFrame, text="Jenis Kelamin", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=3)
    title5 = Label(tableFrame, text="Jurusan", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=4)
    title5 = Label(tableFrame, text="Hobi", borderwidth=1, relief="solid", width=30, padx=5).grid(row=0, column=5)

    # Print content
    i = 0
    for data in result:
        label1 = Label(tableFrame, text=str(i+1), borderwidth=1, relief="solid", height=2, width=3, padx=5).grid(row=i+1, column=0)
        label2 = Label(tableFrame, text=data[1], borderwidth=1, relief="solid", height=2, width=15, padx=5).grid(row=i+1, column=1)
        label3 = Label(tableFrame, text=data[2], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=2)
        label4 = Label(tableFrame, text=data[3], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=3)
        label4 = Label(tableFrame, text=data[4], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=4)
        label4 = Label(tableFrame, text=data[5], borderwidth=1, relief="solid", height=2, width=30, padx=5).grid(row=i+1, column=5)
        i += 1

# Dialog konfirmasi hapus semua data
def clearAll():
    top = Toplevel()
    lbl = Label(top, text="Yakin mau hapus semua data?")
    lbl.pack(padx=20, pady=20)
    btnframe = LabelFrame(top, borderwidth=0)
    btnframe.pack(padx=20, pady=20)

    # Yes
    btn_yes = Button(btnframe, text="Gass", bg="green", fg="white", command=lambda:[top.destroy(), delAll()])
    btn_yes.grid(row=0, column=0, padx=10)
    # No
    btn_no = Button(btnframe, text="Tapi boong", bg="red", fg="white", command=top.destroy)
    btn_no.grid(row=0, column=1, padx=10)

# Dialog konfirmasi keluar GUI
def exitDialog():
    global root
    root.withdraw()
    top = Toplevel()
    lbl = Label(top, text="Yakin mau keluar?")
    lbl.pack(padx=20, pady=20)
    btnframe = LabelFrame(top, borderwidth=0)
    btnframe.pack(padx=20, pady=20)

    # Yes
    btn_yes = Button(btnframe, text="Gass", bg="green", fg="white", command=lambda:[top.destroy(), root.destroy()])
    btn_yes.grid(row=0, column=0, padx=10)
    # No
    btn_no = Button(btnframe, text="Tapi boong", bg="red", fg="white", command=lambda:[top.destroy(), root.deiconify()])
    btn_no.grid(row=0, column=1, padx=10)

def delAll():
    top = Toplevel()

    # Delete data disini
    try:
        dbcursor.execute("DELETE FROM mahasiswa")
        mydb.commit()
    
        label5 = Label(top, text="All Record Successfully Deleted from mahasiswa table", anchor="s", fg='green').pack(padx=10, pady=10)
        btn_ok = Button(top, text="OK!", command=top.destroy)
        btn_ok.pack(pady=20)
    except mysql.connector.Error as error:
        label5 = Label(top, text="Failed to Delete all record from mahasiswa table {}".format(error), anchor="s", fg='red').pack(padx=10, pady=10)
        btn_ok = Button(top, text="Back", command=top.destroy)
        btn_ok.pack(pady=20)

def seeFacility():
    global root
    root.withdraw()

    top = Toplevel()
    top.title("Daftar Fasilitas")
    frame = LabelFrame(top, borderwidth=0)
    frame.pack()

    # Cancel Button
    btn_cancel = Button(frame, text="Kembali", anchor="w", command=lambda:[top.destroy(), root.deiconify()])
    btn_cancel.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    # Head title
    head = Label(frame, text="Data Fasilitas Kampus")
    head.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    tableFrame = LabelFrame(frame)
    tableFrame.grid(row=1, column = 0, columnspan=2)

    # Title
    title2 = Label(tableFrame, text="Nama", borderwidth=1, relief="solid", width=15, padx=5).grid(row=0, column=0)
    title2 = Label(tableFrame, text="Foto", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=1)

    # content
    name1 = Label(tableFrame, text="Lab. Komputer", borderwidth=0, relief="solid", height=2, width=15, padx=5).grid(row=1, column=0)
    name2 = Label(tableFrame, text="Perpustakaan", borderwidth=0, relief="solid", height=2, width=15, padx=5).grid(row=2, column=0)
    name3 = Label(tableFrame, text="Ruang Kelas", borderwidth=0, relief="solid", height=2, width=15, padx=5).grid(row=3, column=0)
    
    # content picture1
    pic1 = Image.open("project/labkom.png")
    resize_pic1 = pic1.resize((150, 100))
    new_pic1 = ImageTk.PhotoImage(resize_pic1)
    img1 = Label(tableFrame, image = new_pic1, padx=20)
    img1.photo = new_pic1
    img1.grid(row=1, column=1)

    # content picture1
    pic2 = Image.open("project/perpustakaan.png")
    resize_pic2 = pic2.resize((150, 100))
    new_pic2 = ImageTk.PhotoImage(resize_pic2)
    img2 = Label(tableFrame, image = new_pic2, padx=20)
    img2.photo = new_pic2
    img2.grid(row=2, column=1)
    
    # content picture1
    pic3 = Image.open("project/ruangkelas.png")
    resize_pic3 = pic3.resize((150, 100))
    new_pic3 = ImageTk.PhotoImage(resize_pic3)
    img3 = Label(tableFrame, image = new_pic3, padx=20)
    img3.photo = new_pic3
    img3.grid(row=3, column=1)

# Title Frame
frame = LabelFrame(root, text="Praktikum DPBO", padx=10, pady=10)
frame.pack(padx=10, pady=10)

# ButtonGroup Frame
buttonGroup = LabelFrame(root, padx=10, pady=10)
buttonGroup.pack(padx=10, pady=10)

# Title
label1 = Label(frame, text="Data Mahasiswa", font=(30))
label1.pack()

# Description
label2 = Label(frame, text="Ceritanya ini database mahasiswa ngab")
label2.pack()

# Input btn
b_add = Button(buttonGroup, text="Input Data Mahasiswa", command=inputs, width=30)
b_add.grid(row=0, column=0, pady=5)

# All data btn
b_add = Button(buttonGroup, text="Semua Data Mahasiswa", command=viewAll, width=30)
b_add.grid(row=1, column=0, pady=5)

# Clear all btn
b_clear = Button(buttonGroup, text="Hapus Semua Data Mahasiswa", command=clearAll, width=30)
b_clear.grid(row=2, column=0, pady=5)

#Facility Button
b_facility = Button(buttonGroup, text="Lihat Fasilitas", command=seeFacility , width=30)
b_facility.grid(row=3, column=0, pady=5)

# Exit btn
b_exit = Button(buttonGroup, text="Exit", command=exitDialog, width=30)
b_exit.grid(row=4, column=0, pady=5)

root.mainloop()