from PIL import Image
import pytesseract
import cv2
import numpy as np
import sys, os
import re

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
def getTextFromImage(img, tesseract_path=None):
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

        if (not cv2.Laplacian(img, cv2.CV_64F).var() > 350):
            ret = False
            message = "this image is too blurry"
            return (ret, message, text)

        grey_id = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

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
        return (ret, message, text)

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
