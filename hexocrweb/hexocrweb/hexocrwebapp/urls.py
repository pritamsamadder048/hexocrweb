
from django.conf.urls import url,include
from django.contrib import admin
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^getlicensedatauk/$', views.GetLicenseDataUK.as_view(),name="getlicenseDatauk"),
    #url(r'^index/$', views.index,name="index"),
    url(r'^index/$', TemplateView.as_view(template_name="hexocrwebapp/index.html"),name="index"),
    #url(r'^$', views.index,name="index"),
    url(r'^$', TemplateView.as_view(template_name="hexocrwebapp/index.html"),name="index"),
    url(r'^processimagetotext/$', views.ProcessImageToText,name="processimagetotext"),
    #url(r'^processlicenseimageuk/$', views.processLicenseImageUK,name="processlicenseimageuk"),

    url(r'^gettextfromimage/$', views.GetTextFromImage.as_view(),name="gettextfromimage"),

]



