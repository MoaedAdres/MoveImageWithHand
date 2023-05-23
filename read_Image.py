import cv2 as cv
import numpy

# imgs = ["image/black.jpeg" , "image/home.jpg", "image/logo.jpg", "image/messi.jpg" , "image/Lenna.jpg","image/image.jpg"]
# choseImage =1
class Image_Read():
    img = "image/messi.jpg"
    # @staticmethod
    def getImage():
        image = cv.imread (Image_Read.img)
        h,w = image.shape[:2]
        image = cv.resize(image,(w+100,h+100)) # w h
        return image
    # @staticmethod
    def restart_point():
        image = cv.imread (Image_Read.img)
        h,w = image.shape[:2]
        image = cv.resize(image,(w+100,h+100)) # w h
        return image





