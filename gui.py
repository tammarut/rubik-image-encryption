import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import os
import encrypt as enc
import decrypt as dec

image_path = "./input"
enc_image_path = "./encrypted_images/"
dec_image_path = "./decrypted_images/"


def encrypt(original_img_name):
    enc.encrypt(original_img_name)
    enc_img = ImageTk.PhotoImage(Image.open(enc_image_path + base))
    enc_img_label = tk.Label(image=enc_img)
    enc_img_label.image = enc_img
    enc_img_label.pack()


def decrypt(enc_img_name):
    dec.decrypt(enc_img_name)
    dec_img = ImageTk.PhotoImage(Image.open(dec_image_path + base))
    dec_img_label = tk.Label(image=dec_img)
    dec_img_label.image = dec_img
    dec_img_label.pack()


window = tk.Tk()
window.wm_title("Rubik's Cube Image Encryption")
window.geometry("400x400")
image_name = filedialog.askopenfilename(initialdir=image_path,
                                        filetypes=(
                                            ("all files", "*.*"), ("jpeg files", "*.jpg"), ("png files", "*.png")))

base = os.path.basename(image_name)
frame_label = tk.Frame(bg="azure3")
frame_original_image = tk.Frame(master=window, bg="gainsboro")
frame_enc_image = tk.Frame(master=window, bg="lavender")
frame_dec_image = tk.Frame(master=window, bg="SkyBlue1")
frame_enc_btn = tk.Frame(master=window, bg="yellow")
frame_dec_btn = tk.Frame(master=window, bg="green")

img = ImageTk.PhotoImage(Image.open(image_name))
img_label = tk.Label(master=frame_original_image, image=img)
img_label.pack()
label = tk.Label(master=frame_label, text="Rubik's Cube Image Encryption",
                 font="30",
                 fg="white",
                 bg="black")
label.pack()

encrypt_btn = tk.Button(master=frame_enc_btn, text="Encrypt", command=lambda: encrypt(base))
decrypt_btn = tk.Button(master=frame_dec_btn, text="Decrypt", command=lambda: decrypt(base))
encrypt_btn.pack()
decrypt_btn.pack()

frame_label.pack()
frame_original_image.pack()
frame_enc_image.pack()
frame_dec_image.pack()
frame_dec_btn.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=True)
frame_enc_btn.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=True)

window.mainloop()
window.destroy()
