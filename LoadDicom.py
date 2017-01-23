# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 17:36:51 2017

@author: Yu Xin
"""

"""
Load the Dicom files as numpy array
Assume all the slices of one scan are stored in the same folder
"""
import dicom
import numpy
import os

"""
folder = ''
patients = os.listdir(folder)
patients.sort()    
"""

def LoadDicom(folderName):

    PathDicom = folderName
    lstFilesDicom = []
    for dirName, subDirList, fileList in os.walk(PathDicom):
        for fileName in fileList:
            if ".dcm" in fileName.lower():
                lstFilesDicom.append(os.path.join(dirName,fileName))
                
    RefDs = dicom.read_file(lstFilesDicom[0])
    
    #Load dimensions based on the number of rows
    constPixelDims = (int(RefDs.Rows), int(RefDs.Columns), len(lstFilesDicom))
    
    #Load spacing values (in mm)
    #constPixelSpacing = (float(RefDs.PixelSpacing[0]), float(RefDs.PixelSpacing[1]),float(RefDs.SliceThickness))
    
    """
    x=numpy.arange(0.0, (constPixelDims[0]+1)*constPixelSpacing[0],constPixelSpacing[0])
    y=numpy.arange(0.0, (constPixelDims[1]+1)*constPixelSpacing[1],constPixelSpacing[1])
    z=numpy.arange(0.0, (constPixelDims[2]+1)*constPixelSpacing[2],constPixelSpacing[2])
    """
    
    ArrayDicom = numpy.zeros(constPixelDims,dtype=RefDs.pixel_array.dtype)
    
    for filename in lstFilesDicom:
        ds = dicom.read_file(filename)
        ArrayDicom[:,:,lstFilesDicom.index(filename)] = ds.pixel_array
    
    return ArrayDicom

def load_scan(path):
    slices = [dicom.read_file(path+'\\'+s) for s in os.listdir(path)]
    slices.sort(key=lambda x: int(x.InstanceNumber))
    try:
        slice_thickness = numpy.abs(slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])
    except:
        slice_thickness = numpy.abs(slices[0].SliceLocation-slices[1].SliceLocation)
        
    for s in slices:
        s.SliceThickness = slice_thickness
        
    return slices

