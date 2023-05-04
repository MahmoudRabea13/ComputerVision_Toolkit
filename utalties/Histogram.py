import matplotlib.pyplot as plt
import numpy as np
import cv2

import random
from scipy import ndimage
from scipy import signal

class Histogram():
        # Function to compute gray level histogram *distributive*
    def Gray_histogram_Compute(self,image):
        img_height = image.shape[0]
        img_width = image.shape[1]
        hist = np.zeros([256],np.int32)
        for x in range(0,img_height):
            for y in range(0,img_width):
                hist[image[x,y]] +=1
        return hist
    # plotting the gray scale histogram *distributive* 
    def Gray_histogram_Plot(self,histogram,path):
        plt.figure()
        plt.title("Histogram Distribution Curve")
        plt.xlabel("Brightness")
        plt.ylabel("number of Pixels")
        plt.xlim([0,256]) # As gray scale levels vary from 0 -> 256
        plt.plot(histogram,'gray')
        plt.savefig(path)
        return "Success"
    # histogram for RGB *distributive*
    def RGB_histogram(self,image):
        image_Height = image.shape[0]
        image_Width = image.shape[1]
        image_Channels = image.shape[2]
        histogram = np.zeros([256, image_Channels], np.int32)
        for x in range(0, image_Height):
            for y in range(0, image_Width):
                for c in range(0, image_Channels):
                        histogram[image[x,y,c], c] +=1
        return histogram
    #Plot the distributive RGB histogram each in separate plot
    def Plot_RGBHistogram(self,RGB_Histogram,path):
        # Separate Histograms for each color
        plt.subplot(3, 1, 1)
        plt.xlim([0, 256])
        plt.title("histogram of Blue")
        plt.plot(RGB_Histogram[:,0],'b')

        plt.subplot(3, 1, 2)
        plt.xlim([0, 256])
        plt.title("histogram of Green")
        plt.plot(RGB_Histogram[:,1],'g')
        
        plt.subplot(3, 1, 3)
        plt.xlim([0, 256])
        plt.title("histogram of Red")
        
        plt.plot(RGB_Histogram[:,2],'r')
        # for clear view
        plt.tight_layout()
        plt.savefig(path)
        return "success"
    # function to normalize the image
    def img_normalization(self,img):
        Min = np.min(img)
        Max = np.max(img)
        return (((img- Min)/((Max-Min)))) #stretching histogram equation from 0->255 to 0.0 -> 1.0
        # function to equalize the image
    def img_equalize(self,img):
        '''
        parameters:
        image: input image
        returns:
        img2: equalized image
        
        '''
        hist = self.Gray_histogram_Compute(Histogram,img)
        cdf = hist.cumsum()
        cdf_normalized = cdf * hist.max()/ cdf.max()
        cdf_m = np.ma.masked_equal(cdf,0)
        cdf_m = (cdf_m - cdf_m.min())*255/(cdf_m.max()-cdf_m.min())
        cdf = np.ma.filled(cdf_m,0).astype('uint8')
        img2 = cdf[img]
        return img2