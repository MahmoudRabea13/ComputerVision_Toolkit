import matplotlib.pyplot as plt
import numpy as np
import cv2
import random
from scipy import ndimage
from scipy import signal

class Filter():
    def __init__(self):
        pass
    def noisy(noise_typ, image):
        if noise_typ == "gaussian":
            row, col = image.shape
            mean = 0
            var = 0.1
            sigma = var**0.5
            gauss = np.random.normal(mean, sigma, (row, col))
            gauss = gauss.reshape(row, col)
            image = image + gauss
            return image

        elif noise_typ == "s&p":
            row, col = image.shape
            number_of_pixels = random.randint(300, 10000)
            for i in range(number_of_pixels):
                y_coord = random.randint(0, row - 1)
                x_coord = random.randint(0, col - 1)
                image[y_coord][x_coord] = 255
            number_of_pixels = random.randint(300, 10000)
            for i in range(number_of_pixels):
                y_coord = random.randint(0, row - 1)
                x_coord = random.randint(0, col - 1)
                image[y_coord][x_coord] = 0
                return image

        elif noise_typ == 'uniform':
            row, col = image.shape
            a = 0
            b = 0.2
            n = np.zeros((row, col), dtype=np.float64)
            for i in range(row):
                for j in range(col):
                    n[i][j] = np.random.uniform(a, b)
            image = image+n
            return image

    def padding(self,image):
        padded_image = np.zeros((image.shape[0]+2,image.shape[1]+2))
        padded_image[1:image.shape[0]+1,1:image.shape[1]+1]=image 
        return padded_image
    def gkernel(self,kernel_size=3, sig=2):
        ax = np.linspace(-(kernel_size - 1) / 2., (kernel_size - 1) / 2., kernel_size)
        xx, yy = np.meshgrid(ax, ax)
        kernel = np.exp(-0.5 * (np.square(xx) + np.square(yy)) / np.square(sig))
        return kernel / np.sum(kernel)
    def average_filter(self,image_data,filter_size=3):
        filter = np.ones((filter_size,filter_size))/(filter_size)**2
        new_img = np.zeros((image_data.shape[0],image_data.shape[1]))
        new_img = signal.convolve2d(image_data,filter,mode='same',boundary='fill',fillvalue=0)
        return new_img
    def median_filter(self,image_data,filter_size=3):
        new_img = np.zeros((image_data.shape[0],image_data.shape[1]))
        for i in range(image_data.shape[0]-1):
            for j in range(image_data.shape[1]-1):
                new_img[i][j] = np.median(image_data[i:i+filter_size,j:j+filter_size])
        return new_img
    def gaussian_filter(self,image,kernel_size=3,sigma=2):
        kernel = self.gkernel(self,kernel_size,sigma)
        new_img = np.zeros((image.shape[0],image.shape[1]))
        new_img = signal.convolve2d(image,kernel,mode='same',boundary='fill',fillvalue=0)
        return new_img
    def low_high_pass(self,image,selection='low',mask_size=20):
        x = image.shape[0]//2-mask_size
        y = image.shape[1]//2+mask_size
        img_fou = np.fft.fft2(image)
        img_fou = np.fft.fftshift(img_fou)
        if selection == "high":
            mask = np.ones((image.shape[0],image.shape[1]))
            mask[x:y,x:y] = 0
        elif selection == "low":
            mask = np.zeros((image.shape[0],image.shape[1]))
            mask[x:y,x:y] = 1
        new_fou = mask*img_fou
        new_fou = np.fft.ifftshift(new_fou)
        new_fou = np.fft.ifft2(new_fou)
        return np.abs(new_fou)
    def rgb2gray(self,image):
        new_image = 0.299*image[:,:,0]+0.587*image[:,:,1]+0.114*image[:,:,2]
        return new_image
    def display_image(self,image,name):
        image = np.array(image,dtype=np.uint8)
        cv2.imwrite(f'./static/imgs/{name}.jpg',image)
    def padding(self,image):
        padded_image = np.zeros((image.shape[0]+2,image.shape[1]+2))
        padded_image[1:image.shape[0]+1,1:image.shape[1]+1]=image 
        return padded_image
    
    def non_max_suppression(self,image):
        # non max suppression
        image = self.padding(self,image)
        for i in range(1,image.shape[0]-1):
            for j in range(1,image.shape[1]-1):
                if image[i,j] == 0:
                    image[i,j] = 0
                elif image[i,j] == 45:
                    if image[i-1,j+1] > image[i,j] or image[i+1,j-1] > image[i,j]:
                        image[i,j] = 0
                elif image[i,j] == 90:
                    if image[i-1,j] > image[i,j] or image[i+1,j] > image[i,j]:
                        image[i,j] = 0
                elif image[i,j] == 135:
                    if image[i-1,j-1] > image[i,j] or image[i+1,j+1] > image[i,j]:
                        image[i,j] = 0
                else:
                    if image[i,j-1] > image[i,j] or image[i,j+1] > image[i,j]:
                        image[i,j] = 0
        return image
    def hysteresis(self,image,minVal=0.3,maxVal=.32):
            # hysteresis thresholding
        image = self.padding(self,image)
        image[image > maxVal] = 255
        image[image < minVal] = 0
        for i in range(1,image.shape[0]-1):
            for j in range(1,image.shape[1]-1):
                if image[i,j] < maxVal and image[i,j] > minVal:
                    if image[i-1,j-1] >= maxVal or image[i-1,j] >= maxVal or image[i-1,j+1] >= maxVal or image[i,j-1] >= maxVal or image[i,j+1] >= maxVal or image[i+1,j-1] >= maxVal or image[i+1,j] >= maxVal or image[i+1,j+1] >= maxVal:
                        image[i,j] = 255
                    else:
                        image[i,j] = 0
        return image
    #function to do sobel, roberts, prewitt and canny edge detection
    def edge_detection(self,image,method):
        # image = self.rgb2gray(image)
        image = self.padding(self,image)

        if method == "sobel":
            Gx = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
            Gy = np.array([[-1,-2,-1],[0,0,0],[1,2,1]])


        elif method == "canny":
            return self.canny_edge(self,image)

       
        elif method == "roberts":
            Gx = np.array([[1,0],[0,-1]])
            Gy = np.array([[0,1],[-1,0]])

        elif method == "prewitt":
            Gx = np.array([[-1,0,1],[-1,0,1],[-1,0,1]])
            Gy = np.array([[-1,-1,-1],[0,0,0],[1,1,1]])

        new_image = np.zeros((image.shape[0],image.shape[1]))
        if method == "roberts":
            for i in range(1,image.shape[0]-1):
                for j in range(1,image.shape[1]-1):
                    Gx_value = np.sum((image[i-1:i+1,j-1:j+1]*Gx))
                    Gy_value = np.sum((image[i-1:i+1,j-1:j+1]*Gy))
                    new_image[i][j] = np.sqrt(Gx_value**2+Gy_value**2)
        else:   
            for i in range(1,image.shape[0]-1):
                for j in range(1,image.shape[1]-1):
                    Gx_value = np.sum((image[i-1:i+2,j-1:j+2]*Gx))
                    Gy_value = np.sum((image[i-1:i+2,j-1:j+2]*Gy))
                    new_image[i][j] = np.sqrt(Gx_value**2+Gy_value**2)


        
        return new_image
 
    def canny_edge(self,image, minVal=.1,maxVal=.15):
        # impelementing canny edge detection
        # image = self.rgb2gray(image)
        image = self.gaussian_filter(self,image,3,1)
        image = self.padding(self,image)
        gx,gy = self.SobelFilter(self,image)
        Mag = np.hypot(gx,gy)

        NMS = self.non_max_suppression(self,Mag)
        image = self.hysteresis(self,self.Normalize(self,NMS),minVal,maxVal)
        return image

    def SobelFilter(self,img):
        Gx = np.array([[-1,0,+1], [-2,0,+2],  [-1,0,+1]])
        Res_x = ndimage.convolve(img, Gx)

        Gy = np.array([[-1,-2,-1], [0,0,0], [+1,+2,+1]])
        Res_y = ndimage.convolve(img, Gy)

        return self.Normalize(self,Res_x), self.Normalize(self,Res_y)
    def Normalize(self,img):
        img = img/np.max(img)
        return img

