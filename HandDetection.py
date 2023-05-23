import cv2 as cv
import numpy as np
import math
import removeBackground as rBG
import StackImage as stack
import copy
import ctime
import step as st
from read_Image import Image_Read
import Drawing as draw
import uuid

image = Image_Read.getImage()
image_did_read=False
blurValue = 17
threshold = 60 
extra_time = 4

finger_zero=True
finger_one=True
finger_two=True
finger_three= True
finger_four= True
finger_five= True
finger_chosed = True

restart_project = True
end_of_processing = False

Values_first_axis_x = 0
Values_end_axis_x = 0
bool_first_axis_x = False
bool_end_axis_x = False

axis_x = 0
# axis_y = 0
# axis_center = 0

checktType = "No Type"
def numberFingers(cnt,drawing,areacnt,arearatio):
    font = cv.FONT_HERSHEY_SIMPLEX
    number_hand = 0
    if cnt==1:
        if areacnt<2000:
            number_hand = -1
            cv.putText(drawing,'Put hand in the box',(0,50), font, 2, (0,0,255), 3, cv.LINE_AA)
        else:
            if arearatio<12:
                number_hand = 0
                cv.putText(drawing,'0',(0,50), font, 2, (0,0,255), 3, cv.LINE_AA)
            # elif arearatio<17.5:
            #     number_hand = 1
            #     cv.putText(drawing,'1',(0,50), font, 2, (0,0,255), 3, cv.LINE_AA)
            
            else:
                number_hand = 1
                cv.putText(drawing,'1',(0,50), font, 2, (0,0,255), 3, cv.LINE_AA)
            
    elif cnt==2:
        number_hand = cnt
        cv.putText(drawing,'2',(0,50), font, 2, (0,0,255), 3, cv.LINE_AA)
        
    elif cnt==3:
        number_hand = cnt
        if arearatio<27:
            cv.putText(drawing,'3',(0,50), font, 2, (0,0,255), 3, cv.LINE_AA)
        else:
            cv.putText(drawing,'3',(0,50), font, 2, (0,0,255), 3, cv.LINE_AA)
                
    elif cnt==4:
        number_hand = cnt
        cv.putText(drawing,'4',(0,50), font, 2, (0,0,255), 3, cv.LINE_AA)
        
    elif cnt==5:
        number_hand = cnt
        cv.putText(drawing,'5',(0,50), font, 2, (0,0,255), 3, cv.LINE_AA)
        
    else :
        number_hand = 6
        cv.putText(drawing,'reposition',(10,50), font, 2, (0,0,255), 3, cv.LINE_AA)
    
    return number_hand

def calculateFingers(res,drawing,areacnt,arearatio):  # -> finished bool, cnt: finger count
    global axis_x

    hull = cv.convexHull(res, returnPoints=False)
    defects = cv.convexityDefects(res, hull)
    if type(defects) != type(None):  # avoid crashing.   (BUG not found)
        cnt = 0
        for i in range(defects.shape[0]):  # calculate the angle
            s, e, f, d = defects[i][0]
            start = tuple(res[s][0])
            end = tuple(res[e][0])
            far = tuple(res[f][0])
            a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
            b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
            c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
            angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))  # cosine theorem
            if angle <= math.pi / 2:  # angle less than 90 degree, treat as fingers
                cnt += 1
                cv.circle(drawing, far, 5, [211, 84, 0], -1)
                cv.circle(drawing, start, 5, [0, 175,0], -1)
                cv.circle(drawing, end, 5, [0, 175, 0], -1)

            # cv.line(drawing,start, end, [255,255,0], 2)
            moments = cv.moments(res) 
            if moments['m00'] == 0 :moments['m00'] = 1
            ((x, y), radius) = cv.minEnclosingCircle(res)
            center = (int(moments['m10'] / moments['m00']),int(moments['m01'] / moments['m00']))
            # print("(x,y)"+str(x),str(y))
            if radius > 0.5:
                # cv.circle(drawing, (int(x), int(y)), int(radius), (255, 0, 0), 2)
                cv.circle(drawing, center, 5, (0, 0,255), -1)
                axis_x = int(x)
                axis_y = int(y)
                axis_center = center

            # cv.line(drawing,moments['m00'], start, [255,255,0], 1)
            # cv.line(drawing,center, end, [255,255,0], 2)
        cnt+=1
        numFing = numberFingers(areacnt=areacnt,arearatio=arearatio,drawing=drawing,cnt=cnt)
        return numFing
    return -1

