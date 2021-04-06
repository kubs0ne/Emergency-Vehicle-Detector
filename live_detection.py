import cv2
import pycuda.autoinit

from utils.yolo_with_plugins import TrtYOLO
from utils.yolo_classes import get_cls_dict
from utils.camera import add_camera_args, Camera
from utils.display import open_window, set_display, show_fps
from utils.visualization import BBoxVisualization

trt_yolo= TrtYOLO('yolov4-tiny-detektor-416', (416, 416), 3)
#trt_yolo= TrtYOLO('yolov4-416', (416, 416), 80)
cap = cv2.VideoCapture(0)  # USB WebCam 0
while True:
    _, img = cap.read()
    if img is None:  break
    middleImg=img.shape[1]/2
    Det=trt_yolo.detect(img)
    #print(Det)
    for i,j,k in zip(Det[0],Det[2],Det[1]):
        #print(i)
        if i.size!=0 and k>0.5:
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
