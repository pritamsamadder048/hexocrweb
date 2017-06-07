from django.shortcuts import render

from django.http import HttpResponse



import datetime
import  sys,os

import urllib
from urllib.request import urlopen




from  django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import  Response
from  rest_framework import  status
from rest_framework import generics
from rest_framework import views




import cv2
import numpy as np
from .drivinglicenseocruk import *
from .rawocr import *
import urllib
from urllib.request import urlopen

import json


from django.core.mail import get_connection, send_mail
from django.core.mail.message import EmailMessage
from django.core.mail import EmailMessage




DEBUG=True

# returned test data : "dob":"01.01.1982","firstname":"ABWJAA","address":"FLAT 2, 19A KENDAL PARADE, SILVER STREET, LONDON, N18 1ND","lastname":"ABDI","licenseid":"ABDI9801012A99FW 56","expirydate":"22,08,2021"


def Log(msg=None, *args):
    if (DEBUG):

        if (msg):

            print(msg)
            for a in args:
                print(a)
            print()
            print()
        else:
            print()
            print()



def _grab_image(path=None, stream=None, url=None):

    try:
        # if the path is not None, then load the image from disk
        print("in _grab_image")
        print("url : ",url)
        print("path : ",path)
        print("stream : ",stream)
        if path is not None and (("http://" not in path)  or ("https://" not in path)):
            image = cv2.imread(path)
        elif path is not None and (("http://"  in path)  or ("https://"  in path)):
            print("it is a url : ",path)
            req = urllib.urlopen(path)
            arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
            image = cv2.imdecode(arr,-1) # 'load it as it is'

        # otherwise, the image does not reside on disk
        else:
            print("in else : ")
            # if the URL is not None, then download the image

            if url is not None and url.strip() is not None:
                print("getting image from url : ",url)
                resp = urlopen(url)
                data = resp.read()

            # if the stream is not None, then the image has been uploaded
            elif stream is not None:
                print("getting image from stream..")
                data = stream.read()

            # convert the image to a NumPy array and then read it into
            # OpenCV format
            image = np.asarray(bytearray(data), dtype="uint8")
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        # return the image
        return image
    except Exception as e:
        print("error occured ")
        print("Error reading the image : ",e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print()
        return None
        

class GetLicenseDataUK(APIView):


    def post(self,request):
        img_data={}
        responsedata={}

        try:

            print("init post GetLicenseDataUK")
            for key in request.POST:
                img_data[key]=request.POST[key].strip()
            #print("img_data : ",img_data)
            if request.FILES.get("license_image", None) is not None:
                # grab the uploaded image
                img = _grab_image(stream=request.FILES["license_image"])
            elif img_data.get("license_image",None) is not None :
                imgpath=img_data["license_image"]
                print("img url : ",imgpath)
                img = _grab_image(url=imgpath)
            else:
                responsedata={"status":"error","message":"please provide a clear image"}
                return  Response(responsedata)

            ret, m, data = getTextFromLicenseId(img)
            if (ret):
                ret, m, fd = formatTextToUKPrivateLicense_2016(data)
                if(ret):
                    responsedata={"status":"ok","data":fd}
                    Log(m)
                    return  Response(responsedata)
                else:
                    responsedata = {"status": "error", "message": m}
                    Log("Error occured could not format the image data")
                    return Response(responsedata)
            else:
                responsedata={"status":"error","message":m}
                Log("Error occured could not process image")
                return  Response(responsedata)



        except Exception as e:
            responsedata={"status": "error", "message": "please provide a clear image"}
            print("error occured : ",e)
            if(DEBUG):
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
            return  Response(responsedata)


import pickle
from .models import ProcessingData
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image,ImageOps

class GetTextFromImage(APIView):


    def post(self,request):
        img_data={}
        responsedata={}

        try:

            print("init post GetTextFromImage")
            for key in request.POST:
                img_data[key]=request.POST[key].strip()
            #print("img_data : ",img_data)
            if request.FILES.get("image", None) is not None:
                # grab the uploaded image
                img = _grab_image(stream=request.FILES["image"])
            elif img_data.get("image",None) is not None :
                imgpath=img_data["image"]
                print("img url : ",imgpath)
                img = _grab_image(url=imgpath)
            else:
                responsedata={"status":"error","message":"please provide a clear image"}
                pd = ProcessingData()
                #simg = json.dumps(img)
                #pd.raw_ocr_image = simg
                #pd.extracted_data = data
                try:
                    pd.ocr_image = ConvertToDjnagoImage(img)
                except:
                    pass
                pd.status = responsedata["status"]
                pd.log=responsedata["message"]
                pd.save()
                return  Response(responsedata)

            ret, m, data = getTextFromImage(img)
            try:
                data=data.strip().replace("\n"," ")
            except:
                data=""
            if (ret):
                responsedata={"status":"ok","text":data}

                pd=ProcessingData()

                try:
                    pd.ocr_image = ConvertToDjnagoImage(img)
                except:
                    pass
                #simg=pickle.dumps(img, protocol=0)
                #pd.raw_ocr_image=simg
                pd.extracted_data=data
                pd.status=responsedata["status"]
                pd.save()


                print(responsedata)
                return Response(responsedata)
            else:
                responsedata={"status":"error","message":"Bad Image"}
                Log("Error occured could not process image")
                print(m)
                pd = ProcessingData()
                #simg = pickle.dumps(img, protocol=0)
                #pd.raw_ocr_image = simg
                try:
                    pd.ocr_image = ConvertToDjnagoImage(img)
                except:
                    pass
                pd.extracted_data = data
                pd.status = responsedata["status"]
                pd.log=responsedata["message"]
                pd.save()
                return  Response(responsedata)



        except Exception as e:
            responsedata={"status": "error", "message": "please provide a clear image"}
            print("error occured : ",e)
            if(DEBUG):
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)

            pd = ProcessingData()
            #simg = pickle.dumps(img, protocol=0)
            #pd.raw_ocr_image = simg
            try:
                pd.ocr_image = ConvertToDjnagoImage(img)
            except:
                pass
            pd.extracted_data = data
            pd.status = responsedata["status"]
            pd.log = responsedata["message"]
            pd.save()
            return  Response(responsedata)




