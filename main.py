import tkinter as tk
import pyperclip
import json
from tkinter import messagebox
from random import randint, choice, shuffle

# ---------------------------- CONSTANT ------------------------------- #
LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
SYMBOLS = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
FONT_NAME = 'Arial'


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generator():
    """Generate a random strong password"""
    password_entry.delete(0, 'end')

    password_letters = [choice(LETTERS) for _ in range(randint(8, 14))]
    password_numbers = [choice(NUMBERS) for _ in range(randint(2, 4))]
    password_symbols = [choice(SYMBOLS) for _ in range(randint(2, 4))]

    password = password_letters + password_numbers + password_symbols
    shuffle(password)
    str_password = ''.join(password)
    password_entry.insert(0, str_password)
    pyperclip.copy(str_password)


# ---------------------------------------------- SAVE PASSWORD MECHANISM---------------------------------------------- #
def account_data(a_data):
    """Write website account data to the 'data.json'"""
    with open('data.json', 'w') as data_file:
        json.dump(a_data, data_file, indent=4)


def read_data():
    """Read 'data.json' file"""
    with open('data.json') as file_data:
        return json.load(file_data)


def is_exist():
    """Checking if the website account already exist in 'data.json' file"""
    data = read_data()
    website = website_entry.get().upper()
    return website in data  # Return True or False


def website_account(website):
    """Retrieve user account email and password already stored in 'data.json' file"""
    data = read_data()
    email = data[website]['email']
    password = data[website]['password']
    messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")


def save():
    """Saving website account email and password to 'data.json' file"""
    website = website_entry.get().upper()
    email_uname = email_uname_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            'email': email_uname,
            'password': password
        }
    }
    if website == "" or password == "":
        messagebox.showwarning(title="Oops", message="Please dont leave any fields empty!")
    else:
        try:
            # Tries to read the 'data.json' file if the file exists or has contents
            data = read_data()
        except json.decoder.JSONDecodeError:
            # Detect and adding the new data if the 'data.json' file doesn't have any contents or empty
            account_data(new_data)
        except FileNotFoundError:
            # Detect and adding the new data if the 'data.json' file doesn't exist
            account_data(new_data)
        else:
            # Append the new data to the 'data.json' file and change the details if the website account already exist
            if is_exist():
                is_ok = messagebox.askokcancel(title="Oops",
                                               message=f"Your {website} account has been added, "
                                                       f"do you want to change the website account details to:\n"
                                                       f"Email: {email_uname}\nPassword: {password}")
                if is_ok:
                    data.update(new_data)
                    account_data(data)
            else:
                data.update(new_data)
                account_data(data)
        finally:
            # Clear the website and password entry and set the cursor focus back to the website entry
            website_entry.delete(0, 'end')
            password_entry.delete(0, 'end')
            website_entry.focus()


def search():
    """Searching the website account email and password if it has been stored in the data.json file"""
    website = website_entry.get().upper()
    try:
        read_data()
    except FileNotFoundError:
        messagebox.showwarning(title="Error", message="No Data File Found.")
    else:
        if is_exist():
            website_account(website)
        else:
            messagebox.showwarning(title="Error", message="No Details for the Website Exists.")


# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

logo_img = tk.PhotoImage(file='logo.png')
canvas = tk.Canvas(width=200, height=200)
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Website Label and Entry and Search Button
website_text = tk.Label(text="Website:", font=(FONT_NAME, 10, 'normal'))
website_text.grid(row=1, column=0)

website_entry = tk.Entry(font=(FONT_NAME, 10, 'normal'))
website_entry.focus()
website_entry.grid(row=1, column=1, sticky="EW")

search_btn = tk.Button(text="Search", command=search)
search_btn.grid(row=1, column=2, sticky="EW")

# Email/Username Label and Entry
email_uname_label = tk.Label(text="Email/Username:", font=(FONT_NAME, 10, 'normal'))
email_uname_label.grid(row=2, column=0)

email_uname_entry = tk.Entry(font=(FONT_NAME, 10, 'normal'))
email_uname_entry.insert(0, "patrrarwsinaga4@gmail.com")
email_uname_entry.grid(row=2, column=1, columnspan=2, sticky="EW")

# Password Label, Entry, and Button
password_label = tk.Label(text="Password:", font=(FONT_NAME, 10, 'normal'))
password_label.grid(row=3, column=0)

password_entry = tk.Entry(font=(FONT_NAME, 10, 'normal'))
password_entry.grid(row=3, column=1, sticky="EW")

password_btn = tk.Button(text="Generate Password", command=password_generator)
password_btn.grid(row=3, column=2, sticky="EW")

# Add button
add_button = tk.Button(text="Add", width=42, highlightthickness=0, command=save)
add_button.grid(row=4, column=1, columnspan=2, sticky="EW")

window.mainloop()
