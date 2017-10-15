import tkinter as tk
from tkinter import messagebox
from tkinter.constants import *
import pony_vk
from pony_vk import errors


def center(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))


class AuthWindow:
    def __init__(self):
        self.auth_window = tk.Tk()
        self.auth_window.title("VK auth")
        self.auth_window.wm_attributes("-topmost" , -1)
        tk.Label(self.auth_window, text="Email:").pack()
        self.email = tk.Entry(self.auth_window, text="")
        self.email.pack()
        tk.Label(self.auth_window, text="Password:").pack()
        self.password = tk.Entry(self.auth_window, text="", show="*")
        self.password.pack()
        tk.Label(self.auth_window, text="Code(if necessary):").pack()
        self.code = tk.Entry(self.auth_window, text="")
        self.code.pack()
        self.login_button = tk.Button(self.auth_window, text="Auth", command=self.auth).pack()
        self.auth_window.mainloop()

    def auth(self):

        try:
            client = pony_vk.Client(login=self.email.get(), password=self.password.get(), code=self.code.get())
        except errors.CodeRequiredError as error:
            messagebox.showinfo("Code is required")
        except errors.VKError as error:
            messagebox.showinfo(error.json['error_description'])


AuthWindow()
