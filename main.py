import gui, terminal
if __name__ == '__main__':
    try:
        process = gui.main()
    except KeyboardInterrupt:
        print("Cannot detect Display! Program will start in Terminal")
        process = terminal.main()
