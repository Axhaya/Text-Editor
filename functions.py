from tkinter import *
from tkinter import filedialog
from tkinter import font
from enum import Enum
import json

# warnings

# widget functions
def set_status(root:Tk, status:Label, text:str, prefix:str="", suffix:str=""):
    slice_point = -1
    for c in range(len(text)):
        if text[c] == "/":
            slice_point = c
    name = text[slice_point+1:]

    root.title(name)
    status.config(text=prefix + text + suffix)

# file functions
current_file_path = False

def new_file(root:Tk, text:Text, status:Label = Label()):
    root.title("New File")
    text.delete("1.0", END)
    status.config(text="New File")

    global current_file_path
    current_file_path = False

def open_file(root:Tk, text:Text, status:Label = Label()):
    file_path = filedialog.askopenfilename(initialdir="", title="Open File", filetypes=(("Text Files", "*.txt"),
                                                                                        ("Python Files", "*.py"),
                                                                                        ("Python Files", "*.pyw"),
                                                                                        ("All Files", "*.*")))
    global current_file_path
    if file_path:
        current_file_path = file_path

    set_status(root,status,file_path)

    file = open(file_path, 'r')
    content = file.read()

    text.delete("1.0", END)
    text.insert(END, content)

    file.close()

def save_file(root:Tk, text:Text, status:Label = Label()):
    global current_file_path
    if not current_file_path:
        save_as_file(root, text, status)
    else:
        set_status(root, status, current_file_path, "Saved:")

        file = open(current_file_path, 'w')
        file.write(text.get(1.0, END))

        file.close()

def save_as_file(root:Tk, text:Text, status:Label = Label()):
    file_path = filedialog.asksaveasfilename(defaultextension=".*", initialdir="", title="Save File", filetypes=(("Text Files", "*.txt"),
                                                                                                                ("Python Files", "*.py"),
                                                                                                                ("Python Files", "*.pyw"),
                                                                                                                ("All Files", "*.*")))
    if file_path:
        set_status(root, status, file_path, "Saved as:")

        file = open(file_path, 'w')
        file.write(text.get(1.0, END))

        file.close()

# edit functions
selected_text = ""
def cut_text(root:Tk, text:Text, e = False):
    global selected_text
    if e:
        selected_text = root.clipboard_get()
    elif text.tag_ranges(SEL):
        selected_text = text.selection_get()
        delete_text(text)

        root.clipboard_clear()
        root.clipboard_append(selected_text)

def copy_text(root:Tk, text:Text, e = False):
    global selected_text
    if e:
        selected_text = root.clipboard_get()
    elif text.tag_ranges(SEL):
        selected_text = text.selection_get()

        root.clipboard_clear()
        root.clipboard_append(selected_text)

def paste_text(text:Text, e = False):
    global selected_text
    if selected_text == "" or e:
        return
    delete_text(text)
    text.insert(text.index(INSERT),selected_text)

def delete_text(text:Text):
    if text.tag_ranges(SEL):
        text.delete("sel.first", "sel.last")

# font functions
FONT = Enum('Name', [('Arial', 1), ('Comic_Sans_MS', 2), ('Courier_New', 3), ('Georgia', 4), ('Impact', 5), ('Times_New_Roman', 6)])

def save_font(font:FONT, size:int):
    font_preferences = {
        "font_type": str(font),
        "font_size": size,
    }
    with open('preferences.json', 'w') as file:
        json.dump(font_preferences, file)

def load_font_type() -> FONT:
    with open('preferences.json', 'r') as file:
        loaded = json.load(file)
    return FONT[str(loaded["font_type"])[str(loaded["font_type"]).index(".")+1:]]

def load_font_size() -> int:
    with open('preferences.json', 'r') as file:
        loaded = json.load(file)
    return loaded["font_size"]

def change_font(text:Text, f:FONT = None, size:int = 0, mainloop:bool = True):
    if f == None: f = load_font_type()
    if size == 0: size = load_font_size()

    name = str(f)[str(f).index(".")+1:].replace("_", " ")

    save_font(f, size)

    cf = font.Font(family=name, size=size)
    text.configure(font=cf)

    text.tag_remove("bold", "1.0", END)
    text.tag_remove("italic", "1.0", END)

    if mainloop: text.master.mainloop()

def bold_text(text:Text):
    bold_font = font.Font(text, text.cget("font"))
    bold_font.configure(weight="bold")

    text.tag_configure("bold", font=bold_font)

    if "bold" in text.tag_names("sel.first"):
        text.tag_remove("bold", "sel.first", "sel.last")
    else:
        text.tag_add("bold", "sel.first", "sel.last")

def italic_text(text:Text):
    italic_font = font.Font(text, text.cget("font"))
    italic_font.configure(slant="italic")

    text.tag_configure("italic", font=italic_font)

    if "italic" in text.tag_names("sel.first"):
        text.tag_remove("italic", "sel.first", "sel.last")
    else:
        text.tag_add("italic", "sel.first", "sel.last")
    