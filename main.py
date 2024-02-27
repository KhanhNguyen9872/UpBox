if __name__ == '__main__':
    try:
        process = __import__("gui").main
    except Exception as e:
        if "no display name" in str(e):
            print(">> Cannot detect Display! Program will start in Terminal!")
            process = __import__("terminal").main
    
    try:
        process()
    except __import__('_tkinter').TclError:
        pass
# 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