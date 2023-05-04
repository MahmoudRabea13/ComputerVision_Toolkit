import cv2
import numpy as np

class Harris():
    def harris_corner_detector(self,image, k=0.04, threshold=0.01):
        # Convert image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Compute gradient using Sobel operator
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        
        # Compute products of derivatives
        IxIx = sobelx ** 2
        IyIy = sobely ** 2
        IxIy = sobelx * sobely
        
        # Compute sums of products of derivatives over a local window
        sum_IxIx = cv2.GaussianBlur(IxIx, (3,3), 0)
        sum_IyIy = cv2.GaussianBlur(IyIy, (3,3), 0)
        sum_IxIy = cv2.GaussianBlur(IxIy, (3,3), 0)
        
        # Compute the Harris response
        det = (sum_IxIx * sum_IyIy) - (sum_IxIy ** 2)
        trace = sum_IxIx + sum_IyIy
        harris_response = det - k * (trace ** 2)
        
        # Threshold the Harris response
        corner_threshold = harris_response.max() * threshold
        corners = np.where(harris_response > corner_threshold)
        
        # Return corner coordinates
        corner_coords = np.vstack((corners[1], corners[0])).T


        # Draw corners on the image
        for corner in corner_coords:
            cv2.circle(image, tuple(corner), 2, (0, 255, 0), -1)

        # Write output image
        cv2.imwrite('./static/imgs/output_harris.jpg', image)
        return "Done"


    def lambdamin(image, window=3, q=0.998):
        """
        Detect corners in an image using the Harris corner detector with lambda_min criterion.
        Args:
            img: input image (grayscale or color).
            window: neighborhood size for detection (default is 3).
            q: quantile value for non-maximum suppression (default is 0.998).
        Returns:
            A boolean matrix of the same size as the input image, with the points of interest (corners) masked with True.
        """

        img = image.copy()
        # convert color image to grayscale
        if img.ndim == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # apply Gaussian smoothing to the image
        img = cv2.GaussianBlur(img, (5, 5), 0)

        # compute gradients using Sobel derivative
        sobel = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
        ix = cv2.filter2D(img, -1, sobel, borderType=cv2.BORDER_REFLECT101)
        iy = cv2.filter2D(img, -1, sobel.T, borderType=cv2.BORDER_REFLECT101)

        # compute elements of the structure tensor
        ixx = cv2.blur(ix * ix, (window, window))
        iyy = cv2.blur(iy * iy, (window, window))
        ixy = cv2.blur(ix * iy, (window, window))

        # compute lambda_min for each pixel
        lambdamat = np.zeros_like(img)
        for x, y in np.ndindex(img.shape):
            H = np.array([[ixx[x, y], ixy[x, y]], [ixy[x, y], iyy[x, y]]])
            eigvals = np.linalg.eigvalsh(H)
            lambdamin = eigvals.min(initial=0)
            lambdamat[x, y] = lambdamin

        # apply non-maximum suppression to get the highest lambda values
        threshold = np.quantile(np.abs(lambdamat), q)
        lambdamat = np.abs(lambdamat) > threshold

        # get the (x,y) coordinates of the non-zero elements in the lambdamat matrix
        corners = np.argwhere(lambdamat)

        # Draw circles on the image at the coordinates of the corners
        for corner in corners:
            cv2.circle(image, (corner[1], corner[0]), 2, (0, 255, 0), -1)


        # Write output image
        cv2.imwrite('./static/imgs/output_harris.jpg', image)
        return "Done"

