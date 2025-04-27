from tkinter import *
from tkinter import font
from PIL import Image, ImageTk
from functools import partial

# variables
window_width = 1000
window_height = 800

select_background = "black"
select_foreground = "white"

# window setup
root = Tk()
root.title("Text Editor")

root.geometry(str(window_width) + "x" + str(window_height))

frame = Frame(root)
frame.pack(fill=BOTH, expand=YES, pady=5)

text_scroll = Scrollbar(frame)
text_scroll.pack(side=RIGHT, fill=Y)
                                                  
text = Text(frame, width=100, height=25, selectbackground=select_background, 
            selectforeground=select_foreground, undo=True, yscrollcommand=text_scroll.set)
text.pack(fill=BOTH, expand=YES)

text_scroll.config(command=text.yview)

status = Label(root, text="Ready")
status.pack(fill=X, side=BOTTOM, ipady=5)

menu = Menu(root)
root.config(menu=menu)

## Menubar
import functions as f # import in this line to prevent unwanted second window
import encryptions as e

# Icon
root.iconbitmap(f.resource_path("Editor Icon.ico"))

# File Menu
file_menu = Menu(menu, tearoff=False)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command= lambda: f.new_file(root, text, status))
file_menu.add_command(label="Open", command= lambda: f.open_file(root, text, status))
file_menu.add_command(label="Save", command= lambda: f.save_file(root, text, status))
file_menu.add_command(label="Save As", command= lambda: f.save_as_file(root, text, status))
file_menu.add_separator()
file_menu.add_command(label="Exit")

# Edit Menu
edit_menu = Menu(menu, tearoff=False)
menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Undo", command=text.edit_undo, accelerator="Ctrl+Z")
edit_menu.add_command(label="Redo", command=text.edit_redo, accelerator="Ctrl+Y")
edit_menu.add_separator()
edit_menu.add_command(label="Cut", command= lambda: f.cut_text(root, text), accelerator="Ctrl+X") 
edit_menu.add_command(label="Copy", command= lambda: f.copy_text(root, text), accelerator="Ctrl+C")
edit_menu.add_command(label="Paste", command= lambda: f.paste_text(text), accelerator="Ctrl+V")
edit_menu.add_separator()
edit_menu.add_command(label="Delete", command= lambda: f.delete_text(text), accelerator="Del")

## Edit Bindings
def hotkey_cut(e): f.cut_text(root, text, e)
def hotkey_copy(e): f.copy_text(root, text, e)
def hotkey_paste(e): f.paste_text(text, e)

root.bind('<Control-Key-x>', hotkey_cut)
root.bind('<Control-Key-c>', hotkey_copy)
root.bind('<Control-Key-v>', hotkey_paste)

# Font Menu
font_menu = Menu(menu, tearoff=False)
menu.add_cascade(label="Font", menu=font_menu)

font_change_menu = Menu(font_menu, tearoff=False)
font_menu.add_cascade(label="Change", menu=font_change_menu)

font_change_menu.add_command(label="Arial", command= lambda: f.change_font(text, f.FONT.Arial))
font_change_menu.add_command(label="Comic Sans", command= lambda: f.change_font(text, f.FONT.Comic_Sans_MS))
font_change_menu.add_command(label="Courier New", command= lambda: f.change_font(text, f.FONT.Courier_New))
font_change_menu.add_command(label="Georgia", command= lambda: f.change_font(text, f.FONT.Georgia))
font_change_menu.add_command(label="Impact", command= lambda: f.change_font(text, f.FONT.Impact))
font_change_menu.add_command(label="Times New Roman", command= lambda: f.change_font(text, f.FONT.Times_New_Roman))

font_size_menu = Menu(font_menu, tearoff=False)
font_menu.add_cascade(label="Size", menu=font_size_menu)

font_size_menu.add_command(label="Custom", command= lambda: f.font_size_widget(text))

font_size_menu.add_separator()

for i in range(8, 48, 2):
    font_size_menu.add_command(label=i, command= partial(f.change_font, text, size=i))

font_menu.add_separator()
font_menu.add_command(label="Bold", command= lambda: f.bold_text(text), accelerator="Alt+B")
font_menu.add_command(label="Italic", command= lambda: f.italic_text(text), accelerator="Alt+I")

## Font Bindings
def hotkey_bold(e): f.bold_text(text)
def hotkey_italic(e): f.italic_text(text)

root.bind('<Alt-Key-b>', hotkey_bold)
root.bind('<Alt-Key-i>', hotkey_italic)

# Encryption Menu
encryption_menu = Menu(menu, tearoff=False)
menu.add_cascade(label="Encryption", menu=encryption_menu)

caesar_menu = Menu(encryption_menu, tearoff=False)
encryption_menu.add_cascade(label="Caesar", menu=caesar_menu)
caesar_menu.add_command(label="Encrypt", command= lambda: e.create_caesar(root, text, e.DIRECTION.Encryption))
caesar_menu.add_command(label="Decrypt", command= lambda: e.create_caesar(root, text, e.DIRECTION.Decryption))

rail_fence_menu = Menu(encryption_menu, tearoff=False)
encryption_menu.add_cascade(label="Rail Fence", menu=rail_fence_menu)
rail_fence_menu.add_command(label="Encrypt", command= lambda: e.create_rail_fence(root, text, e.DIRECTION.Encryption))
rail_fence_menu.add_command(label="Decrypt", command= lambda: e.create_rail_fence(root, text, e.DIRECTION.Decryption))

# basic function calls
f.change_font(text, mainloop=False)

root.mainloop()