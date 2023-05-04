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
    return _hough_ellipse(image, threshold=threshold, accuracy=accuracy,
                          min_size=min_size, max_size=max_size)
    
image_rgb=cv2.imread('./images/ell6.png')
edges=cv2.Canny(image_rgb,50,150)
hough_ell=hough_ellipse(edges,accuracy=20,min_size=50,max_size=100)
#print(hough_ell)
#hough_ell.sort(order='accumulator')
j=0
edges = color.gray2rgb(img_as_ubyte(edges))
while j < len(hough_ell):
    best = list(hough_ell[j])
    yc, xc, a, b = (int(round(x)) for x in best[1:5])
    if a==0 or b==0:
        j+=1
        continue
    for x in range(len(hough_ell)):
        if np.abs(hough_ell[x][1]-yc)<=20 and np.abs(hough_ell[x][2]-xc)<=20:
            hough_ell[x][3]=hough_ell[x][4]=0 
    orientation = best[5]
    cy, cx = ellipse_perimeter(yc, xc, a, b, orientation)
    for i in range(len(cy)):
        if cy[i]>=edges.shape[0]:
            cy[i] =edges.shape[0]-1
        if cx[i]>=edges.shape[1]:
            cx[i] =edges.shape[1]-1    
        print(cy[i],cx[i])
    image_rgb[cy, cx] = (0, 0, 255)
    # Draw the edge (white) and the resulting ellipse (red)
    edges[cy, cx] = (250, 0, 0)
    j+=1
fig2, (ax1, ax2) = plt.subplots(ncols=2, nrows=1, figsize=(8, 4),
                                sharex=True, sharey=True)

ax1.set_title('Original picture')
ax1.imshow(image_rgb)

ax2.set_title('Edge (white) and result (red)')
ax2.imshow(edges)

plt.show()
#print(hf(image))