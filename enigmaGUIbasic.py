import tkinter as tk
import enigma

root1 = tk.Tk()  # root window
root1.title("Basic Encryptor!")

label1 = tk.Label(root1, text='input your plaintext and press enter!')  # writes some text to label the entry
entry = tk.Entry(root1)  # makes a text box to take input
label2 = tk.Label(root1, text="ciphertext:")

ciphertext = "Your ciphertext goes here!"
ciphertext_label_text = tk.StringVar()
ciphertext_label_text.set(ciphertext)
ciphertext_label = tk.Label(root1, textvariable=ciphertext_label_text)


def showentry(event):
    text = entry.get()
    ciphertext = enigma.default_machine.encrypt(text)
    ciphertext_label_text.set(ciphertext)

entry.bind('<Return>', showentry)  # make this function run when you press enter

close_button = tk.Button(root1, text='close', command=root1.quit)

# layout
label1.pack(side=tk.TOP)  # make the things appear in the root window
entry.pack()
label2.pack()
ciphertext_label.pack()
close_button.pack(side=tk.BOTTOM)


root1.mainloop()