def ConvertToDjnagoImage(img):
    try:
        img_io = BytesIO()
        pimg = Image.fromarray(img)
        # ltrb_border = (0, 0, 0, 10)
        # im_with_border = ImageOps.expand(pimg, border=ltrb_border, fill='white')
        # im_with_border.save(fp=img_io, format='JPEG')

        pimg.save(img_io, format="JPEG")

        b=img_io.getbuffer()
        imlen=len(b)
        del(b)
        img_file = InMemoryUploadedFile(img_io, None, 'ocr_beta.jpg', 'image/jpeg', imlen, None)

    except Exception as e:
        print("Error Occured trying to convert to django image : ",e)
        img_file=None
    finally:
        #img_io.close()
        return img_file







def ProcessImageToText(request):
    img_data={}
    responsedata={}
    urlpath = "hexocrwebapp/index.html"
    if request.method=='POST':

        try:

            print("init post ProcessImageToText")
            for key in request.POST:
                img_data[key]=request.POST[key].strip()
            print("img_data : ",img_data)
            if request.FILES.get("image", None) is not None:
                # grab the uploaded image
                print("grab image stream")
                img = _grab_image(stream=request.FILES["image"])
            elif img_data.get("image",None) is not None :
                imgpath=img_data["image"]
                print("img url : ",imgpath)
                img = _grab_image(url=imgpath)
            else:
                responsedata={"status":"error","message":"please provide a clear image"}
                pd = ProcessingData()
                #simg = json.dumps(img)
                #pd.raw_ocr_image = simg
                #pd.extracted_data = data
                try:
                    pd.ocr_image = ConvertToDjnagoImage(img)
                except:
                    pass
                pd.status = responsedata["status"]
                pd.log=responsedata["message"]
                pd.save()
                #return  Response(responsedata)

                return render(request, urlpath, {"data": None,"image":None, "status": responsedata["status"],"message":responsedata["message"]})

            ret, m, data = getTextFromImage(img)
            try:
                data=data.strip().replace("\n"," ")
            except:
                data=""
            if (ret):
                responsedata={"status":"ok","text":data}

                pd=ProcessingData()

                try:
                    pd.ocr_image = ConvertToDjnagoImage(img)

                except:
                    pass
                #simg=pickle.dumps(img, protocol=0)
                #pd.raw_ocr_image=simg
                pd.extracted_data=data
                pd.status=responsedata["status"]
                pd.save()

                try:
                    imurl = "http://139.59.20.175:8000" + pd.ocr_image.url
                except:
                    imurl=None


                print(responsedata)
                #return Response(responsedata)
                print({"data":pd.extracted_data, "image":imurl, "status": responsedata["status"], "message": None})
                return render(request, urlpath,{"data":pd.extracted_data, "image":imurl, "status": responsedata["status"], "message": None})
            else:
                responsedata={"status":"error","message":"Bad Image .. Try With other Image"}
                Log("Error occured could not process image")
                print(m)
                pd = ProcessingData()
                #simg = pickle.dumps(img, protocol=0)
                #pd.raw_ocr_image = simg
                try:
                    pd.ocr_image = ConvertToDjnagoImage(img)

                except:
                    pass
                pd.extracted_data = data
                pd.status = responsedata["status"]
                pd.log=responsedata["message"]
                pd.save()
                try:
                    imurl = "http://139.59.20.175:8000" + pd.ocr_image.url
                except:
                    imurl=None
                return render(request, urlpath,{"data":pd.extracted_data, "image":imurl, "status": responsedata["status"], "message": responsedata["message"]})
                #return  Response(responsedata)



        except Exception as e:
            responsedata={"status": "error", "message": "please provide a clear image"}
            print("error occured : ",e)
            if(DEBUG):
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)

            pd = ProcessingData()
            #simg = pickle.dumps(img, protocol=0)
            #pd.raw_ocr_image = simg
            try:
                pd.ocr_image = ConvertToDjnagoImage(img)

            except:
                pass
            pd.extracted_data = data
            pd.status = responsedata["status"]
            pd.log = responsedata["message"]
            pd.save()
            try:
                imurl = "http://139.59.20.175:8000"+pd.ocr_image.url
            except:
                imurl = None
            return render(request, urlpath,{"data":pd.extracted_data, "image":imurl, "status": responsedata["status"], "message": responsedata["message"]})
            #return  Response(responsedata)
    else:
        return render(request, urlpath, {"data": None, "image": None, "status": "notsubmitted","message": ""})



