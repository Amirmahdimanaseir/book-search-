from tkinter import *
#======================settings==============
root = Tk()
root.title("calculator")
root.geometry("350x350")
root.resizable(width= False , height= False)
color = "black"
root.configure( bg = color)
#======================frames==============
topfirst = Frame(root , width=350 , height=85,bg="blue")
topfirst.pack(side=TOP)

topfirst1 = Frame(root , width=350 , height=85,bg="red")
topfirst1.pack(side=TOP)

topfirst2 = Frame(root , width=350 , height=85,bg="green")
topfirst2.pack(side=TOP)

topfirst3 = Frame(root , width=350 , height=85,bg="yellow")
topfirst3.pack(side=BOTTOM)
#======================================items====================
















lable = Label(root,text = "please enter one number or ....")

lable.place(x=85,y=85)

enter = Entry(root)
enter.place(x=110,y=110)

btn = Button(root, text="result")
btn.place(x=140,y=140)




mainloop()