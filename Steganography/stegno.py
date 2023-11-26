import cv2
import os
import string
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

password = ""
msg = ""

def encode_image(img, message):
    d = {}
    for i in range(255):
        d[chr(i)] = i

    m, n, z = 0, 0, 0

    for i in range(len(message)):
        img[n, m, z] = d[message[i]]
        n = n + 1
        m = m + 1
        z = (z + 1) % 3
    return img

def decode_image(img):
    c = {}
    for i in range(255):
        c[i] = chr(i)

    n, m, z = 0, 0, 0
    decrypted_message = ""

    for i in range(len(msg)):
        decrypted_message += c[img[n, m, z]]
        n = n + 1
        m = m + 1
        z = (z + 1) % 3
    return decrypted_message

def show_image(img):
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    img_tk = ImageTk.PhotoImage(img_pil)
    label_image.config(image=img_tk)
    label_image.image = img_tk
    
def process_image(encrypt=True):
    global password, msg

    img_path = filedialog.askopenfilename(title="Select Image" if encrypt else "Select Encrypted Image")
    print("Selected image path:", img_path)

    if img_path:
        img = cv2.imread(img_path)

        if img is not None:
            if encrypt:
                msg = entry_message.get()
                password = entry_password.get()
                img = encode_image(img, msg)
                cv2.imwrite("encryptedImage.png", img)
            else:
                pas = entry_passcode.get()
                decrypted_message = decode_image(img)
                label_decrypted.config(text="Decrypted message: " + decrypted_message if password == pas else "YOU ARE NOT AUTHORIZED!")
                show_image(img)
        else:
            print("Error: Could not read the image file.")
    else:
        print("Error: No image file selected.")

# Create the main window
root = tk.Tk()
root.title("Image Encryption/Decryption")
root.geometry("400x400")  # Set the initial size of the window

# Create and place widgets in the window
label_message = tk.Label(root, text="Enter the secret message:", bg="lightblue", fg="black",  font=("Helvetica", 12))
label_message.pack()

entry_message = tk.Entry(root, bg="white", fg="black",  font=("Helvetica", 12))
entry_message.pack()

label_password = tk.Label(root, text="Enter a passcode:", bg="lightblue", fg="black",  font=("Helvetica", 12))
label_password.pack()

entry_password = tk.Entry(root, show="*", bg="white", fg="black",  font=("Helvetica", 12))
entry_password.pack()

button_encrypt = tk.Button(root, text="Encrypt Image", command=lambda: process_image(encrypt=True), bg="green", fg="white",  font=("Helvetica", 12))
button_encrypt.pack()

label_passcode = tk.Label(root, text="Enter passcode for Decryption:", bg="lightblue", fg="black",  font=("Helvetica", 12))
label_passcode.pack()

entry_passcode = tk.Entry(root, show="*", bg="white", fg="black",  font=("Helvetica", 12))
entry_passcode.pack()

button_decrypt = tk.Button(root, text="Decrypt Image", command=lambda: process_image(encrypt=False), bg="red", fg="white",  font=("Helvetica", 12))
button_decrypt.pack()

label_decrypted = tk.Label(root, text="", bg="lightblue", fg="black",  font=("Helvetica", 12))
label_decrypted.pack()

label_image = tk.Label(root)
label_image.pack()

root.mainloop()
