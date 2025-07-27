import tkinter as tk
window = tk.Tk()

frame = tk.Frame(master=window)

text_entry = tk.Entry(master=window)
text_entry.insert(tk.END, "This is the end...")
text_entry.insert(tk.END, " No sira mis merda...")
text_entry.pack()

frame.pack()

window.mainloop()