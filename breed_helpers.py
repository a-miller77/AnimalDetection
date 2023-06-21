import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image

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

def get_dog_breed(annot):
    file = annot.replace('\\','/').split('/')
    return file[-2].split('-', 1)[-1]
