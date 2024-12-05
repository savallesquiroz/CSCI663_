import client as c
import server as s
import gui
import tkinter as tk
import sys
import os
import threading

root = tk.Tk()
app = gui.CryptoGUI(root)

def main():
    t = threading.Thread(target=timing)
    t.start()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

def timing():
    if sys.argv[1] == "client":
        c.start_client(app)
    elif sys.argv[1] == "server":
        s.start_server(app)
    else:
        pass

def on_closing():
    root.destroy()
    os._exit(0)

if __name__ == "__main__":
    main()
