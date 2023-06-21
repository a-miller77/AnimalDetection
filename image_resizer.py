import pickle
import numpy as np
import glob
from PIL import Image
from breed_helpers import get_dog_breed

shuffle = True
desired_width = 299 # Saw 299 on someone else project, no reason to stick to this number
desired_height = 299


dog_paths = np.array(glob.glob('data/Images/*/*'))
annotations = np.array(glob.glob('data/Annotation/*/*'))

if(shuffle):
    indices = np.arange(len(dog_paths))  # Create an array of indices
    np.random.shuffle(indices)  # Shuffle the indices

    dog_paths = np.array(dog_paths)[indices]  # Shuffle dog paths based on indices
    annotations = np.array(annotations)[indices] # Shuffle annotations based on indices

breeds = [get_dog_breed(x) for x in annotations] # generate a list of breeds

im_list = list()
counter = 0
mod_size = 1000 #update frequenct on the length of the process, set to 1 to disable

# Brute Force Resize (squish everything down to (299, 299, 3))
for image_path in dog_paths:
    image = Image.open(image_path).convert('RGB')
    arr = np.asarray(image.resize((desired_width, desired_height)))
    im_list.append(arr)
    if(len(im_list) % mod_size == 1):
        counter += 1
        print(f'checkin {counter}/{int(len(dog_paths)/mod_size)}')

images = np.stack(im_list, axis=0)

data = {'X': images, 'y': breeds}

mode, size = 'shuffled_' if shuffle else '', desired_width
with open(f'data/{mode}brute_resized_{size}_images.pickle', 'wb') as file:
    pickle.dump(data, file)