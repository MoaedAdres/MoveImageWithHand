import HandDetection as hand
import cv2 as cv
import numpy as np
import ctime 
is_Rotated = False 
is_Scale = False
def Determine_The_Direction(x_start , x_end):
    if x_end > x_start : 
        return 'right'
    elif x_end < x_start:
        return 'left'
    else :
        return 'nothing'

def chosed_Translate(image , direction):
    global M
    rows,cols,depth = image.shape
    if direction == 'right':
        M = np.float32([[1,0,1],[0,1,0]])
    elif direction == 'left':
        M = np.float32([[1,0,-1],[0,1,0]])
    elif direction == 'nothing':
        M = np.float32([[1,0,0],[0,1,0]])
    dst = cv.warpAffine(image,M,(cols,rows))    
    return dst

def chosed_Rotate(image,direction):
    global M , is_Rotated ,dst 
    rows,cols,depth = image.shape
    
    if not is_Rotated:
        if direction == 'right' :
            print('right')
            M = cv.getRotationMatrix2D((cols/2,rows/2),-90,1)
            dst = cv.warpAffine(image,M,(cols,rows)) 
            is_Rotated = True
            ctime.reset()
            ctime.curTime()

        elif direction == 'left' :
            print("left")
            M = cv.getRotationMatrix2D((cols/2,rows/2),90,1)
            dst = cv.warpAffine(image,M,(cols,rows))
            is_Rotated = True
            ctime.reset()
            ctime.curTime()

        elif direction == 'nothing'  :
            M = cv.getRotationMatrix2D((cols/2,rows/2),0,1)
            dst = cv.warpAffine(image,M,(cols,rows)) 

       
    return dst

def chosed_Scale(image,direction):
    print(direction)
    dimentions= image.shape
    print(dimentions)
    scale = 1.009
    # Zoom in تكبير
    if direction == 'right':
        src =cv.resize(image,(int(dimentions[1]*scale),int(dimentions[0]*scale)))
    # Zoom out تصغير
    elif direction == 'left':
        src =cv.resize(image,(int(dimentions[1]/scale),int(dimentions[0]/scale)))

    elif direction == 'nothing':
        src =cv.resize(image,(int(dimentions[1]),int(dimentions[0])))

    return src

def chosed_Scale_MULT2(image,direction):
    global is_Scale ,src
    dimentions= image.shape
    scale = 2
    if not is_Scale:
        if direction == 'right' :
            print('right')
            src =cv.resize(image,(int(dimentions[1]*scale),int(dimentions[0]*scale))) 
            is_Scale = True
            ctime.reset()
            ctime.curTime()
        elif direction == 'left' :
            print("left")
            src =cv.resize(image,(int(dimentions[1]/scale),int(dimentions[0]/scale)))
            is_Scale = True
            ctime.reset()
            ctime.curTime()
        elif direction == 'nothing'  :
            src =cv.resize(image,(int(dimentions[1]),int(dimentions[0]))) 
    return src