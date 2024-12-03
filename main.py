import client as c
import server as s
import gui
import tkinter as tk
import sys
import threading

root = tk.Tk()
app = gui.CryptoGUI(root)

def main():
    t = threading.Thread(target=timing)
    t.start()
    root.mainloop()

def timing():
    if sys.argv[1] == "client":
        c.start_client(app)
    elif sys.argv[1] == "server":
        s.start_server(app)
    else:
        pass

if __name__ == "__main__":
    main()
