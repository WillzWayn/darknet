import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import time


classes = ["DAN"]

dir_name='test'
models_dir = 'models-heloisa-v3'



def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def train_test_txt(dir_name):
    with open(os.path.join(models_dir, f'{dir_name}.txt'), 'w') as f:
        f.writelines([f'{dir_name}/images/{i}\n' for i in os.listdir(f'{models_dir}/{dir_name}/images/')])

def convert_annotation(main_path_images:'/home/user/models-eloisa-v3/test/',file_to_edit:'str'):
    """You need to put your files like this:
            .
        └── models_path_name
            ├── train
            |   ├─images
            |   └─annotations (.xml)
            |
            ├── test
                ├─images
                └─annotations (.xml)
                 
    """
    in_file = open(main_path_images+f'/annotations/{file_to_edit}.xml')
    out_file = open(main_path_images+f'/labels/{file_to_edit}.txt', 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            print(f'Warning: {cls} não foi encontrada no array.')
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

wd = getcwd()

print(convert_annotation.__doc__)
time.sleep(1)

print('starting')

assert os.path.exists(f'{models_dir}'), f"Pasta {models_dir} não encontrada"
print(models_dir)


## Take Annotations xml to .txt and create train and test dot txt
for dir_name in ['test', 'train']:
    train_test_txt(dir_name)
    for file in os.listdir(f'{models_dir}/{dir_name}/annotations/'):
        if not os.path.exists(f'{models_dir}/{dir_name}/labels/'):
            os.makedirs(f'{models_dir}/{dir_name}/labels/')
        convert_annotation(f'models-heloisa-v3/{dir_name}',file[:-4])

        
# Create obj.data and obj.names
with open(os.path.join(models_dir,'obj.data'), 'w') as f:
    f.write(f'''classes = {len(classes)}
train  = train.txt  
valid  = test.txt  
names = obj.names  
backup = backup/''')

with open(os.path.join(models_dir,'obj.names'), 'w') as f:
    f.writelines(classes)
