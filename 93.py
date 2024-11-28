# data baise

from tkinter import *
import backend


def clear_list():
    list1.delete(0, END)


def fill_list(books):
    for book in books:
        list1.insert(END, book)


window = Tk()
# ========================lables===============
l1 = Label(window, text="title")
l1.grid(row=0, column=0)

l2 = Label(window, text="auther")
l2.grid(row=0, column=2)

l3 = Label(window, text="year")
l3.grid(row=1, column=0)

l4 = Label(window, text="isbm")
l4.grid(row=1, column=2)

# =============================entrys==================
title_text = StringVar()
en1 = Entry(window, textvariable=title_text)
en1.grid(row=0, column=1)

auther_text = StringVar()
en2 = Entry(window, textvariable=auther_text)
en2.grid(row=0, column=3)

year_text = StringVar()
en3 = Entry(window, textvariable=year_text)
en3.grid(row=1, column=1)

isbm_text = StringVar()
en4 = Entry(window, textvariable=isbm_text)
en4.grid(row=1, column=3)

list1 = Listbox(window, width=40, height=8)
list1.grid(row=2, column=0, rowspan=6, columnspan=2)

sb1 = Scrollbar(window)
sb1.grid(row=2, column=2, rowspan=6)

list1.configure(yscrollcommand=sb1.set)
sb1.configure(command=list1.yview)


def get_selected_row(event):
    global selected_book
    index = list1.curselection()[0]
    selected_book = list1.get(index)
    en1.delete(0, END)
    en1.insert(END, selected_book[1])
    en2.delete(0, END)
    en2.insert(END, selected_book[2])
    en3.delete(0, END)
    en3.insert(END, selected_book[3])
    en4.delete(0, END)
    en4.insert(END, selected_book[4])


list1.bind("<<Listbox Select>>", get_selected_row)


def view_command():
    clear_list()
    books = backend.view()
    fill_list(books)


bt1 = Button(window, text="view all", width=12, command=lambda: view_command())
bt1.grid(row=2, column=3)


def search_command():
    clear_list()
    books = backend.search(title_text.get(), auther_text.get(), year_text.get(), isbm_text.get())
    fill_list(books)


bt2 = Button(window, text="search entry", width=12,command=lambda: search_command())
bt2.grid(row=3, column=3)


def add_command():
    backend.insert(title_text.get(), auther_text.get(),year_text.get(), isbm_text.get())
    view_command()


bt3 = Button(window, text="add entry", width=12, command=lambda: add_command())
bt3.grid(row=4, column=3)


def delete_command():
    backend.delete(selected_book()[0])
    view_command()


bt4 = Button(window, text="update select", width=12,command=lambda: update_command())
bt4.grid(row=5, column=3)


def update_command():
    backend.update(selected_book[0],title_text.get(), auther_text.get(),year_text.get(), isbm_text.get())
    view_command()
bt5 = Button(window, text="delet select", width=12,command=lambda: delete_command())
bt5.grid(row=6, column=3)

bt6 = Button(window, text="close", width=12)
bt6.grid(row=7, column=3)


window.mainloop()
