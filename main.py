import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from skimage.metrics import structural_similarity
import cv2
import numpy as np
from tkinter import *
from PIL import ImageTk, Image

THRESHOLD = 85

root=tk.Tk()
root.title("Signature Matching System")
root.geometry("1960x900")


def browsefunc(ent):
    filename = askopenfilename(filetypes=([
        ("image", ".jpeg"),
        ("image", ".png"),
        ("image", ".jpg"),
    ]))
    ent.delete(0, tk.END)
    ent.insert(tk.END, filename)

def signature_match(path1, path2):

    before = cv2.imread(path1)
    after = cv2.imread(path2)

    before = cv2.resize(before, (300, 300))
    after = cv2.resize(after, (300, 300))

    before_gray = cv2.cvtColor(before, cv2.COLOR_BGR2GRAY)
    after_gray = cv2.cvtColor(after, cv2.COLOR_BGR2GRAY)

    (score, diff) = structural_similarity(before_gray, after_gray, full=True)
    diff = (diff * 255).astype("uint8")
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    mask = np.zeros(before.shape, dtype='uint8')
    filled_after = after.copy()

    print("Bounding Box Co-ordinates:")
    for c in contours:
        area = cv2.contourArea(c)
        if area > 40:
            x, y, w, h = cv2.boundingRect(c)
            print("X-axis", x, "| ", "Y-axis", y, "| ", "Width", w, "| ", "Height", h)
            cv2.rectangle(before, (x, y), (x + w, y + h), (36, 255, 12), 2)
            cv2.rectangle(after, (x, y), (x + w, y + h), (36, 255, 12), 2)
            cv2.drawContours(mask, [c], 0, (0, 255, 0), -1)
            cv2.drawContours(filled_after, [c], 0, (0, 255, 0), -1)

    return int(score * 100), before, after

def checkSimilarity(window, path1, path2):
    image_frame_1=""
    image_frame_2=""
    result,before,after= signature_match(path1=path1, path2=path2)

    path1 = before
    path2=after

    img_bgr = cv2.cvtColor(path1, cv2.COLOR_BGR2RGB)
    PIL_image = Image.fromarray(np.uint8(img_bgr)).convert('RGB')
    resized_image = PIL_image.resize((600, 400), Image.ANTIALIAS)
    converted_image = ImageTk.PhotoImage(resized_image)


    image_frame_1 = Frame(root)
    image_frame_1.pack(side=LEFT)
    label = Label(image_frame_1, image=converted_image)
    label.pack()


    img_bgr2 = cv2.cvtColor(path2, cv2.COLOR_BGR2RGB)
    PIL_image2 = Image.fromarray(np.uint8(img_bgr2)).convert('RGB')
    resized_image2 = PIL_image2.resize((600, 400), Image.ANTIALIAS)
    converted_image2 = ImageTk.PhotoImage(resized_image2)


    image_frame_2 = Frame(root)
    image_frame_2.pack(side=RIGHT)
    label2 = Label(image_frame_2, image=converted_image2)
    label2.pack()

    label.config(text="Signatures are "+str(result)+f" % similar!!")
    messagebox.showinfo(" Signatures Match", "Signatures are "+str(result)+f" % similar!!")

    root.destroy()

image_frame_2 = Frame(root)
image_frame_2.pack(side = RIGHT)


uname_label = tk.Label(root, text=" Signature Matching:", font=10)
uname_label.place(x=10, y=5)

img1_message = tk.Label(root, text="Original sign", font=10)
img1_message.place(x=10, y=40)

image1_path_entry = tk.Entry(root, font=10)
image1_path_entry.place(x=140, y=40)

img1_browse_button = tk.Button(root, text="Browse", font=10, bg='#9FF06D',command=lambda: browsefunc(ent=image1_path_entry))
img1_browse_button.place(x=350, y=40)

img2_message = tk.Label(root, text="Comparison Sign", font=10)
img2_message.place(x=450, y=40)

image2_path_entry = tk.Entry(root, font=10)
image2_path_entry.place(x=610, y=40)

img2_browse_button = tk.Button(root, text="Browse", font=10, bg='#9FF06D', command=lambda: browsefunc(ent=image2_path_entry))
img2_browse_button.place(x=830, y=40)

compare_button = tk.Button(root, text="Compare", font=10,bg='#2FDFD2',command=lambda: checkSimilarity(window=root, path1=image1_path_entry.get(),path2=image2_path_entry.get(),))
compare_button.place(x=1100, y=40)

exit_button=tk.Button(root,text="Exit",bg="#F09BF7",command=root.destroy)
exit_button.place(x=1300,y=40)


root.mainloop()

