import pickle
import numpy as np
import glob
from PIL import Image
from breed_helpers import *

shuffle = True
smart = True
desired_width = 299 # 299 is the size of the Xception network
desired_height = 299


# +
dog_paths = np.array(glob.glob('data/Images/*/*'))
annotations = np.array(glob.glob('data/Annotation/*/*'))

if(get_image_path(annotations[0]) != dog_paths[0]):
    dog_paths = [get_image_path(x) for x in annotations]
    assert get_image_path(annotations[0]) == dog_paths[0]
# -

if(shuffle):
    indices = np.arange(len(dog_paths))  # Create an array of indices
    np.random.shuffle(indices)  # Shuffle the indices

    dog_paths = np.array(dog_paths)[indices]  # Shuffle dog paths based on indices
    annotations = np.array(annotations)[indices] # Shuffle annotations based on indices

# +
#breeds = [get_dog_breed(x) for x in annotations] # generate a list of breeds
# -

im_list = list()
breeds = list()
counter = 1
mod_size = 1000 #update frequency on the length of the process, set to 1 to disable

# Resizing algorithim
for i, image_path in enumerate(dog_paths):
    # Brute Force Resize (squish everything down to (299, 299, 3))
        #image = Image.open(image_path).convert('RGB')
        #arr = np.asarray(image.resize((desired_width, desired_height)))
    # Smart Image Resize (grab a 299*299 square centered around the dogs bbox)
    bbox_list = get_bbox(annotations[i])
    for bbox in bbox_list:
        image = crop_image(get_image(image_path), bbox, size = desired_width)
        arr = np.asarray(image.convert('RGB'))
        im_list.append(arr)
        breeds.append(get_dog_breed(annotations[i]))

    if(len(im_list) % mod_size == 1):
        print(f'checkin {counter}/{int(len(dog_paths)/mod_size)+1}')
        counter += 1


images = np.stack(im_list, axis=0)

data = {'X': images, 'y': [breed_to_idx[i] for i in breeds]}

shuffled, mode, size = 'shuffled_' if shuffle else '', 'smart_' if smart else 'brute_', desired_width
with open(f'data/{shuffled}{mode}resized_{size}_images.pickle', 'wb') as file:
    pickle.dump(data, file)


