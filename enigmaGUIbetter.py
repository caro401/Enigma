# TODO error handling!!!

from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import enigma

root1 = Tk()  # root window
root1.title("Enigma!")


# make an Entry to take plaintext input, label it
plaintext_entry_label = ttk.Labelframe(root1, text="Input plaintext:", padding="10 10 10 10")
plaintext_entry = Text(plaintext_entry_label, height=4, width=50)
plaintext_entry.focus()  # make the cursor appear in the plaintext entry box by default


# entry for displaying ciphertext output
ciphertext_entry_label = ttk.Labelframe(root1, text="Your ciphertext:", padding="10 10 10 10")
ciphertext = ""
ciphertext_entry = Text(ciphertext_entry_label, height=4, width=50)
ciphertext_entry.insert(END, ciphertext)


settings_frame = ttk.Labelframe(root1, text="Settings", padding="10 10 10 10")
# dropdowns to select which scrambler to use
available_rotors = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'none']
pick = ttk.Labelframe(settings_frame, text='Select rotors', padding="5 5 5 5")
select_rotor_1 = ttk.Combobox(pick, values=available_rotors, state='readonly', width=5)
select_rotor_1.current(0)  # set which one appears by default

select_rotor_2 = ttk.Combobox(pick, values=available_rotors, state='readonly', width=5)
select_rotor_2.current(8)

select_rotor_3 = ttk.Combobox(pick, values=available_rotors, state='readonly', width=5)
select_rotor_3.current(8)


# dropdown to select which reflector to use
available_reflectors = ["A", "B", "C", "B thin", "C thin"]
pick4 = ttk.Labelframe(settings_frame, text='Select reflector')
select_reflector = ttk.Combobox(pick4, values=available_reflectors, state='readonly', width=5)
select_reflector.current(0)


# Entries to specify starting positions of rotors
set_pos = ttk.Labelframe(settings_frame, text='Set starting positions')
pos1 = ''
set1 = ttk.Entry(set_pos, textvariable=pos1, width=5)
pos2 = ''
set2 = ttk.Entry(set_pos, textvariable=pos2, width=5)
pos3 = ''
set3 = ttk.Entry(set_pos, textvariable=pos3, width=5)


# entry to add plugboard settings
plugboard_entry_label = ttk.Labelframe(settings_frame, text="Set plugboard, eg a:z b:q")
plugtext = ""
plugboard_entry_text = StringVar()
plugboard_entry_text.set(plugtext)
plugboard_entry = ttk.Entry(plugboard_entry_label, textvariable=plugboard_entry_text)


# function to build plugboard
def build_plugboard(map_string):
    length = len(enigma.alphabet)
    new_plug_map = [0] * length
    if len(map_string) != 0:
        pairs = map_string.split()
        for pair in pairs:
            if not (pair[0].isalpha() and pair[2].isalpha() and pair[1] == ":" and len(pair) == 3):
                tkinter.messagebox.showerror("oh no!", "This is not a valid plugboard:\n invalid entry of settings")
        for pair in pairs:
            index1 = enigma.alphabet.find(pair[0])
            index2 = enigma.alphabet.find(pair[2])
            new_plug_map[index1] = (index2 - index1) % length
            new_plug_map[index2] = (index1 - index2) % length
        new_plug = enigma.Plugboard(new_plug_map)
        return new_plug
    else:
        new_plug = enigma.Plugboard(new_plug_map)
        return new_plug


# bind encrypt button to function displaying ciphertext
def encrypt():
    plain = plaintext_entry.get(1.0, END).strip()
    if not plain.isalpha():
        tkinter.messagebox.showerror("oh no!", "Invalid plaintext")

    # put the right scramblers and reflector in the machine
    scram_list = [
        enigma.possible_scramblers[select_rotor_1.current()],
        enigma.possible_scramblers[select_rotor_2.current()],
        enigma.possible_scramblers[select_rotor_3.current()]
    ]
    refl = enigma.possible_reflectors[select_reflector.current()]

    # make a Plugboard from the entry
    plug = build_plugboard(plugboard_entry.get())
    if not plug.check_mapping():
        tkinter.messagebox.showerror("oh no!", "This is not a valid plugboard:\n not mapped in pairs")

    # set the starting orientations of the rotors
    orient_list = [set1.get(), set2.get(), set3.get()]
    for i in orient_list:
        if len(i) > 1 or not (i.isalpha() or i == ""):
            tkinter.messagebox.showerror("oh no!", "Invalid setting for starting position:\n "
                                                   "must be a single letter or blank")
        break
    for i in range(len(scram_list)):
        rotor = scram_list[i]
        rotor.orientation = enigma.alphabet.find(orient_list[i])

    # define the machine to be used for encryption
    current_machine = enigma.Machine(scram_list, refl, plug)

    # do the encryption
    cipher = current_machine.encrypt(plain)
    ciphertext_entry.replace(1.0, END, cipher)

encrypt_button = ttk.Button(root1, text="encrypt!", command=encrypt)


# make a button that closes the window
close_button = ttk.Button(root1, text='close', command=root1.quit)


# PACK ALL THE THINGS!
plaintext_entry.grid(in_=plaintext_entry_label)
plaintext_entry_label.grid(column=0, row=0, padx=10, pady=10)

encrypt_button.grid(column=0, row=1)

ciphertext_entry.grid(in_=ciphertext_entry_label)
ciphertext_entry_label.grid(column=0, row=2, padx=10, pady=10)


settings_frame.grid(column=1, row=0, rowspan=3, padx=10, pady=10)
pick.grid(in_=settings_frame, column=0, row=0, padx=5, pady=5)
select_rotor_1.grid(in_=pick, padx=5, pady=5)
select_rotor_2.grid(in_=pick, column=1, row=0, padx=5, pady=5)
select_rotor_3.grid(in_=pick, column=2, row=0,  padx=5, pady=5)

set_pos.grid(in_=settings_frame, column=0, row=1, padx=5, pady=5)
set1.grid(in_=set_pos, column=0, row=1, padx=5, pady=5)
set2.grid(in_=set_pos, column=1, row=1, padx=5, pady=5)
set3.grid(in_=set_pos, column=2, row=1, padx=5, pady=5)

pick4.grid(in_=settings_frame, column=0, row=2, padx=5, pady=5)
select_reflector.grid(in_=pick4, padx=5, pady=5)

plugboard_entry_label.grid(in_=settings_frame, row=3, padx=5, pady=5)
plugboard_entry.grid(in_=plugboard_entry_label, padx=5, pady=5)


close_button.grid(column=1, row=3, padx=10, pady=10)


root1.mainloop()