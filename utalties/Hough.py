import numpy as np
import cv2
from utalties.Filter import Filter
import random
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt, atan2
import cv2
from skimage.transform  import hough_ellipse as hf
import numpy as np
from skimage import data, color
from skimage.draw import ellipse_perimeter
from skimage.util import img_as_ubyte
from math import sqrt, atan2, pi
from collections import namedtuple
class Hough():
    def accumulator_calc(image,minRadius,maxRadius):
        imgcolor = cv2.imread(image)
        img = cv2.cvtColor(imgcolor, cv2.COLOR_BGR2GRAY)
        img = cv2.resize(img,(512,512))
        image_edges = Filter.edge_detection(Filter,img,'canny')
        accumulator = np.zeros((image_edges.shape[0], image_edges.shape[1], maxRadius-minRadius+1), dtype=np.uint16)
        r_range = np.arange(minRadius, maxRadius+1,10)
        for y in range(image_edges.shape[0]):
            for x in range(image_edges.shape[1]):
                if image_edges[y, x] != 0:
                # Loop over each radius
                    for r in r_range:
                        # Calculate the center of the circle for this radius
                        for theta in range(0, 360, 10):
                            a = int(x - r * np.cos(np.deg2rad(theta)))
                            b = int(y - r * np.sin(np.deg2rad(theta)))
                            if a >= 0 and a < accumulator.shape[1] and b >= 0 and b < accumulator.shape[0]:
                                accumulator[b, a, r-minRadius] += 1
        return accumulator
    def detect_circle(accumulator, minRadius, maxRadius):
        circles = []
        for y in range(accumulator.shape[0]):
            for x in range(accumulator.shape[1]):
                for r in range(maxRadius - minRadius + 1):
                    threshold = 0.8*np.max(accumulator[:,:,r])
                    if accumulator[y, x, r] > threshold:
                        # Check that this circle is not too similar to any previously detected circles
                        too_similar = False
                        for circle in circles:
                            if np.linalg.norm(np.array(circle[:2]) - np.array([x, y])) < circle[2] + r + minRadius:
                                too_similar = True
                                break
                        if not too_similar:
                            circles.append((x, y, r + minRadius))
        return circles
    def draw_circles(circles, img):
        for circle in circles:
            cv2.circle(img, (circle[0], circle[1]), circle[2], (0, 255, 0), 2)
        # Save the output image
        cv2.imwrite('./static/imgs/HoughOutput.jpg', img)
        # cv2.waitKey(0)
    def hough_transform(img, rho, theta, threshold, min_line_len=50, max_line_gap=30):
        height, width = img.shape
        diag_len = np.ceil(np.sqrt(height * height + width * width))
        rho_bins = np.int32(diag_len / rho)
        theta_bins = np.int32(np.pi / theta)

        accumulator = np.zeros((rho_bins, theta_bins), dtype=np.uint8)

        y, x = np.nonzero(img)

        num_edge_points = len(x)

        for i in range(num_edge_points):
            for theta_index in range(theta_bins):

                rho_val = x[i] * np.cos(theta_index * theta) + y[i] * np.sin(theta_index * theta)

                rho_index = np.int32(rho_val / rho)
                # increment the accumulator
                accumulator[rho_index, theta_index] += 1
        # get the indices of the accumulator where the values are greater than the threshold
        indices = np.nonzero(accumulator >= threshold)
        # get the number of lines
        num_lines = len(indices[0])
        # create an array to store the lines
        lines = []
        # get the lines
        for i in range(num_lines):
            
            rho_index = indices[0][i]
            theta_index = indices[1][i]
            # get the rho and theta values
            rho_val = rho_index * rho
            theta_val = theta_index * theta
            # get the x and y values
            x0 = np.cos(theta_val) * rho_val
            y0 = np.sin(theta_val) * rho_val
            x1 = int(x0 + diag_len * np.cos(theta_val + np.pi / 2))
            y1 = int(y0 + diag_len * np.sin(theta_val + np.pi / 2))
            # use minLineLength and maxLineGap to filter out the lines
            if np.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2) > min_line_len and np.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2) > max_line_gap:
                lines.append([x0, y0, x1, y1])
                # cv2.line(img, (int(x0), int(y0)), (int(x1), int(y1)), (0, 0, 255), 2)
            # cv2.imwrite('./static/imgs/HoughOutput.jpg', img)
        return lines, img
    def _hough_ellipse(img,threshold=200,
                       accuracy=1,min_size=4,
                       max_size=None):
        if img.ndim != 2:
                raise ValueError('The input image must be 2D.')

        # The creation of the array `pixels` results in a rather nasty error
        # when the image is empty.
        # As discussed in GitHub #2820 and #2996, we opt to return an empty array.
        if not np.any(img):
            return np.zeros((0, 6))

        pixels = np.row_stack(np.nonzero(img))
        ignore=set()
        #pixels=pixels[:,4000:5000]
        print(pixels.shape)
        num_pixels = pixels.shape[1]
        acc = list()
        results = list()
        bin_size = accuracy * accuracy

        if max_size is None:
            if img.shape[0] < img.shape[1]:
                max_b_squared = np.round(0.5 * img.shape[0])
            else:
                max_b_squared = np.round(0.5 * img.shape[1])
            max_b_squared *= max_b_squared
        else:
            max_b_squared = max_size * max_size

    
        for p1 in range(600,800):
            print(p1,num_pixels)
            if p1 in ignore:
                continue
            p1x = pixels[1, p1]
            p1y = pixels[0, p1]
            #ignore.add(p1)
            for p2 in range(p1):
                if p2 in ignore:
                    continue
                p2x = pixels[1, p2]
                p2y = pixels[0, p2]
                #ignore.add(p2)
                # Candidate: center (xc, yc) and main axis a
                dx = p1x - p2x
                dy = p1y - p2y
                a = 0.5 * sqrt(dx * dx + dy * dy)
                if a > 0.5 * min_size:
                    xc = 0.5 * (p1x + p2x)
                    yc = 0.5 * (p1y + p2y)

                    for p3 in range(num_pixels):
                        if p3 in ignore:
                            continue
                        #ignore.add(p3)
                        p3x = pixels[1, p3]
                        p3y = pixels[0, p3]
                        dx = p3x - xc
                        dy = p3y - yc
                        d = sqrt(dx * dx + dy * dy)
                        if d > min_size:
                            dx = p3x - p1x
                            dy = p3y - p1y
                            cos_tau_squared = ((a*a + d*d - dx*dx - dy*dy)
                                               / (2 * a * d))
                            cos_tau_squared *= cos_tau_squared
                            # Consider b2 > 0 and avoid division by zero
                            k = a*a - d*d * cos_tau_squared
                            if k > 0 and cos_tau_squared < 1:
                                b_squared = a*a * d*d * (1 - cos_tau_squared) / k
                                # b2 range is limited to avoid histogram memory
                                # overflow
                                if b_squared <= max_b_squared:
                                    acc.append(b_squared)
                    if len(acc) > 0:
                        bins = np.arange(0, np.max(acc) + bin_size, bin_size)
                        hist, bin_edges = np.histogram(acc, bins=bins)
                        hist_max = np.max(hist)
                        if hist_max > threshold:
                            orientation = atan2(p1x - p2x, p1y - p2y)
                            b = sqrt(bin_edges[hist.argmax()])
                            # to keep ellipse_perimeter() convention
                            if orientation != 0:
                                orientation = pi - orientation
                                # When orientation is not in [-pi:pi]
                                # it would mean in ellipse_perimeter()
                                # that a < b. But we keep a > b.
                                if orientation > pi:
                                    orientation = orientation - pi / 2.
                                    a, b = b, a
                            if a!=0 and b!=0:        
                                results.append((hist_max,  # Accumulator
                                            yc, xc,
                                            a, b,
                                            orientation))
                            #print(results[-1])
                        acc = []

        return np.array(results, dtype=[('accumulator', np.intp),
                                        ('yc', np.float64),
                                        ('xc', np.float64),
                                        ('a', np.float64),
                                        ('b', np.float64),
                                        ('orientation', np.float64)])


    def hough_ellipse(image, threshold=200, accuracy=5, min_size=4, max_size=None):
        return Hough._hough_ellipse(image, threshold=threshold, accuracy=accuracy,
                              min_size=min_size, max_size=max_size)