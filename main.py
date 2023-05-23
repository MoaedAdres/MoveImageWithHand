import cv2 as cv
import HandDetection as hand
import ctime 
import step as st
import GUI 
import time
from read_Image import Image_Read

cap_region_x_begin = 0.5 
cap_region_y_end = 0.5

bgSubThreshold = 0
isBgCaptured = 0 #  0 => r  restart || 1 => b completed
i = 1

camera = cv.VideoCapture(0)  
camera.set(10,200)  #Set video properties تعيين خصائص الفيديو

ctime.curTime()

main,path =GUI.userInterfaces()



while camera.isOpened():
  ret,frame = camera.read()
  frame = cv.bilateralFilter(frame,5,50,100)
  frame = cv.flip(frame,1) 
  cv.rectangle(frame,(int(cap_region_x_begin * frame.shape[1]),0),(frame.shape[1],int(cap_region_y_end * frame.shape[0])),(0,255),2)
  cv.imshow('original',frame)  

  #main operation
  if isBgCaptured == 1: 
    hand.hand_Detection(bgModel=bgModel,frame=frame,cap_region_x_begin=cap_region_x_begin,cap_region_y_end=cap_region_y_end)

  k = cv.waitKey(10)
  if k == 27 or  k == ord('p'):
    camera.release()
    cv.destroyAllWindows()
    break

  elif k == ord('b'):
    print("****** Minor 3-4 Seconds lag *****")
    bgModel = cv.createBackgroundSubtractorMOG2(0,bgSubThreshold)
    isBgCaptured = 1
    print('Background Captured')

  elif k == ord('r'):
    bgModel = None
    isBgCaptured = 0
    print('Reset BackGround')

  elif k == ord('n'):
    # if i == 1 :
      print(1)
      # bgModel = None
      # isBgCaptured = 0
      # hand.restart_project = False
    #   i -=1
    # else :
    #   print(2)
      # bgModel = cv.createBackgroundSubtractorMOG2(0,bgSubThreshold)
      # isBgCaptured = 1
      # hand.restart_project = True

      hand.finger_zero = True
      hand.finger_zero=True
      hand.finger_one=True
      hand.finger_two=True
      hand.finger_three= True
      hand.finger_chosed = True
      hand.checktType = 'No Type'

      hand.axis_x = 0
      hand.Values_first_axis_x = 0
      hand.Values_end_axis_x = 0
      hand.bool_first_axis_x = False
      hand.bool_end_axis_x = False
      hand.end_of_processing = False
      st.is_Rotated = False
      # i +=1