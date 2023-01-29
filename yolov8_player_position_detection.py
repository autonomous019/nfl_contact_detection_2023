# -*- coding: utf-8 -*-
"""yolov8-player-position-detection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lGNnQ2vM1L9xy8By2jPjZmyl-18kOXrj

# NFL YOLOv8 Player Position Detection
https://github.com/ultralytics/ultralytics<br/>

Ultralytics YOLOv8, developed by Ultralytics, is a cutting-edge, state-of-the-art (SOTA) model that builds upon the success of previous YOLO versions and introduces new features and improvements to further boost performance and flexibility. YOLOv8 is designed to be fast, accurate, and easy to use, making it an excellent choice for a wide range of object detection, image segmentation and image classification tasks.
"""

# Import from GoogleDrive

from google.colab import drive
import os

drive.mount('/content/gdrive')
os.chdir("//content/gdrive/MyDrive/nfl-player-contact-detection/")

data_dir = "/content/gdrive/My Drive/nfl-player-contact-detection/"
'''
data_dir = "../input/"
OUTPUT_DIR = './'
'''

!pip install ultralytics

from ultralytics import YOLO
import os
import cv2
import shutil
import numpy as np
import pandas as pd
from PIL import Image
from tqdm import tqdm
from IPython.display import HTML, Video, Image, clear_output
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import animation, rc
rc('animation', html='jshtml')

"""# Copy Source Movie"""

'''
!mkdir -p /kaggle/working/sample1    ### source mp4
!mkdir -p /kaggle/working/sample2    ### frame images
!mkdir -p /kaggle/working/sample3    ### fig
'''

path = data_dir + 'sample1'
path2 = data_dir + 'sample2'
path3 = data_dir + 'sample3'
path4 = data_dir + 'predict'

#print(path)
# Check whether the specified path exists or not
isExist = os.path.exists(path)
if not isExist:
  # Create a new directory because it does not exist
  os.makedirs(path)

isExist2 = os.path.exists(path2)
if not isExist2:
  # Create a new directory because it does not exist
  os.makedirs(path2)

isExist3 = os.path.exists(path3)
if not isExist3:
  # Create a new directory because it does not exist
  os.makedirs(path3)

isExist4 = os.path.exists(path4)
if not isExist4:
  # Create a new directory because it does not exist
  os.makedirs(path4)

"""58168_003392_Sideline.mp4"""

'''
path_mp0='/kaggle/input/nfl-player-contact-detection/train/58168_003392_Sideline.mp4'
path_mp1='/kaggle/working/sample1/sample.mp4'
'''

path_mp0=data_dir + 'train/58168_003392_Sideline.mp4'
path_mp1=data_dir + 'sample1/sample.mp4'

shutil.copy(path_mp0,path_mp1)

path_mp2=data_dir + 'test/58172_003247_Sideline.mp4'
path_mp3=data_dir + 'predict/sample.mp4'

shutil.copy(path_mp2,path_mp3)



'''
print(os.listdir('/kaggle/working'))
print(os.listdir('/kaggle/working/sample1'))
'''

#print(os.listdir('/kaggle/working'))
print(os.listdir(data_dir + 'sample1'))

"""# YOLOv8"""

model = YOLO(data_dir + "yolov8x.pt")

!yolo task=detect mode=predict model=yolov8x.pt conf=0.001 source={path_mp1}

!ls predict

path_mp2="/kaggle/working/runs/detect/predict/sample.mp4"
path_mp2=data_dir + 'predict/sample.mp4'

Video(path_mp2, width=600, height=400, embed=True)

'''
def video2frames(video_file=path_mp2, image_dir='/kaggle/working/sample2/', image_file='img_%s.png'):
    i = 0
    cap = cv2.VideoCapture(video_file)
    while(cap.isOpened()):
        flag, frame = cap.read()
        if flag == False:
            break
        cv2.imwrite(image_dir+image_file % str(i).zfill(5), frame) 
        i += 1
    cap.release()
    
video2frames()
'''

def video2frames(video_file=path_mp2, image_dir=data_dir + 'sample2/', image_file='img_%s.png'):
    i = 0
    cap = cv2.VideoCapture(video_file)
    while(cap.isOpened()):
        flag, frame = cap.read()
        if flag == False:
            break
        cv2.imwrite(image_dir+image_file % str(i).zfill(5), frame) 
        i += 1
    cap.release()
    
video2frames()

'''
paths0=[]
for dirname, _, filenames in os.walk('/kaggle/working/sample2/'):
    for filename in filenames:
        if filename[-4:]=='.png':
            paths0+=[(os.path.join(dirname, filename))]
paths0=sorted(paths0)            
images0=[]
for i in tqdm(range(len(paths0))):
    images0+=[cv2.imread(paths0[i])]
'''

paths0=[]
for dirname, _, filenames in os.walk(data_dir+ 'sample2/'):
    for filename in filenames:
        if filename[-4:]=='.png':
            paths0+=[(os.path.join(dirname, filename))]
paths0=sorted(paths0)            
images0=[]
for i in tqdm(range(len(paths0))):
    images0+=[cv2.imread(paths0[i])]

