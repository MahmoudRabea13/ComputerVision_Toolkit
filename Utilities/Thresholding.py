import numpy as np
import matplotlib.pyplot as plt
import cv2
class Thresholding():
    def otsu(self,img):
        ans = []
        for t in range(img.min()+1,img.max()):
            Pbelow = img[img<t]
            Pabove = img[img>=t]
            Wb = len(Pbelow)/(img.shape[0]*img.shape[1])
            Wa = len(Pabove)/(img.shape[0]*img.shape[1])
            varb = np.var(Pbelow)
            vara = np.var(Pabove)
            ans.append(Wb*varb+vara*Wa)
        try:
            thre = min(ans)
            thershold = ans.index(thre)
        except ValueError:
            thershold  = 0
        return thershold
    def optimal_threshold(self,gray_image):
         # Maximum number of rows and cols for image
        max_x = gray_image.shape[1] - 1
        max_y = gray_image.shape[0] - 1

        first_corner = int(gray_image[0, 0])
        second_corner = int(gray_image[0, max_x])
        third_corner = int(gray_image[max_y, 0])
        forth_corner = int(gray_image[max_y, max_x])

        # Mean Value of Background Intensity, Calculated From The Four Corner Pixels
        background_mean = (first_corner + second_corner +
                           third_corner + forth_corner) / 4
        Sum = 0
        Length = 0

        # Loop To Calculate Mean Value of Foreground Intensity
        for i in range(0, gray_image.shape[1]):
            for j in range(0, gray_image.shape[0]):
                # Skip The Four Corner Pixels
                if not ((i == 0 and j == 0) or (i == max_x and j == 0) or (i == 0 and j == max_y) or (i == max_x and j == max_y)):
                    Sum += gray_image[j, i]
                    Length += 1
        foreground_mean = Sum / Length

        OldThreshold = (background_mean + foreground_mean) / 2
        NewThreshold = self.new_threshold(gray_image, OldThreshold)

        # Iterate untill the old and new threshold is equal
        while OldThreshold != NewThreshold:
            OldThreshold = NewThreshold
            NewThreshold = self.new_threshold(gray_image, OldThreshold)
        return NewThreshold
    def spectral_local_threshold(self,img, size=20):
        for i in range(0, img.shape[0]-size, size):
            for j in range(0, img.shape[1]-size, size):
                subimage = img[i:i+size, j:j + size].copy()
                img[i:i+size, j:j+size] = self.spectral_threshold(subimage)
        return img
    def new_threshold(self,gray_image, Threshold):
    
        # Get Background Array, Consisting of All Pixels With Intensity Lower Than The Given Threshold
        new_background = gray_image[np.where(gray_image < Threshold)]
        # Get Foreground Array, Consisting of All Pixels With Intensity Higher Than The Given Threshold
        new_foreground = gray_image[np.where(gray_image > Threshold)]

        new_background_mean = np.mean(new_background)
        new_foreground_mean = np.mean(new_foreground)
        # Calculate Optimal Threshold
        OptimalThreshold = (new_background_mean + new_foreground_mean) / 2
        return OptimalThreshold
    def spectral_threshold(self,img):
        # Convert the image to grayscale
        if len(img.shape) > 2:
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        else:
            gray = img

        # Compute the histogram of the image
        hist, bins = np.histogram(gray, 256, [0, 256])

        # Compute the cumulative distribution function (CDF)
        cdf = hist.cumsum()

        # Compute the normalized CDF
        cdf_normalized = cdf / float(cdf.max())

        # Calculate the mean of the entire image
        mean = np.sum(np.arange(256) * hist) / float(gray.size)

        # Initialize variables for the optimal threshold values and the maximum variance
        optimal_high = 0
        optimal_low = 0
        max_variance = 0

        # Loop over all possible threshold values, select ones with maximum variance between modes
        for high in range(0, 256):
            for low in range(0, high):
                w0 = np.sum(hist[0:low])
                if w0 == 0:
                    continue
                mean0 = np.sum(np.arange(0, low) * hist[0:low]) / float(w0)

                # Calculate the weight and mean of the low pixels
                w1 = np.sum(hist[low:high])
                if w1 == 0:
                    continue
                mean1 = np.sum(np.arange(low, high) * hist[low:high]) / float(w1)

                # Calculate the weight and mean of the high pixels
                w2 = np.sum(hist[high:])
                if w2 == 0:
                    continue
                mean2 = np.sum(np.arange(high, 256) * hist[high:]) / float(w2)

                # Calculate the between-class variance
                variance = w0 * (mean0 - mean) ** 2 + w1 * \
                    (mean1 - mean) ** 2 + w2 * (mean2 - mean) ** 2

                # Update the optimal threshold values if the variance is greater than the maximum variance
                if variance > max_variance:
                    max_variance = variance
                    optimal_high = high
                    optimal_low = low

        # Apply thresholding to the input image using the optimal threshold values
        binary = np.zeros(gray.shape, dtype=np.uint8)
        binary[gray < optimal_low] = 0
        binary[(gray >= optimal_low) & (gray < optimal_high)] = 128
        binary[gray >= optimal_high] = 255

        return binary
    def local_threshold_default(self, image, size):
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

    def global_threshold(self,image,type="otsu"):
        img = image.copy()
        if type == "otsu":
            thershold = self.otsu(img)
        elif type == "Optimal":
            thershold = self.optimal_threshold(img)
        elif type == "Spectral":
            return (self.spectral_threshold(image))
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                if img[i,j] >= (img.min()+thershold):
                    img[i,j] = 255
                else:
                    img[i,j] = 0
        return img
    def local_threshold(self,image,block_size,type):
        thresh_img = np.copy(image)
        rows = image.shape[0]
        cols = image.shape[1]
        for row in range(0, rows, block_size):
            for col in range(0, cols, block_size):
                mask = image[row:min(row+block_size,rows),col:min(col+block_size,cols)]
                thresh_img[row:min(row+block_size,rows),col:min(col+block_size,cols)] = self.global_threshold(mask, type)
        return thresh_img
