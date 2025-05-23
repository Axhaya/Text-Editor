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
class RailFence(Toplevel):
    def __init__(self, master:Tk, text:Text, dir:DIRECTION):
        super().__init__(master=master, name = "rail fence")
        self.text = text
        self.dir = dir

        self.title("Rail Fence " + str(dir)[str(dir).index(".")+1:] + " Input")
        self.geometry("350x100")

        self.frame = Frame(self)
        self.frame.pack(fill=BOTH, expand=YES)

        self.show_text = Label(self.frame, text="Input number of rails for " + str(dir)[str(dir).index(".")+1:])
        self.show_text.pack()

        self.entry = Entry(self.frame, validate="all", validatecommand=((self.register(self.callback)), '%P'))
        self.entry.pack()

        self.button = Button(self.frame, text="Confirm", command=self.confirm)
        self.button.pack()

        self.mainloop()
    
    def callback(self, p:chr): return str.isdigit(p) or p == ""

    def confirm(self):
        if self.entry.get() in ["", "0", "1"]:
            return
        
        if self.dir == DIRECTION.Encryption:
            new_text = self.encrypt(self.text.get("1.0", END), int(self.entry.get()) )
        elif self.dir == DIRECTION.Decryption:
            new_text = self.decrypt(self.text.get("1.0", END), int(self.entry.get()) )

        self.text.delete("1.0", END)
        self.text.insert(END, new_text)
        
        self.destroy()
    
    def space_insert(self, original:str, new:str) -> str:
        indexes = []
        for c in range(len(original)):
            if original[c] == " ":
                indexes.append(c)
        
        space_insert = list(new)
        for i in indexes:
            space_insert.insert(i," ")
        
        return "".join(space_insert)

    def encrypt(self, text:str, rails:int) -> str:
        fence = []

        for i in range(rails):
            fence.append([])
        
        rail:int = 0
        increment:int = 1
        for c in text:
            if c == " ":
                continue
            fence[rail].append(c)

            rail += increment
            if rail in [0, len(fence)-1]:
                increment *= -1

        new_text:str = ""
        for r in fence:
            new_text += "".join(str(x).replace("\n","") for x in r)
        
        return self.space_insert(text, new_text)

    def decrypt(self, text:str, amount_rails:int) -> str:
        clean_text = text.replace(" ","").replace("\n","")
        length = len(clean_text)

        fence = [0 for x in range(amount_rails)]

        # get rail char amount
        rail:int = 0
        increment:int = 1
        for i in range(length):
            fence[rail] += 1

            rail += increment
            if rail in [0, len(fence)-1]:
                increment *= -1

        text_blocks = {}
        last_amount_chars:int = 0
        for i in range(amount_rails):
           text_blocks[i] = clean_text[last_amount_chars:last_amount_chars+fence[i]]
           last_amount_chars += fence[i]
        
        new_text:str = ""

        rail = 0
        increment = 1
        for i in range(length):
            c:str = text_blocks[rail][0]
            new_text += c
            text_blocks[rail] = text_blocks[rail][1:]

            rail += increment
            if rail in [0, len(fence)-1]:
                increment *= -1
        
        return self.space_insert(text, new_text)

rail_fence_instance:RailFence = None

def create_rail_fence(parent:Tk, text:Text, dir:DIRECTION):
    global rail_fence_instance
    rail_fence_instance = RailFence(parent, text, dir)