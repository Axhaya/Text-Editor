from tkinter import *
from enum import Enum

DIRECTION = Enum('Type', [('Encryption', 1), ('Decryption', -1)])

# Caesar
alphabet = "abcdefghijklmnopqrstuvwxyz"
special_alphabet = "äöüß"

class Caesar(Toplevel):
    def __init__(self, parent:Tk, text:Text, dir:DIRECTION):
        super().__init__(master=parent, name="caesar")
        self.text = text
        self.direction = dir

        self.title("Caesar " + str(dir)[str(dir).index(".")+1:] + " Input")
        self.geometry("350x100")

        self.frame = Frame(self)
        self.frame.pack(fill=BOTH, expand=YES)

        self.show_text = Label(self.frame, text="Input desired Caesar distance for " + str(dir)[str(dir).index(".")+1:])
        self.show_text.pack()

        self.entry = Entry(self.frame, validate="all", validatecommand=((self.register(self.callback)), '%P'))
        self.entry.pack()

        self.button = Button(self.frame, text="Confirm", command=self.confirm)
        self.button.pack()

        self.mainloop()
    
    def callback(self, p:chr): return str.isdigit(p) or p == ""

    def confirm(self):
        input = int(self.entry.get()) if self.entry.get() != "" else 0
        distance = input % len(alphabet)

        text:str = self.text.get("1.0", END)
        self.text.delete("1.0", END)
        for char in text[:-1]:
            new_char = self.new_char(char, distance if self.direction == DIRECTION.Encryption else -distance)
            self.text.insert(END, new_char)
        
        self.destroy()
    
    def new_char(self, c:str, distance:int) -> chr:
        global alphabet
        global special_alphabet

        upper_case:bool = False
        if not c == c.lower():
            upper_case = True

        if c.lower() in alphabet:
            index = (alphabet.index(c.lower()) + distance) % len(alphabet)
            if upper_case:
                return alphabet[index].upper()
            return alphabet[index]
        elif c.lower() in special_alphabet:
            index = (special_alphabet.index(c.lower()) + distance) % len(special_alphabet)
            if upper_case:
                return special_alphabet[index].upper()
            return special_alphabet[index]
        return c

caesar_instance:Caesar = None

def create_caesar(parent:Tk, text:Text, dir:DIRECTION):
    global caesar_instance
    caesar_instance = Caesar(parent, text, dir)

# Rail Fence