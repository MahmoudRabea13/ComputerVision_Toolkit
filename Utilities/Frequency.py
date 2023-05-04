import matplotlib.pyplot as plt
import numpy as np
import cv2
import random
from scipy import ndimage
from scipy import signal

class Frequency():
    def hybrid(self,image1,image2,r1,r2):
        """image1: high filter image
        image2: low pass image"""
        image1 = self.low_high_pass(image1,'low',r1)
        image2 = self.low_high_pass(image2,'high',r2)
        new_image = image1+image2
        return new_image
    def thres_finder(self,img, thres=20, delta_T=1.0):
        # Step-2: Divide the images in two parts
            x_low, y_low = np.where(img <= thres)
            x_high, y_high = np.where(img > thres)

        # Step-3: Find the mean of two parts
            mean_low = np.mean(img[x_low, y_low])
            mean_high = np.mean(img[x_high, y_high])

        # Step-4: Calculate the new threshold
            new_thres = (mean_low + mean_high)/2

        # Step-5: Stopping criteria, otherwise iterate
            if abs(new_thres-thres) < delta_T:
                return new_thres
            else:
                return self.thres_finder(self,img, thres=new_thres, delta_T=1.0)


    def global_threshold(self,image, thres_value, val_high, val_low):
        img = image.copy()
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                if image[i, j] > thres_value:
                    img[i, j] = val_high
                else:
                    img[i, j] = val_low
        return img


    def local_threshold(self,image, size):
        img = image.copy()
        i = 0
        j = 0
        while i < img.shape[0]:
            j = 0
            while j < img.shape[1]:
                x = i
                mean = 0
                cnt = 0
                while x < img.shape[0] and x < i+size:
                    y = j
                    while y < img.shape[1] and y < j+size:
                        cnt = cnt+1
                        mean = mean+img[x, y]
                        y = y+1
                    x = x+1
                mean = mean/(cnt)
                x = i
                while x < img.shape[0] and x < i+size:
                    y = j
                    while y < img.shape[1] and y < j+size:
                        if img[x, y] <= mean-5:
                            img[x, y] = 0
                        else:
                            img[x, y] = 255
                        y = y+1
                    x = x+1
                j = j+size
            i = i+size
        return img