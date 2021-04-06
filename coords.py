import cv2
import pycuda.autoinit

from utils.yolo_with_plugins import TrtYOLO

img = cv2.imread('karetki1.jpg')
middleImg=img.shape[1]/2
trt_yolo= TrtYOLO('yolov4-tiny-detektor-416', (416, 416), 3)
Det=trt_yolo.detect(img)
#print(Det)
for i,j,k in zip(Det[0],Det[2],Det[1]):
    if i.size!=0:
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