def index(request):


    urlpath="hexocrwebapp/index.html"

    try:



        # img_data={}
        # responsedata={}
        # print("yes it is post")

        return render(request,urlpath,{"data": None,"image":None , "status":"notsubmitted","message":""})



    except:
        return render(request, urlpath, {"data": None,"image":None , "status": "notsubmitted","message":""})



def processLicenseImageUK(request):
    
    if request.method=="POST":
        img_data={}
        urlpath=None
        
        try:

            for key in request.POST:
                img_data[key]=request.POST[key].strip()

            if request.FILES.get("license_image", None) is not None:
                # grab the uploaded image
                print("get image file")
                img = _grab_image(stream=request.FILES["license_image"])
            else:
                responsedata={"status":"error","message":"please provide a clear image"}
                return render(request,urlpath,{"data":{},"status":"provideimage","message":"please provide a clear image"})

            ret, m, data = getTextFromLicenseId(img)
            if (ret):
                ret, m, fd = formatTextToUKPrivateLicense_2016(data)
                if(ret):
                    responsedata={"status":"ok","data":fd}
                    Log(m)
                    return render(request,urlpath,{"data":fd,"status":"ok"})
                else:
                    responsedata = {"status": "error", "message": m}
                    Log("Error occured could not format the image data")
                    return render(request,urlpath,{"data":{},"status":"formattingerror","message": m})
            else:
                responsedata={"status":"error","message":m}
                Log("Error occured could not process image")
                return render(request,urlpath,{"data":{},"status":"processingerror","message":m})



        except Exception as e:
            
            responsedata={"status": "error", "message": "please provide a clear image"}
            print("error occured : ",e)
            if(DEBUG):
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
            return  Response(responsedata)
    else:
        return HttpResponse("<h1> GET NOT ALLOWED </h1>")
            

