#! /usr/bin/python3
# -*- coding: utf-8 -*-
'''
| author:
| Belal HMEDAN, LIG lab/ Marven Team, France, 2021.
| Raspberry vision handeling script.
'''
import cv2
from time import sleep # , time

# tic = time()

resolution = (1024, 768)

cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])  # max: 2592
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1]) # max: 1944
# cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M','J','P','G'))

state=1

while(state!=0):

    with open('/home/pi1/vision/order', 'r') as fp:
        line = fp.readlines()
        if(len(line)!=0):
            # print(line)
            state=int(line[0])

    if(state==2):
        status , frame = cap.read()
        cv2.imwrite('/home/pi1/vision/image.jpg', frame)
        toc=time()
        # print('time neeed: {}'.format(round(toc-tic,2)))
        # tic=toc
        sleep(0.5)

cap.release()