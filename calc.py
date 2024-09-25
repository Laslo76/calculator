import tkinter as tk
from calc_top_window import TopWindow as TWin


def main():
    root = tk.Tk()
    root.iconbitmap("./icon/icon.ico")
    TWin(root)
    root.mainloop()


if __name__ == '__main__':
    main()
