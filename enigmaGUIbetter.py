# TODO error handling!!! find out how to pop up an error message

from tkinter import *
from tkinter import ttk
import enigma

root1 = Tk()  # root window
root1.title("Better Encryptor!")


# make an Entry to take plaintext input, label it
plaintext_entry_label = ttk.Labelframe(root1, text="Input plaintext:")
plaintext_entry = Text(plaintext_entry_label, height=4, width=50)
plaintext_entry.pack()


# entry for displaying ciphertext output
ciphertext_entry_label = ttk.Labelframe(root1, text="Your ciphertext:")
ciphertext = ""
ciphertext_entry = Text(ciphertext_entry_label, height=4, width=50)
ciphertext_entry.insert(END, ciphertext)
ciphertext_entry.pack()


settings_frame = ttk.Labelframe(root1, text="Settings")
# dropdowns to select which scrambler to use
available_rotors = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'none']

pick1 = ttk.Labelframe(settings_frame, text='Select first rotor')
pick1.pack()
select_rotor_1 = ttk.Combobox(pick1, values=available_rotors, state='readonly')
select_rotor_1.current(0)  # set which one appears by default
select_rotor_1.pack()

pick2 = ttk.Labelframe(settings_frame, text='Select second rotor')
pick2.pack()
select_rotor_2 = ttk.Combobox(pick2, values=available_rotors, state='readonly')
select_rotor_2.current(8)
select_rotor_2.pack()

pick3 = ttk.Labelframe(settings_frame, text='Select third rotor')
pick3.pack()
select_rotor_3 = ttk.Combobox(pick3, values=available_rotors, state='readonly')
select_rotor_3.current(8)
select_rotor_3.pack()


# dropdown to select which reflector to use
available_reflectors = ["A", "B", "C", "B thin", "C thin"]
pick4 = ttk.Labelframe(settings_frame, text='Select reflector')
pick4.pack()
select_reflector = ttk.Combobox(pick4, values=available_reflectors, state='readonly')
select_reflector.current(0)
select_reflector.pack()


# Entries to specify starting positions of rotors
set_pos = ttk.Labelframe(settings_frame, text='Set starting positions')
set_pos.pack()
pos1 = ''
set1 = ttk.Entry(set_pos, textvariable=pos1)
set1.pack()
pos2 = ''
set2 = ttk.Entry(set_pos, textvariable=pos2)
set2.pack()
pos3 = ''
set3 = ttk.Entry(set_pos, textvariable=pos3)
set3.pack()


# entry to add plugboard settings
plugboard_entry_label = ttk.Labelframe(settings_frame, text="Set plugboard, eg a:z b:q")
plugboard_entry_label.pack()
plugtext = ""
plugboard_entry_text = StringVar()
plugboard_entry_text.set(plugtext)
plugboard_entry = ttk.Entry(plugboard_entry_label, textvariable=plugboard_entry_text)
plugboard_entry.pack()


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
# TODO (eventually!) make look pretty
plaintext_entry_label.pack()
settings_frame.pack()
encrypt_button.pack()
ciphertext_entry_label.pack()
close_button.pack(side=BOTTOM)


root1.mainloop()