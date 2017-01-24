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
import scipy

import matplotlib.pyplot as plt
from skimage import measure, morphology 
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

"""
folder = ''
patients = os.listdir(folder)
patients.sort()    
"""

def loadDicom(folderName):

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

def get_pixels_hu(scans):
    image = numpy.stack([s.pixel_array for s in scans])
    
    image = image.astype(numpy.int16)
    
    image[image == -2000] =0
    
    intercept = scans[0].RescaleIntercept
    
    slope = scans[0].RescaleSlope
    
    if slope !=1:
        image = slope*image.astype(numpy.float64)
        image = image.astype(numpy.int16)
        
    image += numpy.int16(intercept)
    
    return numpy.array(image, dtype=numpy.int16)
        
def resample(image, scan, new_spacing=[1,1,1]):
    # Determine current pixel spacing
    spacing = map(float, ([scan[0].SliceThickness] + scan[0].PixelSpacing))
    spacing = numpy.array(list(spacing))

    resize_factor = spacing / new_spacing
    new_real_shape = image.shape * resize_factor
    new_shape = numpy.round(new_real_shape)
    real_resize_factor = new_shape / image.shape
    new_spacing = spacing / real_resize_factor
    
    image = scipy.ndimage.interpolation.zoom(image, real_resize_factor)
    
    return image, new_spacing

def plot_3d(image, threshold=-300):
    p = image.transpose(2,1,0)
    p=p[:,:,::-1]
    
    verts, faces = measure.marching_cubes(p,threshold)
    
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111,projection='3d')
    
    mesh = Poly3DCollection(verts[faces], alpha=0.1)
    face_color = [0.5,0.5,1]
    mesh.set_facecolor(face_color)
    ax.add_collection3d(mesh)
    
    ax.set_xlim(0,p.shape[0])
    ax.set_ylim(0,p.shape[1])
    ax.set_zlim(0,p.shape[2])
    
    plt.show()
