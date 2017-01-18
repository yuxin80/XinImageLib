# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 17:36:51 2017

@author: XYu4
"""

"""
Load the Dicom files as numpy array
"""
def LoadDicom(folderName):
    import dicom
    import numpy
    import os
    
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

