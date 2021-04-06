import cv2
import pycuda.autoinit
from multiprocessing import Process,Queue

from utils.yolo_with_plugins import TrtYOLO
from utils.yolo_classes import get_cls_dict
from utils.camera import add_camera_args, Camera
from utils.display import open_window, set_display, show_fps
from utils.visualization import BBoxVisualization

import pyaudio
import os
import struct
import numpy as np
from scipy.fftpack import fft
import time

Qa=Queue()
    
def audio():
    C = 1024 * 2             
    F = pyaudio.paInt16  
    CH = 1             
    R = 44100              

    p = pyaudio.PyAudio()

    stream = p.open(
    format=F,
    channels=CH,
    rate=R,
    input=True,
    output=True,
    frames_per_buffer=C
    )
    xf = np.linspace(0, R, C)
    while True:
        data = stream.read(C)  
        data_int = struct.unpack(str(2*C) + 'B', data)
        #data_np = np.array(data_int, dtype='b')[::2] + 128
        yf = fft(data_int)
        ydata=np.abs(yf[0:C]) / (128 * C)
        for x,y in zip(xf,ydata):    
            if x>600 and x<1300 and y>0.4:
                Qa.put(1)
        
if __name__ == '__main__':
    trt_yolo = TrtYOLO('yolov4-tiny-detektor-416', (416, 416), 3)
    cap = cv2.VideoCapture(0)  # USB WebCam 0
    p1=Process(target=audio)  
    p1.start()
    while True:
        _, img = cap.read()
        if img is None:  break
        middleImg=img.shape[1]/2
        Det=trt_yolo.detect(img)
        if Det[0].size==0 and Qa.get()==1:
            print("pojazd na sygnale")
        for i,j,k in zip(Det[0],Det[2],Det[1]):
            if Qa.get()==1 and i.size!=0 and k>0.5:
                middleDet = i[0] + (i[2]-i[0])/2
                if middleDet>middleImg+middleImg/10 and j==0:
                    print("karetka z prawej strony")
                if middleDet<middleImg-middleImg/10 and j==0:
                    print("karetka z lewej strony")
                if middleDet>middleImg-middleImg/10 and middleDet<middleImg+middleImg/10 and j==0:
                    print("karetka po środku")
                if middleDet>middleImg+middleImg/10 and j==1:
                    print("radiowóz z prawej strony")
                if middleDet<middleImg-middleImg/10 and j==1:
                    print("radiowóz z lewej strony")
                if middleDet>middleImg-middleImg/10 and middleDet<middleImg+middleImg/10 and j==1:
                    print("radiowóz po środku")
                if middleDet>middleImg+middleImg/10 and j==2:
                    print("wóz strażacki z prawej strony")
                if middleDet<middleImg-middleImg/10 and j==2:
                    print("wóz strażacki z lewej strony")
                if middleDet>middleImg-middleImg/10 and middleDet<middleImg+middleImg/10 and j==2:
                    print("wóz strażacki po środku")

    p1.join()
            
    
    
    
    
