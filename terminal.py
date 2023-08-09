import sys
if __name__=='__main__':
    sys.exit()
import lib, os

class main:
    def __init__(self):
        os.system("title {}".format(lib.program_name())) if os.name == 'nt' else sys.stdout.write("\x1b]2;{}\x07".format(lib.program_name()))
        
        # Setup Color
        self.Color = lib.Color(False)
        
        self.get_token()
    
    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def pause_terminal(self, message=""):
        input(message)
    
    def owrite(self, message="", color=""):
        if not color:
            color = 'white'
        print("{}{}{}".format(self.Color.getcolor(color), message, self.Color.getcolor('white')))
    
    def iwrite(self, message="", color="", color2=""):
        if not color:
            color = 'white'
        if not color2:
            color = 'white'
        return input("{}{}{}".format(self.Color.getcolor(color), message, self.Color.getcolor(color2)))
    
    def get_token(self):
        while 1:
            self.token = str(self.iwrite(">> Token Github: ", 'violet', 'yellow'))
            if self.check_token():
                break
        self.main_program()
    
    def init_data(self):
        self.owrite(">> Getting account information....", 'blue')
        self.username = lib.get_username()
        self.storage_data = lib.load_data()
        
    def check_token(self):
        self.owrite(">> Login....", 'green')
        if lib.check_token_github(self.token):
            self.init_data()
            return True
        else:
            self.owrite("token error", 'red')
            return False
        
    def main_program(self):
        self.clear_terminal()
        print('main program')