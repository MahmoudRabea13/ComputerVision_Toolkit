import cv2
import numpy as np
import random

class Segmentation():
    
    def region_growing(self,img, seed_point, threshold):
        # Convert the input image to the LAB color space
        lab_img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        
        # Create a mask for the segmented region
        mask = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
        
        # Set the seed point value as the initial region value
        region_value = lab_img[seed_point[::-1]]
        
        # Define a neighborhood of 4-connected pixels
        neighborhood = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        
        # Loop until the region stops growing
        while True:
            prev_mask = np.copy(mask)
            for y in range(mask.shape[0]):
                for x in range(mask.shape[1]):
                    # If the current pixel is already in the region, skip it
                    if mask[y, x] == 255:
                        continue
                    # Calculate the difference between the current pixel and the region value
                    diff = np.abs(lab_img[y, x] - region_value)
                    # If the difference is below the threshold, add the pixel to the region
                    if np.all(diff < threshold):
                        mask[y, x] = 255
                        # Update the region value using the newly added pixel
                        region_value = (region_value + lab_img[y, x]) / 2
            # If the mask hasn't changed, stop looping
            if np.array_equal(prev_mask, mask):
                break
        
        # Convert the mask to a 3-channel image and apply it to the input image
        mask = np.expand_dims(mask, axis=2)
        mask = np.repeat(mask, 3, axis=2)
        output_img = np.where(mask == 255, img, 0)
        
        # Convert the output image to the LAB color space
        output_lab_img = cv2.cvtColor(output_img, cv2.COLOR_BGR2LAB)
        # save the segmented image
        cv2.imwrite('./static/imgs/segmented.jpg',output_lab_img)
        return "success segmentation"


    def kmeans(self,num_clusters, data, max_iter):
        # Initialize centroids randomly
        centroids = data[np.random.choice(data.shape[0], num_clusters, replace=False)]

        # Assign points to nearest centroid
        distances = np.zeros((data.shape[0], num_clusters))
        for i in range(num_clusters):
            distances[:, i] = np.linalg.norm(data - centroids[i], axis=1)
        clusters = np.argmin(distances, axis=1)

        # Update centroids
        for i in range(num_clusters):
            centroids[i] = np.mean(data[clusters == i], axis=0)

        # Repeat until convergence or max number of iterations is reached
        for i in range(max_iter):
            old_clusters = clusters

            # Assign points to nearest centroid
            distances = np.zeros((data.shape[0], num_clusters))
            for i in range(num_clusters):
                distances[:, i] = np.linalg.norm(data - centroids[i], axis=1)
            clusters = np.argmin(distances, axis=1)

            # Check for convergence
            if np.array_equal(clusters, old_clusters):
                break

            # Update centroids
            for i in range(num_clusters):
                centroids[i] = np.mean(data[clusters == i], axis=0)

        return centroids


    def kmeans_cluster_image(self, num_clusters, image, max_iter):
        # get the image dimensions
        height, width, channels = image.shape

        # reshape the image to be a list of pixels
        image = image.reshape((height * width, channels))

        # cluster the pixels and assign labels
        centroids = Segmentation.kmeans(Segmentation, num_clusters, image, max_iter)
        distances = np.zeros((image.shape[0], num_clusters))
        for i in range(num_clusters):
            distances[:, i] = np.linalg.norm(image - centroids[i], axis=1)
        labels = np.argmin(distances, axis=1)

        # convert the label image to color
        label_image = np.uint8(labels.reshape((height, width)))
        color_image = np.zeros((height, width, channels), dtype=np.uint8)
        for i in range(num_clusters):
            color_image[label_image == i] = centroids[i]

        # save the output image
        cv2.imwrite('./static/imgs/segmented.jpg', color_image)

        return "success"


    def mean_shift(self,image, bandwidth):
        # Load the input image in BGR format

        # Convert the input image from BGR to LAB color space
        lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

        # Compute the mean shift vector for each pixel
        height, width, channels = lab_image.shape
        ms_image = np.zeros((height, width), dtype=np.int32)
        label = 1
        for y in range(height):
            for x in range(width):
                if ms_image[y, x] == 0:
                    ms_vector = np.zeros(channels, dtype=np.float32)
                    pixel_vector = lab_image[y, x].astype(np.float32)
                    count = 0
                    while True:
                        prev_ms_vector = ms_vector
                        prev_count = count
                        for i in range(max(y - bandwidth, 0), min(y + bandwidth, height)):
                            for j in range(max(x - bandwidth, 0), min(x + bandwidth, width)):
                                if ms_image[i, j] == 0 and np.linalg.norm(pixel_vector - lab_image[i, j]) < bandwidth:
                                    ms_vector += lab_image[i, j]
                                    count += 1
                                    ms_image[i, j] = label
                        ms_vector /= count
                        if np.linalg.norm(ms_vector - prev_ms_vector) < 1e-5 or count == prev_count:
                            break
                    ms_image[ms_image == label] = count
                    label += 1
        # Convert the mean shift labels to a color image using the LAB color space
        unique_labels = np.unique(ms_image)
        n_clusters = len(unique_labels)
        ms_color_image = np.zeros_like(lab_image)
        for i, label in enumerate(unique_labels):
            mask = ms_image == label
            ms_color_image[mask] = np.mean(lab_image[mask], axis=0)

        # Save the output image in the LAB color space
        cv2.imwrite('./static/imgs/segmented.jpg', ms_color_image)
        return "Sucess segmentation"

    def compute_init_matrix(self,points) :
        Dis_Mat = [[-1]*len(points) for i in range(0,len(points))]
        for i in range(len(points)) :
            for j in range(i,len(points)) :
                if(j == i) : 
                    Dis_Mat[j][i] = -1
                    continue
                Dis_Mat[j][i] = Segmentation.compute_Dis(Segmentation,points[i],points[j],i,j)
        return Dis_Mat

    def compute_Dis(self,p1, p2, i, j):
        p1 = np.concatenate((p1, [i]))
        p2 = np.concatenate((p2, [j]))
        return np.linalg.norm(p1 - p2)


    def Min_Dis(self,matrix) :
        minimum = [1,0]
        for i in range(len(matrix)) :
            for j in range(len(matrix[0])) :
                if((matrix[i][j] == -1)) : continue
                if(matrix[i][j] < matrix[minimum[0]][minimum[1]]) :
                    minimum = [i,j]
        return minimum

    def segment(self,image,number_of_clusters = 2) :
     
        points = image.reshape(image.shape[0] * image.shape[1] , 3)
        dindogram = [[i] for i in range(len(points))]
        if(number_of_clusters > len(points)) : raise Exception("Clusters exceeded points!!")
        Dis_Mat = Segmentation.compute_init_matrix(Segmentation,points)
        while len(dindogram) != number_of_clusters :
            minimum = Segmentation.Min_Dis(Segmentation,Dis_Mat)
            new_cluster = [dindogram[minimum[0]],dindogram[minimum[1]]]
            flat_new_cluster = [item for sublist in new_cluster for item in sublist]
            dindogram.pop(np.max(minimum))
            dindogram[np.min(minimum)] = flat_new_cluster
            Segmentation.Update_Mat(Segmentation,Dis_Mat,minimum[0],minimum[1])
        
        return points,dindogram

    def Update_Mat(self,Dis_Mat,indx1,indx2) :
        maximum_indx = max([indx1,indx2])
        Segmentation.single_link(Segmentation,Dis_Mat,indx1,indx2)
        Dis_Mat.pop(maximum_indx)
        for i in range(len(Dis_Mat)) :
            Dis_Mat[i].pop(maximum_indx)


    def single_link(self,Dis_Mat, indx1, indx2):
        minimum_indx = min([indx1, indx2])
        for i in range(len(Dis_Mat)):
            if i in (indx1, indx2):
                continue
            if i < minimum_indx:
                distanc_1 = Dis_Mat[indx1][i]
                distanc_2 = Dis_Mat[indx2][i]
            else:
                distanc_1 = Dis_Mat[i][indx1]
                distanc_2 = Dis_Mat[i][indx2]
            m = min([distanc_1, distanc_2])
            Dis_Mat[minimum_indx][i] = m


    def agglomerative_cluster(self,points, dindogram, Image_Before):
        colors = np.array([[random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)] for _ in range(len(dindogram))])
        for i, cluster in enumerate(dindogram):
            mask = np.isin(np.arange(len(points)), cluster)
            points[mask] = colors[i]
        image = points.reshape(Image_Before.shape)
        cv2.imwrite('./static/imgs/segmented.jpg',image)
        return "success segmentation"




