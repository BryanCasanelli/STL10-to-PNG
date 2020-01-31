# ------------------------------------------------------ #
# Developed by Bryan Casanelli, bryancasanelli@gmail.com #
# ------------------------------------------------------ #
# ----------------------------------------------------- #
# This code decompress the STL10 image files            #
# availables at https://cs.stanford.edu/~acoates/stl10/ #
# The files are decompressed in PNG format and          #
# are separated based on their label                    #
# ----------------------------------------------------- #
import os
import numpy as np
from PIL import Image

# Load files
test_images_file = open("test_X.bin","rb")
test_labels_file = open("test_y.bin","rb")
train_images_file = open("train_X.bin","rb")
train_labels_file = open("train_y.bin","rb")
unlabeled_images_file = open("unlabeled_X.bin","rb")

# Create output folders
dir_main = "STL10 images"
dir_test = f"{dir_main}/Test"
dir_train = f"{dir_main}/Train"
dir_unlabeled = f"{dir_main}/Unlabeled"
os.makedirs(dir_main,exist_ok=True)
os.makedirs(dir_test,exist_ok=True)
os.makedirs(dir_train,exist_ok=True)
os.makedirs(dir_unlabeled,exist_ok=True)
for i in range(10):
    os.makedirs(f'{dir_test}/{i+1}',exist_ok=True)
    os.makedirs(f'{dir_train}/{i+1}',exist_ok=True)

# Decompress images
def decompress(image_file,label_file,dir,number):
    for i in range(number):
        image = np.empty([96,96,3],dtype=np.uint8)
        for a in range(3):
            for b in range(96):
                for c in range(96):
                    image[c,b,a] = int(image_file.read(1).hex(),16)
        img = Image.fromarray(image,"RGB")
        if label_file != None:
            label = int(label_file.read(1).hex(),16)
            img.save(f'{dir}/{label}/{i+1}.png')
        else:
            img.save(f'{dir}/{i+1}.png')

# Decompress
if __name__ == "__main__":
    decompress(train_images_file,train_labels_file,dir_train,5000)
    decompress(test_images_file,test_labels_file,dir_test,8000)
    decompress(unlabeled_images_file,None,dir_unlabeled,100000)
