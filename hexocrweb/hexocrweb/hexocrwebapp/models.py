from django.db import models
from django.core.validators import MaxValueValidator
import random
import hashlib
from datetime import datetime




def ocr_image_upload_location(instance,filename):
    return "ocr_image_beta/%s"%(filename)
class ProcessingData(models.Model):

    ocr_image=models.ImageField(upload_to=ocr_image_upload_location,
                                      null=True,
                                      blank=True,
                                      height_field="height_field",
                                      width_field="width_field")
    height_field = models.IntegerField(default=0,blank=True,null=True)
    width_field = models.IntegerField(default=0,blank=True,null=True)


    #raw_ocr_image=models.TextField(null=True,blank=True)

    extracted_data=models.TextField(null=True,blank=True)
    status=models.CharField(max_length=40)
    log=models.TextField(null=True,blank=True)
    process_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)



