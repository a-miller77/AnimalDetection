# +
# Path to the .tar file
folder_name = 'data'

tar_annot_path = 'annotation.tar'
tar_image_path = 'images.tar'

# Extract the contents of the .tar file
with tarfile.open(tar_annot_path, 'r') as tar:
    tar.extractall(folder_name)

# Extract the contents of the .tar file
with tarfile.open(tar_image_path, 'r') as tar:
    tar.extractall(folder_name)
