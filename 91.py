from tkinter import *

# =====================setting=======
root = Tk()
root.title("culculate")
root.geometry("400x300")
root.resizable(width=False, height=False)
color = "gray"
root.configure(bg=color)
# =====================frame=======
frame1 = Frame(root, width=400, height=65, bg=color)
frame1.pack(side=TOP)
frame2 = Frame(root, width=400, height=65, bg=color)
frame2.pack(side=TOP)
frame3 = Frame(root, width=400, height=65, bg=color)
frame3.pack(side=TOP)
frame4 = Frame(root, width=400, height=65, bg=color)
frame4.pack(side=TOP)
# ====================buttons=======================
btn_plus = Button(frame3, text="+", width=9, highlightbackground=color)
btn_plus.pack(side=LEFT, padx=10, pady=10)

btn_minus = Button(frame3, text="-", width=9, highlightbackground=color)
btn_minus.pack(side=LEFT, padx=10, pady=10)

btn_mul = Button(frame3, text="*", width=9, highlightbackground=color)
btn_mul.pack(side=LEFT, padx=10, pady=10)

btn_divid = Button(frame3, text="/", width=9, highlightbackground=color)
btn_divid.pack(side=LEFT, padx=10, pady=10)
# ============================entres and lables=====================
lable_1 = Label(frame1, text="inpute number 1: ", bg=color)
lable_1.pack(side=LEFT, pady=10, padx=10)

enter1 = Entry(frame1, highlightbackground=color)
enter1.pack(side=LEFT)

lable_2 = Label(frame2, text="inpute number 2: ", bg=color)
lable_2.pack(side=LEFT, pady=10, padx=10)

enter2 = Entry(frame2, highlightbackground=color)
enter2.pack(side=LEFT)

res = Label(frame4, text="Result", bg=color)
res.pack(side=LEFT, padx=10, pady=10)

resnumber = Entry(frame4, highlightbackground=color)
resnumber.pack(side=LEFT)


mainloop()
