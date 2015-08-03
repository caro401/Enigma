# TODO error handling!!! find out how to pop up an error message
# TODO make the dropdowns actually define the machine to use for encryption

from tkinter import *
from tkinter import ttk
import enigma

root1 = Tk()  # root window
root1.title("Better Encryptor!")


# initialise the machine that will be used for encryption
possible_scramblers = [enigma.si, enigma.sii, enigma.siii, enigma.siv, enigma.sv, enigma.svi, enigma.svii,
                       enigma.sviii, enigma.sx]
possible_reflectors = [enigma.ra, enigma.rb, enigma.rc, enigma.rbt, enigma.rct, enigma.rx]
scram_list = []
refl = possible_reflectors[5]
current_machine = enigma.Machine(scram_list, refl)


# make a text box to take plaintext input, label it
plaintext_entry_label = ttk.Label(root1, text="Input plaintext:")
plaintext_entry = ttk.Entry(root1)  # when you create a widget, you must pass its parent as a parameter


# entry for displaying ciphertext output
ciphertext = "Your ciphertext goes here!"
ciphertext_entry_text = StringVar()
ciphertext_entry_text.set(ciphertext)
ciphertext_entry = ttk.Entry(root1, textvariable=ciphertext_entry_text)


# bind encrypt button to function displaying ciphertext
# TODO remember to change this to not default machine when functionality exists!
def showentry():
    text = plaintext_entry.get()
    ciphertext = current_machine.encrypt(text)
    ciphertext_entry_text.set(ciphertext)

encrypt_button = ttk.Button(root1, text="encrypt!", command=showentry)


# dropdowns to select which scrambler to use
# NOTE these do nothing yet!
available_rotors = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'none']

pick1 = ttk.Labelframe(root1, text='Select first rotor')
select_rotor_1 = ttk.Combobox(pick1, values=available_rotors, state='readonly')
select_rotor_1.current(0)  # set which one appears by default
select_rotor_1.pack()

pick2 = ttk.Labelframe(root1, text='Select second rotor')
select_rotor_2 = ttk.Combobox(pick2, values=available_rotors, state='readonly')
select_rotor_2.current(8)
select_rotor_2.pack()

pick3 = ttk.Labelframe(root1, text='Select third rotor')
select_rotor_3 = ttk.Combobox(pick3, values=available_rotors, state='readonly')
select_rotor_3.current(8)
select_rotor_3.pack()


# dropdown to select which reflector to use
# NOTE this does nothing yet!
available_reflectors = ["A", "B", "C", "B thin", "C thin"]
pick4 = ttk.Labelframe(root1, text='Select reflector')
select_reflector = ttk.Combobox(pick4, values=available_reflectors, state='readonly')
select_reflector.current(0)
select_reflector.pack()


# make a button that closes the window
close_button = ttk.Button(root1, text='close', command=root1.quit)


# make the cursor appear in the plaintext entry box by default
plaintext_entry.focus()


# PACK ALL THE THINGS!
# TODO (eventually!) make look pretty
plaintext_entry_label.pack()
plaintext_entry.pack()
pick1.pack()
pick2.pack()
pick3.pack()
pick4.pack()
encrypt_button.pack()
ciphertext_entry.pack()


close_button.pack(side=BOTTOM)

root1.mainloop()