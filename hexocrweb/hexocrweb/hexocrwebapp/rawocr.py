from PIL import Image
import pytesseract
import cv2
import numpy as np
import sys, os
import re
from pylab import array, plot, show, axis, arange, figure, uint8

DEBUG = True


def Log(debug=False, msg=None, *args):
    if (debug):

        if (msg):

            print(msg)  # "debug :",debug," , ",
            for a in args:
                print(a)
            print()
            print()
        else:
            print()
            print()


# extract text from licenseid
def getTextFromImage(img, tesseract_path=None,converttogray=True):
    ret = False
    message = ""
    text = None

    if "nt" in os.name and tesseract_path == None:
        tesseract_path = r'C:/Program Files (x86)/Tesseract-OCR/tesseract'
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
    elif "posix" in os.name and tesseract_path == None:
        tesseract_path = "/usr/local/bin/tesseract"
        pytesseract.pytesseract.tesseract_cmd = tesseract_path

    try:

        blurval=cv2.Laplacian(img, cv2.CV_64F).var()
        print("\n\nBlur Value : {0}\n\n".format(blurval))
        # if (not blurval > 100):
        #     ret = False
        #     message = "this image is too blurry"
        #     return (ret, message, text)

        if(converttogray):
            grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            grey=img.copy()

        print("constructing image from data")
        pilimg = Image.fromarray(img)

        print("extracting text from image")
        print("type of pilimg : ", type(pilimg))
        text = pytesseract.image_to_string(pilimg)

        ret = True
        message = "successfully extracted data"
        Log(DEBUG, message)
        Log()
        Log()
        print("succesfully extracted text from image")
        return (ret, message,text)

    except Exception as e:
        ret = False
        message = e.__str__()
        text = None

        Log(DEBUG, "error occured while processing image data")
        Log(DEBUG, "error : ", e.__str__())

        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print("error occured while processing image data")
        return (ret, message, text)


def getLChannelOfLAB(img):
    try:
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        ret=True
        message=None
        return (ret, message, l)
    except Exception as e:

        ret = False
        message = e.__str__()
        l=None
        #text = None

        print("error occured while getting L channel value")
        print("error : ", e.__str__())

        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print("error occured while processing image data")
        return (ret, message, l)


def IncreaseContrastAndBrightness_phi_thetta(img,phi = 1,theta = 1,maxIntensity = 255.0):
    try:
        newImage1 = (maxIntensity / phi) * (img / (maxIntensity / theta)) ** 2
        img = array(newImage1, dtype=uint8)
        ret = True
        message = None
        return (ret, message, img)
    except Exception as e:

        ret = False
        message = e.__str__()
        img=None
        #text = None

        print("error occured while getting L channel value")
        print("error : ", e.__str__())

        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print("error occured while processing image data")
        return (ret, message, img)


def IncreaseContrastAndBrightness_ALPHA_BETA(img,alpha=3,beta=10):
    try:
        r = cv2.addWeighted(img, alpha, np.zeros(img.shape, img.dtype), 0, beta)
        ret = True
        message = None
        return (ret, message, r)
    except Exception as e:

        ret = False
        message = e.__str__()
        r=None
        #text = None

        print("error occured while adding alpha :{0} and beta : {1} value".format(alpha,beta))
        print("error : ", e.__str__())

        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        #print("error occured while processing image data")
        return (ret, message, r)



def ThresholdImage(img,threshold=100,low=0,high=255,grayscale=True):

    try:
        if(grayscale):
            gimg=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            for k in range(0, img.shape[0]):
                for l in range(0, img.shape[1]):
                    if (gimg[k, l] < threshold):
                        gimg[k,l] = 0
                    else:
                        gimg[k, l] = 255
        else:
            gimg  = img.copy()
            for k in range(0, img.shape[0]):
                for l in range(0, img.shape[1]):
                    if (gimg[k, l] < threshold):
                        gimg[k, l] = low
                    else:
                        gimg[k, l] = high
        ret=True
        message=None
        return (ret,message,gimg)
    except Exception as e:
        ret = False
        message = e.__str__()
        gimg = None
        # text = None

        print("error occured while Thresholding")
        print("error : ", e.__str__())

        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        # print("error occured while processing image data")
        return (ret, message, gimg)

def GetBrightnessAndBlurValue(img):
    try:
        blurval=0
        hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        bval = v.sum()
        blurval = cv2.Laplacian(img, cv2.CV_64F).var()
        return bval,blurval
    except Exception as e:
        v=0
        print("error occured getting brightness value")
        print("error : ", e.__str__())

        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        # print("error occured while processing image data")
        del(hsv)
        bval=v.sum()
        return  bval,blurval