def resetVariable():
    global finger_zero , finger_one , finger_two , finger_three , finger_chosed , checktType
    global axis_x  ,Values_first_axis_x , Values_end_axis_x , bool_first_axis_x , bool_end_axis_x , end_of_processing
    # finger_zero = True
    finger_zero=True
    finger_one=True
    finger_two=True
    finger_three= True
    finger_chosed = True
    checktType = 'No Type'

    axis_x = 0
    Values_first_axis_x = 0
    Values_end_axis_x = 0
    bool_first_axis_x = False
    bool_end_axis_x = False
    end_of_processing = False
    st.is_Rotated = False

def startProject(cnt,frame):
    global finger_zero , finger_one , finger_two,finger_three ,finger_four , finger_five ,finger_chosed , restart_project
    global checktType
    global bool_first_axis_x,bool_end_axis_x ,Values_first_axis_x , Values_end_axis_x ,axis_x
    global end_of_processing
    global image
    if restart_project:
        if ctime.cur_time+extra_time <= ctime.nowTime() and finger_zero and cnt == 0  :
            print("**** Translation    ( 1 ) ****")
            print("**** Rotete         ( 2 ) ****")
            print("**** Scale          ( 3 ) ****")
            print("**** Paint          ( 4 ) ****")
            print("**** Saved Image    ( 5 ) ****")

            finger_zero = False
            ctime.reset()
            ctime.curTime()

        if not finger_zero and cnt >=1 and cnt <= 5:
            if cnt == 1 and finger_one and finger_chosed :
                if ctime.cur_time+extra_time <= ctime.nowTime() :
                    print("Translation")
                    finger_one ,finger_chosed= False , False
                    checktType = 'Translation'

            if cnt == 2 and finger_two and finger_chosed:
                if ctime.cur_time+extra_time <= ctime.nowTime() :
                    print("Rotate")
                    finger_two,finger_chosed = False , False
                    checktType = 'Rotate'

                    
            if cnt == 3 and finger_three and finger_chosed:
                if ctime.cur_time+extra_time <= ctime.nowTime() :
                    print("Scale")
                    finger_three,finger_chosed = False , False
                    checktType = 'Scale'

            if cnt == 4 and finger_four and finger_chosed:
                if ctime.cur_time+extra_time <= ctime.nowTime() :
                    print("Paint")
                    finger_four,finger_chosed = False , False
                    cv.destroyAllWindows()
                    drawing = draw.drawingCanvas()
                    drawing.draw()

            if cnt == 5 and finger_five and finger_chosed:
                if ctime.cur_time+extra_time <= ctime.nowTime() :
                    # outfile = '%s/%s.png' % ("image","A")
                    outfile = '%s/%s.jpg' % ("saveImage", str(uuid.uuid4()))
                    isWritten = cv.imwrite(outfile,image)
                    if isWritten:
                        print("*** Saved Image Success ***")
                        finger_five,finger_chosed = False , False
                        resetVariable()
                    

                    

        if checktType != 'No Type' and not end_of_processing:
            if not bool_first_axis_x  and cnt == 5:
                Values_first_axis_x = axis_x
                # print("Fist : " + str(Values_first_axis_x))
                bool_first_axis_x = True
            
            if not bool_end_axis_x and bool_first_axis_x and (cnt == 4 or cnt == 3 or cnt ==2 or cnt ==1 or cnt == 5) :
                Values_end_axis_x = axis_x


            if bool_first_axis_x and not bool_end_axis_x :
                direction = st.Determine_The_Direction(Values_first_axis_x , Values_end_axis_x)
                
                if checktType == 'Translation':
                    image = st.chosed_Translate(image,direction)
                    if cnt == 0  and not end_of_processing:
                        end_of_processing = True
                        resetVariable()
                        print("Final Translation")

                if checktType == 'Rotate':
                    if cnt == 0  and not end_of_processing and cnt != -1:
                        image = st.chosed_Rotate(image,direction)
                        if ctime.cur_time +1 <= ctime.nowTime():
                            st.is_Rotated = False

                    if cnt == -1 and not end_of_processing:
                        end_of_processing = True
                        resetVariable()
                        print("Final Rotate")
                
                
                if checktType == 'Scale':
                    image = st.chosed_Scale(image,direction)
                    if cnt == 0  and not end_of_processing:
                        end_of_processing = True
                        resetVariable()
                        print("Final Scale")

                # if checktType == 'Scale':
                #     if cnt == 0  and not end_of_processing and cnt != -1:
                #         image = st.chosed_Scale_MULT2(image,direction)
                #         if ctime.cur_time +1 <= ctime.nowTime():
                #             st.is_Scale = False

                #     if cnt == -1 and not end_of_processing:
                #         end_of_processing = True
                #         resetVariable()
                #         print("Final Scale")


