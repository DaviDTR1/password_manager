from tkinter import *
import random
from tkinter import messagebox
import json

PURPLE_STRONG = "#150050"
BLUE = "#8FD6E1"
PURPLE_SOFT = "#610094"
GRAY = "#444444"
DARK = "#151515"
LETTERS = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
           'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

NUM = [str(i) for i in range(10)]

SYMBOLS = ['!','#','$','%','&','(',')','*','+','_'] 

# ----------------------- Password Generator -------------------------------------------------
def generator_password_button_clicked():

    nr_letters = random.randint(6,8)
    nr_symbols = random.randint(2,4)
    nr_numbers = random.randint(2,4)

    password_list = [random.choice(LETTERS) for i in range(nr_letters)]
    password_list += [random.choice(NUM) for i in range(nr_numbers)]
    password_list += [random.choice(SYMBOLS) for i in range(nr_symbols)]
        
    random.shuffle(password_list)

    PASSWORD = "".join(password_list)
    
    password_input.delete(0,END)
    password_input.insert(0,PASSWORD)
    
    


# ----------------------- Save Password ------------------------------------------------------
def add_button_clicked():
    website = website_input.get()
    email = email_username_input.get()
    password = password_input.get()
    new_data = {
        website: { 
            "email" : email, 
            "password": password,
        }
    }
    
    
    if len(website)==0 or len(password)==0 or len(email)==0:
        messagebox.showwarning(title="Empty Field", message="Please fill all the Fields")
        return 
        
    if messagebox.askokcancel(f"{website}", f"These are the details entered: \nEmail: {email} \nPassword: {password} \nIt is ok to save?"):
        try:
            with open("data/passwords/acounts.json",mode="r") as file:
                # Read
                data = json.load(file)
                # Update
                data.update(new_data)
        except :
            data = new_data
        finally :
            with open("data/passwords/acounts.json",mode="w") as file:
                # Saving update data
                json.dump(data,file,indent=4)
                
            website_input.delete(0,END)
            password_input.delete(0,END)
            email_username_input.delete(0,END)
            messagebox.showinfo("Succes","Password Generated Succesfully")
            

# ----------------------- Search Website and Username Information ----------------------------
def search_button_clicked():
    website = website_input.get()
    try:
        with open("data/passwords/acounts.json",mode="r") as file:
            data = json.load(file)
            if website in data:
                email = data[website]['email']
                password = data[website]['password']
                messagebox.showinfo(website,f"Email: {email} \nPassword: {password}")
            else:
                messagebox.showinfo("Error",f"No details for {website} exists")      
                      
    except FileNotFoundError:
        with open("data/passwords/acounts.json",mode="w") as file:
            pass
        messagebox.showinfo("Error","No Data File Found")
    except json.decoder.JSONDecodeError:
        messagebox.showinfo("Error","There is not information in your database")
        


# ----------------------- UI Setup -----------------------------------------------------------

window = Tk()
icon = PhotoImage(file="data/image/icon_lock_small.png")
window.iconphoto(True, icon)
window.title("Password Manager")
window.config(padx=20  , pady=20, bg=DARK)

canvas = Canvas(width=305,height=405, bg=DARK, highlightthickness=0)
background = PhotoImage(file="data/image/icon_lock_small.png")
canvas.create_image(150,202,image = background)
# columnspan allow to spand a widget to another columns
canvas.grid(column=1, row=0,columnspan=2)

# Labels
website_label = Label(text="Website:", font=("Courier",14,"bold"),background=GRAY,fg=BLUE,width=15,highlightthickness=1,highlightbackground=PURPLE_STRONG)
website_label.grid(column=0,row=1)

email_username__label = Label(text="Email/Username:", font=("Courier",14,"bold"),background=GRAY,fg=BLUE,width=15,highlightthickness=1,highlightbackground=PURPLE_STRONG)
email_username__label.grid(column=0,row=2)

password_label = Label(text="Password:", font=("Courier",14,"bold"),background=GRAY,fg=BLUE,width=15,highlightthickness=1,highlightbackground=PURPLE_STRONG)
password_label.grid(column=0,row=3)

# Entries
website_input = Entry(width=31,fg=BLUE,bg=GRAY,highlightcolor=BLUE,highlightthickness=1)
website_input.grid(column=1,row=1, columnspan=1)
# start with this entry selected
website_input.focus()

email_username_input = Entry(width=50,fg=BLUE,bg=GRAY,highlightcolor=BLUE,highlightthickness=1,font=("Arial",8,"bold"))
email_username_input.grid(column=1,row=2, columnspan=2)

password_input = Entry(width=31,fg=BLUE,bg=GRAY,highlightcolor=BLUE,highlightthickness=1)
password_input.grid(column=1,row=3)

# Buttons
generator_password_button = Button(text="Generate Password", command=generator_password_button_clicked,foreground=BLUE,bg=GRAY)
generator_password_button.grid(column=2, row=3)

add_button = Button(text="Add", command=add_button_clicked, width=42,foreground=BLUE,bg=GRAY)
add_button.grid(column=1, row=4, columnspan=2)

search_button = Button(text="Search", command=search_button_clicked, width=14,bg=GRAY,fg=BLUE)
search_button.grid(column=2,row=1)


window.mainloop()