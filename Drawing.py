import cv2
import numpy as np
import StackImage as stack
from read_Image import Image_Read
import uuid
import ctime
class drawingCanvas():
    def __init__(self):
        self.penrange = np.load('penrange.npy')
        self.cap = cv2.VideoCapture(0)

        self.canvas = None
        self.imgcanvas = None

        self.image = Image_Read.getImage()
        self.h,self.w = self.image.shape[:2]

        self.x1,self.y1=0,0
        self.val=1
        self.colors = [(0,0,0) , (255 * self.val, 0, 0), (0, 255* self.val, 0), (0, 0, 255* self.val), (0, 255* self.val, 255* self.val)]
        self.color = 1
        self.fontSize = 10
        self.extra_time = 3
        # self.draw()

    def draw(self):
        while True:
            _, self.frame = self.cap.read()
            self.frame = cv2.resize(self.frame, (self.w, self.h)) 
            
            self.frame = cv2.flip( self.frame, 1 )
            self.image = Image_Read.restart_point()
            if self.canvas is None:
                self.canvas = np.zeros_like(self.frame)
                self.imgcanvas = np.zeros_like(self.image)

            mask=self.CreateMask()
            contours=self.ContourDetect(mask)
            self.drawLine(contours)
            self.paintWindow()
            self.display()
            k = cv2.waitKey(1) & 0xFF
            self.takeAction(k)
            if k == 27:
                break        

    def CreateMask(self):
        hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV) 
        lower_range = self.penrange[0]
        upper_range = self.penrange[1]
        mask = cv2.inRange(hsv, lower_range, upper_range)
        return mask


    def ContourDetect(self,mask):
        # Find Contours
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours
    
    def drawLine(self,contours):

        #if contour area is not none and is greater than 100 draw the line
        if contours and cv2.contourArea(max(contours, key = cv2.contourArea)) > 100:                
            c = max(contours, key = cv2.contourArea)    
            x2,y2,w,h = cv2.boundingRect(c)
            if self.x1 == 0 and self.y1 == 0:
                self.x1,self.y1= x2,y2
            else:
                # Draw the line on the canvas
                self.canvas = cv2.line(self.canvas, (self.x1,self.y1),(x2,y2), self.colors[self.color], self.fontSize)
                self.imgcanvas = cv2.line(self.imgcanvas, (self.x1,self.y1),(x2,y2), self.colors[self.color], self.fontSize)
                self.image = cv2.line(self.image, (self.x1,self.y1),(x2,y2), self.colors[self.color], self.fontSize)

            #New point becomes the previous point 
            self.x1,self.y1= x2,y2
        else:
            # If there were no contours detected then make x1,y1 = 0 (reset)
            self.x1,self.y1 =0,0        

    def axis_point(self,x1,x2,y1,y2,pointX,pointY,color,size):
        self.colors = [(0,0,0),(255 * self.val, 0, 0), (0, 255* self.val, 0), (0, 0, 255* self.val), (0, 255* self.val, 255* self.val)]

        if pointX in range(x1,x2+1) and pointY in range(y1,y2+1) :
            if color == -1 :
                if self.fontSize == 1 :
                    self.fontSize = 2
                else :
                    self.fontSize = size
            elif color == -2 :
                self.canvas = np.zeros_like(self.frame)
                self.imgcanvas = np.zeros_like(self.image)
            elif color == -3 :
                self.image = Image_Read.restart_point()
                self.image = cv2.add(self.imgcanvas,self.image)

                if ctime.cur_seconds+self.extra_time <= ctime.nowSeconds():
                    outfile = '%s/%s.jpg' % ("saveImage", str(ctime.nowSeconds()))
                    isWritten = cv2.imwrite(outfile,self.image)
                    if isWritten :
                        ctime.cSeconds()
                        print("*** Saved Image Success ***")

                    

            else : 
                self.color = color


        

    def paintWindow(self):
        
        paintWindow = np.zeros((471,636,3)) + 255
        paintWindow = cv2.rectangle(self.image, (0,1), (80,50), self.colors[0], 2) # Erase
        paintWindow = cv2.rectangle(self.image, (90,1), (170,50), self.colors[1], -1)# blue
        paintWindow = cv2.rectangle(self.image, (180,1), (260,50), self.colors[2], -1)# green
        paintWindow = cv2.rectangle(self.image, (270,1), (350,50), self.colors[3], -1)# red
        paintWindow = cv2.rectangle(self.image, (360,1), (440,50), self.colors[4], -1)# yellow

        paintWindow = cv2.rectangle(self.image, (450,1), (520,50), (255,255,255), -1)   # Clear All
        paintWindow = cv2.rectangle(self.image, (540,1), (630,50), (128,128,128), -1)   # SaveImage

        paintWindow = cv2.rectangle(self.image, (0,430), (60,480), self.colors[0], 2)   # +
        paintWindow = cv2.rectangle(self.image, (550,430), (610,480), self.colors[0], 2)   # -

        


        cv2.putText(paintWindow, "Erase", (2, 30), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(paintWindow, "BLUE", (95, 30), cv2.FONT_ITALIC, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(paintWindow, "GREEN", (185, 30), cv2.FONT_ITALIC, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(paintWindow, "RED", (275, 30), cv2.FONT_ITALIC, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(paintWindow, "YELLOW", (365, 30), cv2.FONT_ITALIC, 0.5, (255,255,255), 2, cv2.LINE_AA)
        cv2.putText(paintWindow, "ClearAll", (455, 30), cv2.FONT_ITALIC, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(paintWindow, "Save", (545, 30), cv2.FONT_ITALIC, 0.5, (255,255,255), 2, cv2.LINE_AA)
        cv2.putText(paintWindow, "+", (20, 463), cv2.FONT_ITALIC, 0.5, (0,0,255), 4, cv2.LINE_AA)
        cv2.putText(paintWindow, "-", (575, 463), cv2.FONT_ITALIC, 0.5, (0,0,255), 4, cv2.LINE_AA)


        self.axis_point(x1 = 0   ,  y1 = 1 , x2 = 80 , y2 = 50 , pointX = self.x1 , pointY = self.y1 , color = 0  , size= self.fontSize) # Eras
        self.axis_point(x1 = 90  ,  y1 = 1 , x2 = 170 , y2 = 50 , pointX = self.x1 , pointY = self.y1 , color = 1 , size= self.fontSize) # Blue
        self.axis_point(x1 = 180 ,  y1 = 1 , x2 = 260 , y2 = 50 , pointX = self.x1 , pointY = self.y1 , color = 2 , size= self.fontSize) # Green
        self.axis_point(x1 = 270 ,  y1 = 1 , x2 = 350 , y2 = 50 , pointX = self.x1 , pointY = self.y1 , color = 3 , size= self.fontSize) # Red
        self.axis_point(x1 = 360 ,  y1 = 1 , x2 = 440 , y2 = 50 , pointX = self.x1 , pointY = self.y1 , color = 4 , size= self.fontSize) # Yellow
        self.axis_point(x1 = 450 ,  y1 = 1 , x2 = 520 , y2 = 50 , pointX = self.x1 , pointY = self.y1 , color = -2 , size= self.fontSize) #Clear All
        self.axis_point(x1 = 540 ,  y1 = 1 , x2 = 630 , y2 = 50 , pointX = self.x1 , pointY = self.y1 , color = -3 , size= self.fontSize) #Save Image
        self.axis_point(x1 = 0 ,  y1 = 430 , x2 = 60 , y2 = 480 , pointX = self.x1 , pointY = self.y1 , color = -1 , size= self.fontSize + 1) # +
        self.axis_point(x1 = 550 ,  y1 = 430 , x2 = 610 , y2 = 480 , pointX = self.x1 , pointY = self.y1 , color = -1 , size= self.fontSize - 1) # -
        
       
        # paintWindow = cv2.rectangle(self.image, (540,1), (630,50), (128,128,128), -1)   # SaveImage


  
       
    
    def display(self):
        # Merge the canvas and the frame.

        # self.frame = cv2.add(self.frame,self.canvas)
        self.image = cv2.add(self.imgcanvas,self.image)

        # Stacked= stack.stackImages(([self.image , self.frame],[self.canvas,self.imgcanvas]),0.6)

        Stacked= np.hstack([self.image , self.frame])
        cv2.imshow('Stacked',Stacked)

    def takeAction(self,k):
        # When c is pressed clear the entire canvas
        if k == ord('c'):
            self.canvas = None
            self.imgcanvas = None
        #press e to change between eraser mode and writing mode
        if k==ord('e'):
            self.val= int(not self.val)

                   
# if __name__ == '__main__':
#     drawingCanvas()
    
cv2.destroyAllWindows()
