import cv2 
import numpy as np

def removeBG(bgModel,frame): 

  #alculate the foreground mask احسب قناع المقدمة
    fgmask = bgModel.apply(frame,learningRate=0) 
    kernel = np.ones((3,3),np.uint8)
    #Erodes images using specific structuring elements. يعمل على تآكل الصور باستخدام عناصر هيكلية محددة.
    fgmask = cv2.erode(fgmask,kernel,iterations=1) 
    #Use a mask to remove a static background استخدم قناعًا لإزالة خلفية ثابتة
    res = cv2.bitwise_and(frame,frame,mask=fgmask) 
    return res