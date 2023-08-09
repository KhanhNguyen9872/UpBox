import gui, terminal
if __name__ == '__main__':
    try:
        process = gui.main()
    except Exception as e:
        if "no display name" in str(e):
            print(">> Cannot detect Display! Program will start in Terminal!")
            process = terminal.main()
