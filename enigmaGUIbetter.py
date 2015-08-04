# TODO error handling!!! find out how to pop up an error message
# TODO make pretty

from tkinter import *
from tkinter import ttk
import enigma

root1 = Tk()  # root window
root1.title("Enigma!")


# make an Entry to take plaintext input, label it
plaintext_entry_label = ttk.Labelframe(root1, text="Input plaintext:")
plaintext_entry = Text(plaintext_entry_label, height=4, width=50)
plaintext_entry.grid(padx=3, pady=5)


# entry for displaying ciphertext output
ciphertext_entry_label = ttk.Labelframe(root1, text="Your ciphertext:")
ciphertext = ""
ciphertext_entry = Text(ciphertext_entry_label, height=4, width=50)
ciphertext_entry.insert(END, ciphertext)
ciphertext_entry.grid(padx=3, pady=5)


settings_frame = ttk.Labelframe(root1, text="Settings")
# dropdowns to select which scrambler to use
available_rotors = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'none']




pick = ttk.Labelframe(settings_frame, text='Select rotors')
pick.grid(column=0, row=0, pady=5)
select_rotor_1 = ttk.Combobox(pick, values=available_rotors, state='readonly', width=5)
select_rotor_1.current(0)  # set which one appears by default
select_rotor_1.grid(column=0, row=0, padx=3, pady=5)

select_rotor_2 = ttk.Combobox(pick, values=available_rotors, state='readonly', width=5)
select_rotor_2.current(8)
select_rotor_2.grid(column=1, row=0, padx=3, pady=5)

select_rotor_3 = ttk.Combobox(pick, values=available_rotors, state='readonly', width=5)
select_rotor_3.current(8)
select_rotor_3.grid(column=2, row=0, padx=3, pady=5)


# dropdown to select which reflector to use
available_reflectors = ["A", "B", "C", "B thin", "C thin"]
pick4 = ttk.Labelframe(settings_frame, text='Select reflector')
pick4.grid(column=0, row=2, pady=5)
select_reflector = ttk.Combobox(pick4, values=available_reflectors, state='readonly')
select_reflector.current(0)
select_reflector.grid(padx=3, pady=5)


# Entries to specify starting positions of rotors
set_pos = ttk.Labelframe(settings_frame, text='Set starting positions')
set_pos.grid(row=1, pady=5)
pos1 = ''
set1 = ttk.Entry(set_pos, textvariable=pos1, width=5)
set1.grid(column=0, row=1, padx=10, pady=5)
pos2 = ''
set2 = ttk.Entry(set_pos, textvariable=pos2, width=5)
set2.grid(column=1, row=1, padx=10, pady=5)
pos3 = ''
set3 = ttk.Entry(set_pos, textvariable=pos3, width=5)
set3.grid(column=2, row=1, padx=10, pady=5)


# entry to add plugboard settings
plugboard_entry_label = ttk.Labelframe(settings_frame, text="Set plugboard, eg a:z b:q")
plugboard_entry_label.grid(row=3, pady=5)
plugtext = ""
plugboard_entry_text = StringVar()
plugboard_entry_text.set(plugtext)
plugboard_entry = ttk.Entry(plugboard_entry_label, textvariable=plugboard_entry_text)
plugboard_entry.grid(padx=3, pady=2)


# bind encrypt button to function displaying ciphertext
def encrypt():
    # put the right scramblers and reflector in the machine
    scram_list = []
    scram_list.append(enigma.possible_scramblers[select_rotor_1.current()])
    scram_list.append(enigma.possible_scramblers[select_rotor_2.current()])
    scram_list.append(enigma.possible_scramblers[select_rotor_3.current()])
    refl = enigma.possible_reflectors[select_reflector.current()]

    # make a Plugboard from the entry
    plug = enigma.build_plugboard(plugboard_entry.get())

    # set the starting orientations of the rotors
    orient_list = [set1.get(), set2.get(), set3.get()]
    for i in range(len(scram_list)):
        rotor = scram_list[i]
        rotor.orientation = enigma.alphabet.find(orient_list[i])
        print(rotor.orientation)

    # define the machine to be used for encryption
    current_machine = enigma.Machine(scram_list, refl, plug)

    # do the encryption
    ciphertext = current_machine.encrypt(plaintext_entry.get(1.0, END))
    ciphertext_entry.insert(END, ciphertext)

encrypt_button = ttk.Button(root1, text="encrypt!", command=encrypt)


# make a button that closes the window
close_button = ttk.Button(root1, text='close', command=root1.quit)


# make the cursor appear in the plaintext entry box by default
plaintext_entry.focus()


# PACK ALL THE THINGS!
plaintext_entry_label.grid(column=0, row=0, pady=10, padx=10)
settings_frame.grid(column=1, row=0, rowspan=3, padx=10, pady=10, ipadx=10, ipady=10)
encrypt_button.grid(column=0, row=1, pady=10)
ciphertext_entry_label.grid(column=0, row=2, pady=10, padx=10)
close_button.grid(column=1, row=3, pady=10)


root1.mainloop()