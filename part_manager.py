from tkinter import *
from tkinter import messagebox
from db import Database

# window object
app = Tk()

db=Database('store.db')

# functions

def populate_list():
    for row in db.fetch():
        parts_list.insert(END, row)

def add_item():
    # if empty, show error and return
    if part_text.get() == '' or customer_text.get() == '' or retailer_text.get() == '' or price_text.get() == '':
        messagebox.showerror('Required fields', 'Please include all fields')
        return
    db.insert(part_text.get(), customer_text.get(), retailer_text.get(), price_text.get())
    #delete old list
    parts_list.delete(0, END)
    #insert item to the end
    parts_list.insert(END, (part_text.get(), customer_text.get(), retailer_text.get(), price_text.get()))
    #repopulate list
    populate_list()

def select_item(event):
    try:
        global selected_item
        #get item index of list
        index = parts_list.curselection()[0]
        selected_item = parts_list.get(index)
        #delete what's currently in the entry field
        part_entry.delete(0, END)
        #add the selected item aprt to the entry field
        part_entry.insert(END, selected_item[1])
        customer_entry.delete(0, END)
        customer_entry.insert(END, selected_item[2])
        retailer_entry.delete(0, END)
        retailer_entry.insert(END, selected_item[3])
        price_entry.delete(0, END)
        price_entry.insert(END, selected_item[4])
    except IndexError:
        pass

def remove_item():
    #remove selected item
    db.remove(selected_item[0])
    clear_text()
    populate_list()


def update_item():
    #update selected item with entry text
    db.update(selected_item[0], part_text.get(), customer_text.get(),
              retailer_text.get(), price_text.get())
    populate_list()


def clear_items():
    #delete all entries
    part_entry.delete(0, END)
    customer_entry.delete(0, END)
    retailer_entry.delete(0, END)
    price_entry.delete(0, END)

# Part Label
part_text = StringVar()
part_label = Label(app, text='Part Name', font=('bold', 14), pady=20)
# grid method places the var on the screen
part_label.grid(row=0, column=0, sticky=W)

part_entry = Entry(app, textvariable=part_text)
part_entry.grid(row=0, column=1)

# Part Label
customer_text = StringVar()
customer_label = Label(app, text='Customer Name', font=('bold', 14), pady=20)
customer_label.grid(row=0, column=2, sticky=W)

customer_entry = Entry(app, textvariable=customer_text)
customer_entry.grid(row=0, column=3)

# Part Label
retailer_text = StringVar()
retailer_label = Label(app, text='Retailer Name', font=('bold', 14), pady=20)
retailer_label.grid(row=1, column=0, sticky=W)

retailer_entry = Entry(app, textvariable=retailer_text)
retailer_entry.grid(row=1, column=1)

# Part Label
price_text = StringVar()
price_label = Label(app, text='Price', font=('bold', 14), pady=20)
# grid method places the var on the screen
price_label.grid(row=1, column=2, sticky=W)

price_entry = Entry(app, textvariable=price_text)
price_entry.grid(row=1, column=3)



# Parts list (textbox)
parts_list = Listbox(app, height=8, width=50)
parts_list.grid(row=3, column=0, columnspan=3, rowspan=6, pady=20, padx=20)

# scrollbar
scrollbar = Scrollbar(app)
scrollbar.grid(row=3, column=3)
#connect scroll
parts_list.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=parts_list.yview)

# Bind select
parts_list.bind('<<ListboxSelect>>', select_item)


#Buttons
add_btn = Button(app, text='Add Part', width=12, command=add_item)
add_btn.grid(row=2, column=0, pady=20)
remove_btn = Button(app, text='Remove Part', width=12, command=remove_item)
remove_btn.grid(row=2, column=1)
update_btn = Button(app, text='Update Part', width=12, command=update_item)
update_btn.grid(row=2, column=2)
clear_btn = Button(app, text='Clear Parts', width=12, command=clear_items)
clear_btn.grid(row=2, column=3)

# set vars
app.title('Part Manager')
app.geometry('700x350')

#init data

populate_list()

# run gui
app.mainloop()