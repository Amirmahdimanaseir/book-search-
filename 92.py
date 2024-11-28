from tkinter import *
import tkinter.messagebox

# ===============================setting=========================
root = Tk()
root.title("calculator")
root.geometry("400x300")
root.resizable(width=False, height=False)
color = "gray"
root.configure(bg=color)
# ===============================variables=========================
number1 = StringVar()
number2 = StringVar()
resvalue = StringVar()
# ===============================frame=============================
frame1 = Frame(root, width=400, height=75, bg=color)
frame1.pack(side=TOP)
frame2 = Frame(root, width=400, height=75, bg=color)
frame2.pack(side=TOP)
frame3 = Frame(root, width=400, height=75, bg=color)
frame3.pack(side=TOP)
frame4 = Frame(root, width=400, height=75, bg=color)
frame4.pack(side=TOP)
# ===============================functions===========================


def errormsg(ms):
    if ms == "error":
        tkinter.messagebox.showerror("error", "something went wrong")
    elif ms == "divition zero error":
        tkinter.messagebox.showerror(
            "divition xero error ", "can not divide by 0")


def pluse():
    try:
        value = float(number1.get()) + float(number2.get())
        resvalue.set(value)
    except:
        errormsg("error")


def minus1():
    try:
        value = float(number1.get()) - float(number2.get())
        resvalue.set(value)
    except:
        errormsg("error")


def mull1():
    try:
        value = float(number1.get()) * float(number2.get())
        resvalue.set(value)
    except:
        errormsg("error")


def dividd():
    if number2.get() == "0":
        errormsg("error for multiply function")
    try:
        value = float(number1.get()) / float(number2.get())
        resvalue.set(value)
    except:
        errormsg("error")


# ===============================buttons===========================
btn_plus1 = Button(frame3,  text="+", width=9,highlightbackground=color, command=lambda: pluse())
btn_plus1.pack(side=LEFT, padx=10, pady=10)
btn_minus1 = Button(frame3,  text="-", width=9,highlightbackground=color, command=lambda: minus1())
btn_minus1.pack(side=LEFT, padx=10, pady=10)
btn_mull1 = Button(frame3,  text="*", width=9,highlightbackground=color, command=lambda: mull1())
btn_mull1.pack(side=LEFT, padx=10, pady=10)
btn_dividd = Button(frame3,  text="/", width=9,highlightbackground=color, command=lambda: dividd())
btn_dividd.pack(side=LEFT, padx=10, pady=10)
# ===============================entry and lables==================
lablee_1 = Label(frame1, text="inpute number 1: ", bg=color)
lablee_1.pack(side=LEFT, padx=10, pady=10)
enterr1 = Entry(frame1, highlightbackground=color, textvariable=number1)
enterr1.pack(side=LEFT)
lablee_2 = Label(frame2, text="inpute number 2: ", bg=color)
lablee_2.pack(side=LEFT, pady=10, padx=10)
enterr2 = Entry(frame2, highlightbackground=color, textvariable=number2)
enterr2.pack(side=LEFT)
ress = Label(frame4, text="result", bg=color)
ress.pack(side=LEFT, padx=10, pady=10)
resnumber = Entry(frame4, highlightbackground=color, textvariable=resvalue)
resnumber.pack(side=LEFT)
# ===============================variables=========================














root.mainloop()