def create_animation(ims):
    fig=plt.figure(figsize=(12,8))
    plt.axis('off')
    im=plt.imshow(cv2.cvtColor(ims[0],cv2.COLOR_BGR2RGB))
    plt.close()
    
    def animate_func(i):
        im.set_array(cv2.cvtColor(ims[i],cv2.COLOR_BGR2RGB))
        return [im]

    return animation.FuncAnimation(fig, animate_func, frames=len(ims), interval=1000//10)

create_animation(np.array(images0))

"""### Obtain rectangle information"""

results = model.predict(path_mp1,conf=0.001)
print(len(results))

BOX=pd.DataFrame(columns=range(6))
for i in range(len(results)):
    arri=pd.DataFrame(results[i].boxes.boxes).astype(float)
    arri['i']=i
    BOX=pd.concat([BOX,arri],axis=0)
BOX.columns=['x','y','x2','y2','confidence','class','i']
display(BOX)

class_map = {0: u'__background__', 1: u'person', 2: u'bicycle',3: u'car', 4: u'motorcycle', 5: u'airplane', 6: u'bus', 7: u'train', 8: u'truck', 9: u'boat', 10: u'traffic light', 11: u'fire hydrant', 12: u'stop sign', 13: u'parking meter', 14: u'bench', 15: u'bird', 16: u'cat', 17: u'dog', 18: u'horse', 19: u'sheep', 20: u'cow', 21: u'elephant', 22: u'bear', 23: u'zebra', 24: u'giraffe', 25: u'backpack', 26: u'umbrella', 27: u'handbag', 28: u'tie', 29: u'suitcase', 30: u'frisbee', 31: u'skis', 32: u'snowboard', 33: u'sports ball', 34: u'kite', 35: u'baseball bat', 36: u'baseball glove', 37: u'skateboard', 38: u'surfboard', 39: u'tennis racket', 40: u'bottle', 41: u'wine glass', 42: u'cup', 43: u'fork', 44: u'knife', 45: u'spoon', 46: u'bowl', 47: u'banana', 48: u'apple', 49: u'sandwich', 50: u'orange', 51: u'broccoli', 52: u'carrot', 53: u'hot dog', 54: u'pizza', 55: u'donut', 56: u'cake', 57: u'chair', 58: u'couch', 59: u'potted plant', 60: u'bed', 61: u'dining table', 62: u'toilet', 63: u'tv', 64: u'laptop', 65: u'mouse', 66: u'remote', 67: u'keyboard', 68: u'cell phone', 69: u'microwave', 70: u'oven', 71: u'toaster', 72: u'sink', 73: u'refrigerator', 74: u'book', 75: u'clock', 76: u'vase', 77: u'scissors', 78: u'teddy bear', 79: u'hair drier', 80: u'toothbrush'}

BOX['class']=BOX['class'].apply(lambda x: class_map[int(x)+1])
BOX=BOX.reset_index(drop=True)
display(BOX)
display(BOX['class'].value_counts())

data0=BOX[BOX['class']=='person'] #[BOX['confidence']>0.1]
data0['i']=data0['i'].apply(lambda x: int(x))
data0['y']=data0['y'].apply(lambda y: -y)
data0=data0.reset_index(drop=True)
data0['j']=data0.index.tolist()
display(data0)
print(len(data0))
data0.to_csv(data_dir + 'data0.csv',index=False)

import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

print(data0['x'].min(),data0['x'].max())
print(data0['y'].min(),data0['y'].max())

for i in range(len(results)):
    #plt.figure(figsize=(8,6))
    sns.scatterplot(data=data0[data0['i']==i], x="x", y="y", palette="Paired") #, hue="i", 
    plt.title("Player Positions "+str(i).zfill(5))
    #plt.legend()
    #plt.show()
    plt.savefig('./sample3/fig_'+str(i).zfill(5)+'.png')

'''
paths3=[]
for dirname, _, filenames in os.walk('/kaggle/working/sample3/'):
    for filename in filenames:
        if filename[-4:]=='.png':
            paths3+=[(os.path.join(dirname, filename))]
paths3=sorted(paths3)
print(paths3[100:103])
images0=[]
for i in tqdm(range(0,len(paths3),2)):
    images0+=[cv2.imread(paths3[i])]
'''

paths3=[]
for dirname, _, filenames in os.walk(data_dir+ 'sample3/'):
    for filename in filenames:
        if filename[-4:]=='.png':
            paths3+=[(os.path.join(dirname, filename))]
paths3=sorted(paths3)
print(paths3[100:103])
images0=[]
for i in tqdm(range(0,len(paths3),2)):
    images0+=[cv2.imread(paths3[i])]

def create_animation(ims):
    fig=plt.figure(figsize=(12,8))
    plt.axis('off')
    im=plt.imshow(cv2.cvtColor(ims[0],cv2.COLOR_BGR2RGB))
    plt.close()
    
    def animate_func(i):
        im.set_array(cv2.cvtColor(ims[i],cv2.COLOR_BGR2RGB))
        return [im]

    return animation.FuncAnimation(fig, animate_func, frames=len(ims), interval=1000//10)

create_animation(np.array(images0))



