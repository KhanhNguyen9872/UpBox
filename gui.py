import sys
if __name__=='__main__':
    sys.exit()

import tkinter, lib
from tkinter import filedialog
from tkinter import scrolledtext

try:
    import config
except (ImportError, ModuleNotFoundError):
    open("config.py", "w").write()
    import config

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
        
    def get_items(self, event):
        selected_indices = self.list_file.curselection()
        return [self.list_file.get(idx) for idx in selected_indices]
    
    def on_select(self, event):
        selected_items = self.get_items(event)
        self.selected_data.set(", ".join(selected_items))
        return
        
    def view_file(self):
        for item in self.selected_data.get().split(","):
            item = "-".join(item.split("-")[1:])[1:]
            if item:
                lib.threading.Thread(target=self.showTextBox, args=(item,)).start()
        self.reload_listfile()
        return

    def open_file(self):
        for item in self.selected_data.get().split(","):
            item = "-".join(item.split("-")[1:])[1:]
            if item:
                lib.threading.Thread(target=self.openFileCMD, args=(item,)).start()
        self.reload_listfile()
        return
    
    def choose_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            return folder_path
        else:
            return False
        
    def choose_file(self):
        file = filedialog.askopenfilename()
        if file:
            return file
        else:
            return False
        
    def upload_progress(self, file):
        if file:
            file_name = "/".join(file.split("\\")).split("/")[-1]
            lib.upload_file_release(file)
            lib.update_data("add", file_name)
            self.reload_listfile()
        return
        
    def upload_file(self):
        file = self.choose_file()
        if (file != False):
            lib.threading.Thread(target=self.upload_progress, args=(file, )).start()
        return
    
    def delete_file(self):
        listFile = self.selected_data.get().split(",")
        for item in listFile:
            item = "-".join(item.split("-")[1:])[1:]
            if item:
                lib.remove_file_release(item)
                lib.update_data('del', item)
                self.reload_listfile()
        
    def download_file(self):
        path = self.choose_folder()
        if (path != False):
            fullItems = self.selected_data.get().split(",")
            for item in fullItems:
                item = "-".join(item.split("-")[1:])[1:]
                if item:
                    data = lib.get_data_from_release(item)
                    if (data[0] == 404):
                        return
                    open("{path}/{item}".format(path = path, item = item), "wb").write(data[1])
        self.reload_listfile()
        return

    def openFileCMD(self, item):
        data = lib.get_data_from_release(item)
        if (data[0] == 404):
            return
        
        path = "{tmp}\\{folder}".format(tmp = lib.tmp_path, folder = lib.random_str(48))
        lib.os.mkdir(path)
        open("{path}\\{item}".format(path = path, item = item), 'wb').write(data[1])
        lib.os.system("\"{path}\\{item}\"".format(path = path, item = item))
        lib.time.sleep(5)
        lib.shutil.rmtree(path)
        return
            
    def showTextBox(self, item):
        data = lib.get_data_from_release(item)
        if (data[0] == 404):
            data[1] == "Network ERROR!"
        
        root = tkinter.Tk()
        root.title(item)

        text_area = scrolledtext.ScrolledText(root, wrap=tkinter.WORD, width=100, height=30)
        text_area.pack(expand=True, fill="both")

        scrollbar = tkinter.Scrollbar(root, command=text_area.yview)
        scrollbar.pack(side="right", fill="y")

        text_area.config(yscrollcommand=scrollbar.set)
        text_area.insert(tkinter.END, data[1])
        text_area.config(state='disabled')

        root.mainloop()
        
    def reload_listfile(self):
        self.list_file.delete(0, tkinter.END)
        lst = lib.get_list_file()
        lib.debug(lib.get_data())
        for name in lst:
            print(name)
            print(lst[name])
            if(lst[name] == "file"):
                name = str(round(int(lib.json.loads(lib.get_data()['file'][name])['info']['0'].split("|")[2]) / 1024, 2)) + " kb - " + name
                self.list_file.insert(tkinter.END, name)
        return
        
    def main_program(self):
        self.tk = tkinter.Tk()
        self.tk.title(lib.program_name())
        self.tk.geometry(self.center_screen(800, 480, self.tk))
        self.tk.resizable(False, False)
        
        self.list_file = tkinter.Listbox(self.tk, selectmode=tkinter.MULTIPLE)
        self.list_file.pack(padx=10, pady=10, fill=tkinter.BOTH, expand=True)
        
        self.reload_listfile()
    
        self.list_file.bind("<<ListboxSelect>>", self.on_select)

        # Open Button
        open_button = tkinter.Button(self.tk, text="Open", command=self.open_file)
        open_button.pack(side=tkinter.LEFT, padx=10, pady=10)
        
        # View Button
        view_button = tkinter.Button(self.tk, text="View as text", command=self.view_file)
        view_button.pack(side=tkinter.LEFT, padx=10, pady=10)

        # Download Button
        download_button = tkinter.Button(self.tk, text="Download", command=self.download_file)
        download_button.pack(side=tkinter.LEFT, padx=10, pady=10)
        
        # Upload Button
        upload_button = tkinter.Button(self.tk, text="Upload", command=self.upload_file)
        upload_button.pack(side=tkinter.LEFT, padx=10, pady=10)
        
        # Delete Button
        delete_button = tkinter.Button(self.tk, text="Delete", command=self.delete_file)
        delete_button.pack(side=tkinter.LEFT, padx=10, pady=10)

        # Reload Button
        reload_button = tkinter.Button(self.tk, text="Reload", command=self.reload_listfile)
        reload_button.pack(side=tkinter.LEFT, padx=10, pady=10)
        
        self.tk.mainloop()
    
    def init_data(self):
        self.username = lib.get_username()
        self.storage_data = lib.load_data()
        self.selected_data = tkinter.StringVar()
        return
        
    def lock_obj(self, lst=[]):
        if not str(type(lst)) == "<class 'list'>":
            return
        for i in lst:
            i.config(state='disabled')
        while not self.is_done:
            lib.time.sleep(0.01)
        try:
            for i in lst:
                i.config(state='normal')
        except:
            pass
        return
        
    def check_token_thread(self):
        self.is_done = False
        lib.threading.Thread(target=self.lock_obj, args=([self.entry_token, self.button_token],)).start()
        lib.threading.Thread(target=self.check_token).start()
        return
    
    def check_token(self):
        self.textbox.write('>> Login account....')
        #lib.time.sleep(1)
        var = lib.check_token_github(self.token.get())
        if var == True:
            self.textbox.write(">> Getting account information....")
            #lib.time.sleep(1)
            self.init_data()
            self.tk.quit()
            self.is_done = True
            del self.textbox
        elif var == False:
            self.textbox.write('>> Token ERROR!')
            self.is_done = True
            return False
        else:
            self.textbox.write('>> Token ERROR! Message: {message}'.format(message = var))
            self.is_done = True
            return False
        return True
        
    def center_screen(self, w, h, ____):
        ws = ____.winfo_screenwidth()
        hs = ____.winfo_screenheight()
        x = (ws/2) - (int(w)/2)
        y = (hs/2) - (int(h)/2)
        return '%dx%d+%d+%d' % (int(w), int(h), x, y)
        