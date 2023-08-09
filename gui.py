import sys
if __name__=='__main__':
    sys.exit()

import os, threading, subprocess, tkinter, config, lib, time

class TextBox:
    def __init__(self, textbox):
        self.textbox = textbox
    def write(self, text):
        self.textbox.config(state = 'normal')
        self.textbox.delete(1.0,'end')
        self.textbox.insert(1.0, text)
        self.textbox.config(state = 'disabled')
    def append(self, text):
        self.textbox.config(state = 'normal')
        self.textbox.insert('end', text)
        self.textbox.config(state = 'disabled')
        self.textbox.see('end')

class main:
    def __init__(self):
        # Setup Color
        self.Color = lib.Color()
        
        # Start program
        self.get_token()
        self.tk.destroy()
        self.main_program()
        
    def get_token(self):
        self.tk = tkinter.Tk()
        self.tk.title(lib.program_name())
        self.tk.geometry(self.center_screen(500, 70, self.tk))
        self.tk.resizable(False, False)
        
        # Label/Textbox/Button Token Github
        label_token = tkinter.Label(self.tk, text="Token Github:", font=('Arial', 8, 'bold'))
        label_token.place_forget()
        label_token.place(x=5,y=13)
        
        self.token = tkinter.StringVar(self.tk, value='# Token')
        self.entry_token = tkinter.Entry(self.tk, textvariable=self.token, show="", bd=1, width=56)
        self.entry_token.place_forget()
        self.entry_token.place(x=90,y=14)
        
        self.button_token = tkinter.Button(self.tk, text = "Login", command = lambda: self.check_token_thread(), background=self.Color.getcolor('blue'), foreground=self.Color.getcolor('white'))
        self.button_token.place_forget()
        self.button_token.place(x=440,y=10)
        
        # Status
        label_token = tkinter.Label(self.tk, text="Status:", font=('Arial', 8, 'bold'))
        label_token.place_forget()
        label_token.place(x=5,y=41)
        
        textbox_token = tkinter.Text(self.tk, font=("Arial", 10), width = 61, height=1)
        textbox_token.config(state='disabled')
        textbox_token.place_forget()
        textbox_token.place(x=53, y=42)
        
        
        # Bind keyboard
        self.tk.bind('<Return>', lambda key_event: self.check_token_thread())
        
        # assign
        self.textbox = TextBox(textbox_token)
        self.textbox.write("Please input Token Github!")
        
        # Lock current tkinter window
        # self.tk.attributes('-disabled', True)
        self.tk.mainloop()
        
    def main_program(self):
        ## main
        self.tk = tkinter.Tk()
        self.tk.title(lib.program_name())
        self.tk.geometry(self.center_screen(800, 480, self.tk))
        self.tk.resizable(False, False)
        
        self.tk.mainloop()
    
    def init_data(self):
        self.username = lib.get_username()
        self.storage_data = lib.load_data()
        return
        
    def lock_obj(self, lst=[]):
        if not str(type(lst)) == "<class 'list'>":
            return
        for i in lst:
            i.config(state='disabled')
        while not self.is_done:
            time.sleep(0.01)
        try:
            for i in lst:
                i.config(state='normal')
        except:
            pass
        return
        
    def check_token_thread(self):
        self.is_done = False
        threading.Thread(target=self.lock_obj, args=([self.entry_token, self.button_token],)).start()
        threading.Thread(target=self.check_token).start()
        return
    
    def check_token(self):
        self.textbox.write('>> Login account....')
        #time.sleep(1)
        if lib.check_token_github(self.token.get()):
            self.textbox.write(">> Getting account information....")
            #time.sleep(1)
            self.init_data()
            self.tk.quit()
            self.is_done = True
            del self.textbox
        else:
            self.textbox.write('>> Token ERROR!')
            self.is_done = True
            return False
        return True
        
    def center_screen(self, w, h, ____):
        ws = ____.winfo_screenwidth()
        hs = ____.winfo_screenheight()
        x = (ws/2) - (int(w)/2)
        y = (hs/2) - (int(h)/2)
        return '%dx%d+%d+%d' % (int(w), int(h), x, y)
        