import tkinter as tk

def home_screen():
    pass

def on_key(event):
    print(f'Key pressed: {event.char}')
    if event.char == 'q':
        quit()


if __name__ == '__main__':
    root = tk.Tk()
    root.bind('<Key>', on_key)
    root.mainloop()
    home_screen()
