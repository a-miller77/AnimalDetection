import xml.etree.ElementTree as ET
import numpy as np
import math
from PIL import Image

def create_vocab(file_path = './data/vocab.txt') -> tuple:
    with open(file_path) as f:
        lines = f.readlines()
        lines = [i[:-1] for i in lines]  # Remove new line characters
    breed_to_idx = {breed: idx for idx, breed in enumerate(lines)}
    idx_to_breed = {idx: breed for idx, breed in enumerate(lines)}
    return breed_to_idx, idx_to_breed

breed_to_idx, idx_to_breed = create_vocab()
vocab_size = len(breed_to_idx)

def get_bbox(annot):
    root = ET.parse(annot).getroot()
    objects = root.findall('object')
    bbox = []
    for o in objects:
        bndbox = o.find('bndbox')
        xmin = int(bndbox.find('xmin').text)
        ymin = int(bndbox.find('ymin').text)
        xmax = int(bndbox.find('xmax').text)
        ymax = int(bndbox.find('ymax').text)
        bbox.append((xmin,ymin,xmax,ymax))
    return bbox

def get_image_path(annot):
    img_path = 'data/Images/'
    file = annot.replace('\\','/').split('/')
    img_filename = img_path + file[-2] + '/' + file[-1] + '.jpg'
    return img_filename

def get_image(im_path):
    return Image.open(im_path)

def get_image_from_annot(annot):
    return get_image(get_image_path(annot))

def get_dog_breed(annot):
    file = annot.replace('\\','/').split('/')
    return file[-2].split('-', 1)[-1]

def str_to_tuple(str: str) -> tuple:
    return tuple([int(x) for x in str[1:-1].replace(' ', '').split(',')])

def crop_image(image: Image, bbox: tuple, size = 299, verbose = 0) -> Image:
    xmin, ymin, xmax, ymax = bbox #unpack bbox
    im_width, im_height = image.size #image width and height
    width = xmax - xmin #bbox width
    height = ymax - ymin #bbox height
    cntr_x = xmin + width/2 #center of bbox x coord
    cntr_y = ymin + height/2 #center of bbox y coord

    new_bbox = ()
    bbox_expand = 0 # half the distance between the center coord and the outer bounds of the new bbox

    largest_dim = max(size, width, height) #largest dimension
    smallest_dim = min(size, width, height) #smallest dimension

    if(verbose == 1):
        print(f'Bbox: {bbox}')
        print(f'Im width, height: {im_width}, {im_height}')
        print(f'Largest Dim: {largest_dim}')
        print(f'Smallest Dim: {smallest_dim}')
    
    # if bbox is larger or slightly smaller than the asked for size, 
    # grab square arround center and resize to desired size
    if (largest_dim > size):
        bbox_expand = largest_dim/2

    # if bbox is substantially smaller (50% smallest_dim) than the asked for size, grab square 
    # around center of size 100 + smallest_dim, ensuring that its big enough for the entire bbox,
    # then upscale to desired size
    elif (size * 0.5 > smallest_dim):
        bbox_expand = (smallest_dim + 100)/2
    else:
        bbox_expand = largest_dim/2

    # create a new sqaure bbox, rounding down for min bounds and rounding up for max bounds
    new_bbox = (math.floor(cntr_x - bbox_expand), 
                    math.floor(cntr_y - bbox_expand), 
                    math.ceil(cntr_x + bbox_expand), 
                    math.ceil(cntr_y + bbox_expand))
    if(verbose == 1): print(f'New Bbox: {new_bbox}')

    # ensure that the bbox found does not exceed the bounds of the source image
    xmin, ymin, xmax, ymax = new_bbox
    size_adjust, max_neg, max_pos = 0, 0, 0

    # if the new bbox has negative bounds, find the absolute value of the most negative number
    if(xmin < 0 or ymin < 0):
        max_neg = abs(min(xmin, ymin))
    # if the new bbox exceeds the max bounds of the image, 
    # find the largest value that exceeds the image bounds
    if(xmax > im_width or ymax > im_height):
        max_pos = max(xmax - im_width, ymax - im_height)
    
    #find the largest value that exceeds the bounds of the original image
    size_adjust = max(max_neg, max_pos)

    if(verbose == 1): print(f'Size Adjustment: {size_adjust}')

    #shrink the original bbox in all dimensions so as to fit within original image bounds
    if(size_adjust > 0):
        new_bbox = (xmin + size_adjust, 
                    ymin + size_adjust, 
                    xmax - size_adjust, 
                    ymax - size_adjust)
    if(verbose == 1): print(f'Final Bbox: {new_bbox}')

    # NOTE: for exceptionally rectangular bboxs that lie near the edges of a picture, this tactic
    # will cause parts of the dog to be cut off, but works well for the majority of pictures.
    # More work could be done to fix this error, such as allowing a slightly rectangular bbox, say
    # an extra 10% of the axis that would be expanded, before being resized by PILLOW
    return image.resize((size, size), box = new_bbox, resample = Image.BICUBIC)








# +
# def create_cropped():
#     #plt.figure(figsize=(10,6))
#     for i in range(len(dog_image_paths)):
#         bbox = get_bbox(annotations[i])
#         dog = get_image_path(annotations[i])
#         im = Image.open(dog)
#         for j in range(len(bbox)):
#             im2 = im.crop(bbox[j])
#             #im2 = im2.resize((331,331), Image.ANTIALIAS)
#             new_path = dog.replace('data/Images/','data/Cropped/')
#             new_path = new_path.replace('.jpg', '-' + str(j) + '.jpg')
#             im2 = im2.convert('RGB')
#             head, tail = os.path.split(new_path)
#             Path(head).mkdir(parents=True, exist_ok=True)
#             im2.save(new_path)
