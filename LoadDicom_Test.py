# -*- coding: utf-8 -*-

from LoadDicom import LoadDicom

img = LoadDicom('E:\\Organized\\Programming\\Sample_codes\\Kaggle\\Cancer detection\\00cba091fa4ad62cc3200a657aeb957e')

import cv2

cv2.imshow('Image 10', img[:,:,10])
cv2.waitKey(0)
