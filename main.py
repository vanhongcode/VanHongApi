import customtkinter as ctk
import base64
import smtplib
import os
import requests
from random import randint
from tkinter import messagebox
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from tkinter import ttk
code = randint(111111, 222222)
def manage_apis():
    def generate_auth_key(username):
        name_bytes = username.encode('utf-8')
        base64_bytes = base64.b64encode(name_bytes)
        return base64_bytes.decode('utf-8')
    def generate_api_key(username):
        return username.encode('utf-8').hex()
    def load_apis():
        if not os.path.exists('api.txt'):
            return []
        with open('api.txt', 'r') as file:
            lines = file.readlines()
        apis = [line.strip().split(',') for line in lines]
        return apis
    def save_apis(apis):
        with open('api.txt', 'w') as file:
            for api in apis:
                file.write(','.join(api) + '\n')
    def add_api(username, email, job):
        authapi = generate_auth_key(username)
        apikey = generate_api_key(username)
        return [username, authapi, apikey, email, job]
    def show_add_api_window():
        add_window = ctk.CTkToplevel(gui)
        add_window.title('VanHongApiBusiness - Add API')
        add_window.geometry("400x200")
        add_window.resizable(False, False)
        frame = ctk.CTkFrame(add_window)
        frame.pack(pady=20, padx=20, fill='both', expand=True)
        ctk.CTkLabel(frame, text='Username', font=("Arial", 12)).grid(row=0, column=0, pady=5, padx=5, sticky='w')
        entry_username = ctk.CTkEntry(frame, width=270)
        entry_username.grid(row=0, column=1, pady=5, padx=5, sticky='w')
        ctk.CTkLabel(frame, text='Email', font=("Arial", 12)).grid(row=1, column=0, pady=5, padx=5, sticky='w')
        entry_email = ctk.CTkEntry(frame, width=270)
        entry_email.grid(row=1, column=1, pady=5, padx=5, sticky='w')
        ctk.CTkLabel(frame, text='Job', font=("Arial", 12)).grid(row=2, column=0, pady=5, padx=5, sticky='w')
        entry_job = ctk.CTkEntry(frame, width=270)
        entry_job.grid(row=2, column=1, pady=5, padx=5, sticky='w')
        def on_submit():
            username = entry_username.get()
            email = entry_email.get()
            job = entry_job.get()
            if username and email and job:
                new_api = add_api(username, email, job)
                apis.append(new_api)
                save_apis(apis)
                update_treeview()
                add_window.destroy()
            else:
                messagebox.showerror('Error', 'All fields are required')
        ctk.CTkButton(frame, text='Add API', command=on_submit).grid(row=3, columnspan=2, pady=10)
    def update_treeview():
        for row in treeview.get_children():
            treeview.delete(row)
        for api in apis:
            treeview.insert('', 'end', values=api)
    def show_api_details(event):
        item = treeview.selection()[0]
        api = treeview.item(item, "values")
        detail_window = ctk.CTkToplevel(gui)
        detail_window.title('VanHongApiBusiness - API Details')
        detail_window.geometry("400x300")
        detail_window.resizable(False, False)
        frame = ctk.CTkFrame(detail_window)
        frame.pack(pady=20, padx=20, fill='both', expand=True)
        labels = ['Username', 'AuthAPI', 'APIKey', 'Email', 'Job']
        for i, label in enumerate(labels):
            ctk.CTkLabel(frame, text=f'{label}:', font=("Arial", 12)).grid(row=i, column=0, pady=5, padx=5, sticky='w')
            entry = ctk.CTkEntry(frame, width=270)
            entry.grid(row=i, column=1, pady=5, padx=5, sticky='w')
            entry.insert(0, api[i])
            entry.configure(state='readonly') 
    gui = ctk.CTk()
    gui.title('VanHongApiBusiness - Api Manager')
    screen_width = gui.winfo_screenwidth()
    screen_height = gui.winfo_screenheight()
    gui.geometry(f'{screen_width}x{screen_height}')
    apis = load_apis()
    columns = ('Username', 'AuthAPI', 'APIKey', 'Email', 'Job')
    treeview = ttk.Treeview(gui, columns=columns, show='headings')
    for col in columns:
        treeview.heading(col, text=col)
        treeview.column(col, width=100)
    vsb = ttk.Scrollbar(gui, orient="vertical", command=treeview.yview)
    vsb.pack(side='right', fill='y')
    treeview.configure(yscrollcommand=vsb.set)
    treeview.pack(fill='both', expand=True, pady=20)
    treeview.bind("<Double-1>", show_api_details)
    ctk.CTkButton(gui, text='Add API', command=show_add_api_window).pack(pady=10)
    update_treeview()
    gui.mainloop()
