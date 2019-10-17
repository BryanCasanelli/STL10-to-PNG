from __future__ import print_function
import sys

if "-h" in sys.argv or "--help" in sys.argv:
    print(
    '''
Python script to transform the binary STL-10 dataset (http://cs.stanford.edu/~acoates/stl10/) into PNG image files.

Usage: python/python3 stl10_to_png.py [OPTIONS]

    OPTIONS:
    -h  --help      : Show this help.
    -d  --download  : Download the dataset and extract it.
                      If the file is already downloaded, then only extract it.

Warning: Transform the unlabeled data into images requires approximately 3 GB of free RAM.

Developed by Bryan Casanelli based on STL10 by Martin Tutek.
https://github.com/BryanCasanelli
bryancasanelli@gmail.com.
2019.
    '''
    )
    exit(0)

import os, sys, tarfile, errno
import numpy as np
import matplotlib.pyplot as plt
if sys.version_info >= (3, 0, 0):
    import urllib.request as urllib
else:
    import urllib
try:
    from imageio import imsave
except:
    from scipy.misc import imsave

# Height x width x depth
SIZE = 96*96*3

# Path to the directory with the data
DATA_DIR = 'data'

# URL of the binary data
DATA_URL = 'http://ai.stanford.edu/~acoates/stl10/stl10_binary.tar.gz'

# Path to the binary image files
DATA_PATH = ['data/test_X.bin','data/train_X.bin','data/unlabeled_X.bin']

# Path to the binary labels files
LABEL_PATH = ['data/test_y.bin','data/train_y.bin']

def read_labels(path_to_labels):
    with open(path_to_labels, 'rb') as f:
        labels = np.fromfile(f, dtype=np.uint8)
        return labels

def read_all_images(path_to_data):
    with open(path_to_data, 'rb') as f:
        data = np.fromfile(f, dtype=np.uint8)

        # The first 96*96 values are the red channel,
        # the next 96*96 are green, and the last are blue.
        # The -1 is since the size of the pictures is
        # determined automatically by numpy.
        images = np.reshape(data, (-1, 3, 96, 96))

        # Transpose the images into a standard image format
        images = np.transpose(images, (0, 3, 2, 1))
        return images

def save_image(image, name):
    imsave("%s.png" % name, image, format="png")

def download_and_extract():
    def progress(current_size, total_size):
        sys.stdout.write('\rDownloading %s: %.2fMB of %.2fMB, %.2f%%' % (filename,float(current_size/10**6),float(total_size/10**6),float(current_size) / float(total_size) * 100.0))
        sys.stdout.flush()
    dest_directory = DATA_DIR
    if not os.path.exists(dest_directory):
        os.makedirs(dest_directory)
    filename = DATA_URL.split('/')[-1]
    filepath = os.path.join(dest_directory, filename)
    download = urllib.Request(DATA_URL)
    data = urllib.urlopen(download)
    meta = data.info()
    total_size = int(meta.get_all("Content-Length")[0])
    if os.path.isfile(filepath) == True:
        current_size = os.path.getsize(filepath)
        if current_size != total_size:
            download.headers['Range'] = 'bytes=%s-' % (current_size)
            data = urllib.urlopen(download)
            file = open(filepath, 'ab')
        else:
            print("File already downloaded")
    else:
        current_size = 0
        file = open(filepath, 'wb')
    if current_size != total_size:
        block_size = 2**15
        while True:
            buffer = data.read(block_size)
            if not buffer:
                break
            file.write(buffer)
            current_size += len(buffer)
            progress(current_size, total_size)
        print('Downloaded', filename)
    try:
        file.close()
    except:
        pass
    print("Extracting...")
    tarfile.open(filepath, 'r:gz').extractall(dest_directory)
    os.rename("data/stl10_binary/test_X.bin", DATA_PATH[0])
    os.rename("data/stl10_binary/train_X.bin", DATA_PATH[1])
    os.rename("data/stl10_binary/unlabeled_X.bin", DATA_PATH[2])
    os.rename("data/stl10_binary/test_y.bin", LABEL_PATH[0])
    os.rename("data/stl10_binary/train_y.bin", LABEL_PATH[1])
    os.rename("data/stl10_binary/class_names.txt", DATA_DIR + "/class_names.txt")
    os.rename("data/stl10_binary/fold_indices.txt", DATA_DIR + "/fold_indices.txt")
    os.rmdir("data/stl10_binary")
    print("Done")

def progress(current, total):
    sys.stdout.write('\r%.2f%%' % ((current/total)*100))
    sys.stdout.flush()

def save_images(images, labels, aux):
    print("Saving images to disk...")
    if aux == 0:
        d = "Test"
    elif aux == 1:
        d = "Train"
    else:
        d = "Unlabeled"
    i = 0
    for image in images:
        label = labels[i]
        directory = d + '/' + str(label) + '/'
        try:
            os.makedirs(directory, exist_ok=True)
        except OSError as exc:
            if exc.errno == errno.EEXIST:
                pass
        filename = directory + str(i)
        save_image(image, filename)
        i = i+1
        if i%1000 == 0:
            progress(i,images.shape[0])
    print("\nDone")

if __name__ == "__main__":
    if "-d" in sys.argv or "--download" in sys.argv:
        download_and_extract()

    for i in range(3):
        if i == 0:
            print("--- Test data ---")
        elif i == 1:
            print("--- Train data ---")
        else:
            print("--- Unlabeled data ---")

        if os.path.isfile(DATA_PATH[i]) == True:
            images = read_all_images(DATA_PATH[i])
            print("Images shape:" + str(images.shape))

            if i == 0 or i == 1:
                labels = read_labels(LABEL_PATH[i])
            else:
                labels = np.ones(100000,dtype=int)
            print("Labels shape:" + str(labels.shape))

            save_images(images, labels, i)
        else:
            print("Please first download and/or extract the data with the -d argument")
