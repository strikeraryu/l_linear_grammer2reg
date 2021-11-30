from tkinter import *
from llg2reg import llg2reg

root = Tk()
width, height = 500, 400
in_width = 40
root.title('Conversion')
root.geometry(f"{width}x{height}")

def display():
  INPUT = inputtxt.get("1.0", "end-1c")
  conv = llg2reg(INPUT)
  OUTPUT = conv.create_reg()[0]
  outtext.config(state=NORMAL)
  outtext.delete("insert linestart", "insert lineend")
  outtext.insert(END, OUTPUT)
  outtext.config(state=DISABLED)

def clear_text():
  outtext.config(state=NORMAL)
  outtext.delete("insert linestart", "insert lineend")
  inputtxt.delete("insert linestart", "insert lineend")
  outtext.config(state=DISABLED)

in_labl = Label(root, text = "Enter regular grammar")
in_labl.config(font = ("Courier", 11))

b1 = Button(root, text = "Convert", command = lambda :display())
b1.config(font = ("Courier", 11))

b2 = Button(root, text = "Exit", command = root.destroy)
b2.config(font = ("Courier", 11))

b3 = Button(root, text = "Clear", command = clear_text)
b3.config(font = ("Courier", 11))

inputtxt = Text(root, height = 5, width = in_width, bg = "light yellow")
inputtxt.config(font = ("Courier", 11))

out_labl=Label(root, text="Regular expression")
out_labl.config(font = ("Courier", 11))

outtext = Text(root, height=2, width=in_width, bg="light yellow")
outtext.config(font = ("Courier", 11))

in_labl.pack(pady=15)
inputtxt.pack()
out_labl.pack(pady=15)
outtext.pack()
b2.pack(pady=8, side=BOTTOM)
b1.pack(pady=10, side=BOTTOM)
b3.pack(pady=10, side=BOTTOM)

mainloop()