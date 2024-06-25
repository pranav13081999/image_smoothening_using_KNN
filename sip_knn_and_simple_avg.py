import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps
import threading
from tkinter import ttk
from queue import PriorityQueue
import os

class KNNSmooth:
    
    # This function returns smoothend image by performing KNN smoothening provided image, window size, k
    def smooth(self, img, window, k):
        
        m,n = img.shape
        
        # checking if window size is greater than 1 and less than minimum of M X N
        if  window < 1 or window > min(m,n): 
            return 0
        
        # checking if k is less than window size and k is greater than 1
        if k < 1 or k > window*window:
            return 0
        
        # checking if window size is equal to 1 then k should be 0
        if window == 1 and k != 0:
            return 0
        
        # returning same image if window size = 1
        if window == 1:
            return img
        
        # zero padding
        pad_num = window//2
        pad_img = np.pad(img, (pad_num,), 'constant', constant_values=(0))
        
        pad_m,pad_n = pad_img.shape

        img_n = np.zeros([m, n])

        for i in range(pad_num, pad_m-(pad_num)):
            for j in range(pad_num, pad_n-(pad_num)):
                temp_arr = []
                x = -1*(window//2)
                center_val = pad_img[i,j]
                while(x <= window//2):
                    y = -1*(window//2)
                    while(y <= window//2):
                        temp_arr.append(pad_img[i+x, j+y])
                        y += 1
                    x += 1
                knn_arr = []
                pix_val = pad_img[i,j]
                knn_arr.append(pix_val)
                pq = PriorityQueue()
                for i1 in range(len(temp_arr)):
                    pq.put((abs(temp_arr[i1]-pix_val), i1))
                for i1 in range(k):
                    p, pi = pq.get()
                    knn_arr.append(temp_arr[pi])
                img_n[i-pad_num, j-pad_num] = round(np.mean(knn_arr))

        return img_n


class SimpleAveragingSmooth:
    
    # This function returns smoothend image by performing Simple average smoothening provided image, window size
    def smooth(self, img, window):
        m, n = img.shape

        # checking if window size is greater than 1 and less than minimum of M X N
        if  window < 1 or window > min(m,n): 
            return 0
        
        # returning same image if window size = 1
        if window == 1:
            return img
        
        # zero padding
        pad_num = window//2
        pad_img = np.pad(img, (pad_num,), 'constant', constant_values=(0))
        
        pad_m,pad_n = pad_img.shape

        img_smoothened = np.zeros([m, n])

        for i in range(pad_num, pad_m-(pad_num)):
            for j in range(pad_num, pad_n-(pad_num)):
                k = -1*(window//2)
                temp = 0
                cnt = 0
                while(k <= window//2):
                    l = -1*(window//2)
                    while(l <= window//2):
                        temp += pad_img[i+k, j+l]
                        cnt += 1
                        l += 1
                    k += 1
                temp = round(temp / cnt)
                img_smoothened[i-pad_num, j-pad_num] = temp
                
        return img_smoothened
    

def open_image():
    global file_path
    global file_name
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg *.gif *.bmp *.webp *.tif")])
    if file_path:
        # Extract the filename from the path
        file_name = os.path.basename(file_path)
        
        img_name.grid_remove()
        knn_name.grid_remove()
        avg_name.grid_remove()
        dif_name.grid_remove()
        #image_label.grid_remove()
        knn_label.grid_remove()
        avg_label.grid_remove()
        dif_label.grid_remove()
        error_label.configure(text='')
        
        global original_image
        original_image = Image.open(file_path).convert("L")
        image_width, image_height = original_image.size
        image_width, image_height = image_width//(max(image_width, image_height)//256), image_height//(max(image_width, image_height)//256)
        original_image = original_image.resize((image_width, image_height), Image.LANCZOS)
        photo = ImageTk.PhotoImage(original_image)
        image_label.configure(image=photo)
        image_label.image = photo


def is_valid(input_entry):
    ip = input_entry.get()
    try:
        ip_int = int(ip)
        return True, ip_int
    except ValueError:
        return False, 0
    
def run_function():
    img_name.grid_remove()
    knn_name.grid_remove()
    avg_name.grid_remove()
    dif_name.grid_remove()
    # image_label.grid_remove()
    knn_label.grid_remove()
    avg_label.grid_remove()
    dif_label.grid_remove()
    loading_bar.grid(row=3, column=2, columnspan=5)
    loading_text.grid(row=3, column=8)
    loading_bar.start()
    
    if 'original_image' in globals() and file_path:
        # error_label.configure(text='')
        display_original_image(original_image)
        
        image_label.grid(row=6, column=0, columnspan=3)
        knn_label.grid(row=6, column=5, columnspan=3)
        avg_label.grid(row=6, column=10, columnspan=3)
        dif_label.grid(row=6, column=15, columnspan=3)

        img_name.grid(row=5, column=0, columnspan=3)
        knn_name.grid(row=5, column=5, columnspan=3)
        avg_name.grid(row=5, column=10, columnspan=3)
        dif_name.grid(row=5, column=15, columnspan=3)
    else:
        # print("Please upload an image first.")
        error_label.grid(row=4, column=0)
    loading_bar.stop()
    loading_bar.grid_remove()
    loading_text.grid_remove()

def display_original_image(image):
    
    w_b, w = is_valid(input_entry1)
    k_b, k = is_valid(input_entry2)

    if(w_b and k_b):
        
        im = Image.open(r"{}".format(file_path)).convert("L")
        im_arr = np.array(im)
        
        image_width, image_height = im.size
        image_width, image_height = image_width//(max(image_width, image_height)//256), image_height//(max(image_width, image_height)//256)

        knn = KNNSmooth()
        knn_img_arr = knn.smooth(im_arr, window=w, k=k)
        knn_img_arr = np.clip(knn_img_arr, 0, 255).astype(np.uint8)
        knn_img = Image.fromarray(knn_img_arr)
        knn_img.save(file_name.split('.')[0]+' knn_smoothing_output_with_w_'+str(w)+'_k_'+str(k)+'.tif')

        avg = SimpleAveragingSmooth()
        avg_img_arr = avg.smooth(im_arr, w)
        avg_img_arr = np.clip(avg_img_arr, 0, 255).astype(np.uint8)
        avg_img = Image.fromarray(avg_img_arr)
        avg_img.save(file_name.split('.')[0]+'simple_avg_smoothing_output_with_w_'+str(w)+'.tif')
        
        dif = difference_image(knn_img_arr, avg_img_arr)
        dif_img = Image.fromarray(dif)
        dif_img.save(file_name.split('.')[0]+'difference_img_output_with_w_'+str(w)+'_k_'+str(k)+'.tif')

        # Display images
        image = image.resize((image_width, image_height), Image.LANCZOS)
        original_photo = ImageTk.PhotoImage(image)
        knn_img = knn_img.resize((image_width, image_height), Image.LANCZOS)
        knn_photo = ImageTk.PhotoImage(knn_img)
        avg_img = avg_img.resize((image_width, image_height), Image.LANCZOS)
        avg_photo = ImageTk.PhotoImage(avg_img)
        dif_img = dif_img.resize((image_width, image_height), Image.LANCZOS)
        dif_photo = ImageTk.PhotoImage(dif_img)

        image_label.configure(image=original_photo)
        image_label.image = original_photo
        
        img_name.configure(text="Input image")
        knn_name.configure(text="KNN smoothened image")
        avg_name.configure(text="Avg smoothened image")
        dif_name.configure(text="Difference image")

        knn_label.configure(image=knn_photo)
        knn_label.image = knn_photo

        avg_label.configure(image=avg_photo)
        avg_label.image = avg_photo
        
        dif_label.configure(image=dif_photo)
        dif_label.image = dif_photo

def difference_image(image1, image2):
    dif = difference = np.abs(image1 - image2)
    return dif
        
def start_run_function_thread():
    threading.Thread(target=run_function).start()

app = tk.Tk()
app.title("KNN and simple averaging smoothing")

# Labels and input boxes
input_label1 = tk.Label(app, text="Window Size")
input_label2 = tk.Label(app, text="k value")
input_entry1 = tk.Entry(app)
input_entry2 = tk.Entry(app)

input_label1.grid(row=1, column=0)
input_entry1.grid(row=1, column=1)
input_label2.grid(row=2, column=0)
input_entry2.grid(row=2, column=1)

# Image display labels
image_label = tk.Label(app)
knn_label = tk.Label(app)
avg_label = tk.Label(app)
dif_label = tk.Label(app)

img_name = tk.Label(app)
knn_name = tk.Label(app)
avg_name = tk.Label(app)
dif_name = tk.Label(app)

loading_bar = ttk.Progressbar(app, mode="indeterminate", length=280)
loading_text = tk.Label(app, text="Loading...")

image_label.grid(row=6, column=0, columnspan=3)
knn_label.grid(row=6, column=5, columnspan=3)
avg_label.grid(row=6, column=10, columnspan=3)
dif_label.grid(row=6, column=15, columnspan=3)

img_name.grid(row=5, column=0, columnspan=3)
knn_name.grid(row=5, column=5, columnspan=3)
avg_name.grid(row=5, column=10, columnspan=3)
dif_name.grid(row=5, column=10, columnspan=3)

error_label = tk.Label(app, text="Please upload an image first")

# Buttons
upload_button = tk.Button(app, text="Upload Image", command=open_image)
run_button = tk.Button(app, text="Run", command=start_run_function_thread)
upload_button.grid(row=0, column=0)
run_button.grid(row=3, column=1)

file_path = None

# Set window size
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

# Set the window's geometry to the full screen size
app.geometry(f"{screen_width}x{screen_height}")

app.mainloop()
