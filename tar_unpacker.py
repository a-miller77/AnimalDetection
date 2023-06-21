# Unpacks the default data and annotation files downloaded from http://vision.stanford.edu/aditya86/ImageNetDogs/
# Additionally, sets up the data file structure for the project

import os
import tarfile
import shutil


# Folder to be created
folder_name = 'data'

tar_annot = 'annotation.tar'
tar_image = 'images.tar'

os.makedirs(folder_name, exist_ok=True)

# Extract the contents of the .tar file
with tarfile.open(tar_annot, 'r') as tar:
    tar.extractall(folder_name)

# Extract the contents of the .tar file
with tarfile.open(tar_image, 'r') as tar:
    tar.extractall(folder_name)


tar_annot_name = os.path.basename(tar_annot)
tar_image_name = os.path.basename(tar_image)

new_tar_annot = os.path.join(folder_name, tar_annot_name)
new_tar_image = os.path.join(folder_name, tar_image_name)

shutil.move(tar_annot, new_tar_annot)
shutil.move(tar_image, new_tar_image)