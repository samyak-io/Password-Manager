from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_data():
    web = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    new_data = {
        web: {
            "email": email,
            "password": password
        }
    }

    if len(web) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showerror(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        is_ok = messagebox.askokcancel(title=web, message=f"These are the details entered: \nEmail: {email}"
                                                          f"\nPassword: {password}\nIs it ok to save?")
        if is_ok:
            try:
                with open("password-manager-data.json", "r") as file:
                    data = json.load(file)

            except (FileNotFoundError, json.decoder.JSONDecodeError):
                data = new_data

            else:
                data.update(new_data)

            with open("password-manager-data.json", "w") as file:
                json.dump(data, file, indent=4)
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- SEARCH PASSWORD ------------------------------- #

def search_data():
    web = website_entry.get()
    try:
        with open("password-manager-data.json", "r") as file:
            data = json.load(file)

    except FileNotFoundError:
        messagebox.showerror(title="FileNotFoundError", message="No Data File Found.")

    else:
        if web in data:
            email = data[web]['email']
            password = data[web]['password']
            messagebox.showinfo(title=web, message=f"Email: {email}"
                                                   f"\nPassword: {password}")
            pyperclip.copy(password)
        else:
            messagebox.showerror(title="Error", message=f"No details for '{web}' exist.")


# ---------------------------- UI SETUP ------------------------------- #

# window setup
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# canvas setup
canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)
email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# Entries
website_entry = Entry(width=21)
website_entry.focus()
website_entry.grid(column=1, row=1, sticky="EW")
email_entry = Entry(width=35)
email_entry.grid(column=1, row=2, columnspan=2, sticky="EW")
email_entry.insert(0, "samyak.khobragade@outlook.com")
password_entry = Entry(width=21)
password_entry.grid(column=1, row=3, sticky="EW")

# buttons
search_btn = Button(text="Search", borderwidth=1, command=search_data)
search_btn.grid(column=2, row=1, sticky="EW")
generate_pass_btn = Button(text="Generate Password", borderwidth=1, command=generate_password)
generate_pass_btn.grid(column=2, row=3, sticky="EW")
add_btn = Button(text="Add", width=36, borderwidth=1, command=save_data)
add_btn.grid(column=1, row=4, columnspan=2, sticky="EW")

window.mainloop()