def on_submit():
    username = entry_username.get()
    apikey = entry_apikey.get()
    email = entry_email.get()
    api = doc_api(apikey)
    if api != username:
        messagebox.showerror('VanHongApiBusiness', 'API key or Username is incorrect')
        return
    if email == "":
        messagebox.showerror('VanHongApiBusiness', 'Please enter your email')
        return
    send_code(email)
    nhap_code()
def doc_api(api):
    try:
        apis = api.encode('utf-8')
        name_bytes = base64.b64decode(apis)
        name = name_bytes.decode('utf-8')
        return name
    except Exception as e:
        messagebox.showerror('VanHongApiBusiness', 'Invalid API key')
        return None
def send_code(receiver_email):
    sender_email = "SMTP Username"
    sender_password = "SMTP Password"
    username = entry_username.get()
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "VanHongApiBusiness"
    body = f"""<h2>Xin chào {receiver_email},</h2><br>
    <h4>Chúng tôi là VanHongApiBusiness.</h4><br>
    <h4>Mã đăng nhập cho tài khoảng <span font-size:15px;>{username}</span> là </h4><br>
    <span style="background-color:yellow; font-size:35px;">{code}</span><br>
    <h4>Đừng chia sẻ mã này cho bất kỳ ai vì có thể mất tài khoảng.</h4><br>
    <h3>Gửi từ VanHongApi</h3><br>
    <h2>TRÂN TRỌNG ./.</H2>"""
    message.attach(MIMEText(body, "html"))
    image_url = "https://media.discordapp.net/attachments/1228716682059710615/1243407569847058432/learn.png?ex=66515d0a&is=66500b8a&hm=a38f00ffb747930c08da6bed2bf00bd0cbc4f4a3c23ffa5613114776a13dd6cd&=&format=webp&quality=lossless"
    image_data = requests.get(image_url).content
    image = MIMEImage(image_data)
    image.add_header("Content-Disposition", "attachment", filename="learn.png") 
    message.attach(image)
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
        print("[VANHONGAPI] Verification code sent to your email")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
def nhap_code():
    Screen.withdraw()
    verification_screen.deiconify()
def xulima():
    codenhap = codeap.get()
    if codenhap != str(code):
        messagebox.showerror('VanHongApiBusiness', 'Incorrect verification code')
        return
    if codenhap == str(code):
        messagebox.showinfo('VanHongApiBusiness','Enter code successfully')
        manage_apis()
        verification_screen.withdraw()
Screen = ctk.CTk()
Screen.title('VanHongApiBusiness - Login')
Screen.geometry('300x250')
Screen.resizable(False, False)
entry_username = ctk.CTkEntry(Screen, placeholder_text='Username')
entry_username.pack(pady=5)
entry_apikey = ctk.CTkEntry(Screen, placeholder_text='AuthApi')
entry_apikey.pack(pady=5)
entry_email = ctk.CTkEntry(Screen, placeholder_text='Email')
entry_email.pack(pady=5)
ctk.CTkButton(Screen, text='Login', fg_color='#0000FF', command=on_submit).pack(pady=10)
verification_screen = ctk.CTk()
verification_screen.title('VanHongApiBusiness - Verification')
verification_screen.geometry('300x100')
verification_screen.withdraw()
ctk.CTkLabel(verification_screen, text='we sent the code to your mail\nPlease enter the code in the box below').pack()
codeap = ctk.CTkEntry(verification_screen)
codeap.pack(pady=5)
ctk.CTkButton(verification_screen, text='Verify', command=xulima).pack(pady=5)
Screen.mainloop()