def hand_Detection(bgModel,frame,cap_region_y_end,cap_region_x_begin):
  global image
  global image_did_read
  if not image_did_read:
        image = Image_Read.getImage()
        image_did_read=True

  img = rBG.removeBG(bgModel,frame)
  img = img[0:int(cap_region_y_end * frame.shape[0]),int(cap_region_x_begin * frame.shape[1]):frame.shape[1]]
  # cv.imshow('mask',img)

  gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY) 
  blur = cv.GaussianBlur(gray,(blurValue,blurValue),0)
  # cv.imshow('blur',blur)
  ret, thresh = cv.threshold(blur, threshold, 255, cv.THRESH_BINARY)
  # cv.imshow('binary',thresh)
  thresh1 = copy.deepcopy(thresh)
  #RETR_EXTERNAL
  contours,hierarchy = cv.findContours(thresh1,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)#Find the outline Note

  length = len(contours)
  maxArea = -1
  if length > 0:
    for i in range(length): # Find the largest contour (according to area)  ابحث عن أكبر محيط (حسب المنطقة)
      temp = contours[i]
      area = cv.contourArea(temp) #Calculate the area of the contour region احسب مساحة منطقة الكنتور
      if area > maxArea:
        maxArea = area
        ci = i

    res = contours[ci] #get the largest contour area الحصول على أكبر مساحة كفاف

    epsilon = 0.0005*cv.arcLength(res,True)
    approx= cv.approxPolyDP(res,epsilon,True)

    #Returns the convex hull of the set of points (points that make up the contour) 
    # إرجاع الهيكل المحدب لمجموعة النقاط (النقاط التي تشكل المحيط)
    hull = cv.convexHull(res) 

    areahull = cv.contourArea(hull)
    areacnt = cv.contourArea(res)
    if areacnt == 0 : areacnt =1
    arearatio=((areahull-areacnt)/areacnt)*100
    drawing = np.zeros(img.shape,np.uint8)
  
    cv.drawContours(drawing,[res],0,(255,0,0),1)
    cv.drawContours(drawing,[hull],0,(0,0,255),1)

    cnt= calculateFingers(approx,drawing,areacnt,arearatio)
    startProject(cnt=cnt,frame = frame)
# [['img','blur'],['thresh','drawing']]

    Stacked= stack.stackImages(([img , blur],[thresh,drawing]),0.6)


    cv.imshow('Stacked',Stacked)
    cv.imshow('Image',image)
    
