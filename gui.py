import sys
if __name__=='__main__':
    sys.exit()

import os, threading, subprocess, tkinter, config, lib

class main:
    def __init__(self):
        # Setup color
        self.white = lib.Color.white()
        self.black = lib.Color.black()
        self.blue = lib.Color.blue()
        
        self.get_token()
        
    def get_token(self):
        # Khởi tạo giao diện tkinter
        self.tk = tkinter.Tk()
        
        # Tên chương trình
        self.tk.title = "UpBox"
        
        # Kích thước cửa sổ tkinter hiện tại
        self.tk.geometry(self.center_screen(500, 45, self.tk))
        
        # Fixed size
        self.tk.resizable(False, False)
        
        # Label/Textbox/Button Token Github
        self.label_token = tkinter.Label(self.tk, text="Token Github:", font=('Arial', 8, 'bold'))
        self.label_token.place_forget()
        self.label_token.place(x=5,y=13)
        
        self.token = tkinter.StringVar(self.tk, value='# Token')
        self.entry_token = tkinter.Entry(self.tk, textvariable=self.token, show="", bd=1, width=56)
        self.entry_token.place_forget()
        self.entry_token.place(x=90,y=14)
        
        self.button_token = tkinter.Button(self.tk, text = "Check", command = lambda: self.check_token(self.token.get()), background=self.blue, foreground=self.white)
        self.button_token.place_forget()
        self.button_token.place(x=435,y=10)
        
        
        # Bind keyboard
        self.tk.bind('<Return>', lambda key_event: self.check_token(self.token.get()))
        
        # Lock current tkinter window
        # self.tk.attributes('-disabled', True)
        self.tk.mainloop()
        
    def main_program(self):
        self.tk = tkinter.Tk()
        self.tk.title = "UpBox"
        self.tk.geometry(self.center_screen(500, 45, self.tk))
        self.tk.resizable(False, False)
        
        self.tk.mainloop()
    
    def init_data(self):
        self.username = lib.get_username()
        print("Username: {}".format(self.username))
        self.storage_data = lib.load_data()
        print("Storage data: {}".format(self.storage_data))
        self.main_program()
    
    def check_token(self, token):
        if lib.check_token_github(token):
            self.tk.destroy()
            self.init_data()
        else:
            print('token error')
        
    def center_screen(self, w, h, ____):
        ws = ____.winfo_screenwidth()
        hs = ____.winfo_screenheight()
        x = (ws/2) - (int(w)/2)
        y = (hs/2) - (int(h)/2)
        return '%dx%d+%d+%d' % (int(w), int(h), x, y)
        
    def lock_tkinter(self, list=[]):
        for i in list:
            eval(i).config(state='disabled')