import numpy as np
import cv2
from utalties.Sift import computeKeypointsAndDescriptors
class Match():
    def calc_SSD(self,des1,des2):
        ssd = 0
        for i in range(len(des1)):
            ssd += (des1[i]-des2[i])**2
        ssd = np.sqrt(ssd)
        return ssd
    def calculate_NCC(self,desc_image1, desc_image2):
        normlized_output1 = (desc_image1 - np.mean(desc_image1)) / (np.std(desc_image1))
        normlized_output2 = (desc_image2 - np.mean(desc_image2)) / (np.std(desc_image2))
        correlation_vector = np.multiply(normlized_output1, normlized_output2)
        NCC = float(np.mean(correlation_vector))
        return NCC
    def feature_matching(self,descriptor1,descriptor2,method,threshold):
    

        keyPoints1 = descriptor1.shape[0]
        keyPoints2 = descriptor2.shape[0]

        #Store matching scores
        matched_features = []
        # i=0
        for kp1 in range(keyPoints1):
            # Initial variables (will be updated)
            distance = np.inf
            y_index = -1
            for kp2 in range(keyPoints2):
                if method=="SSD":
                   score = self.calc_SSD(self,descriptor1[kp1], descriptor2[kp2])
                elif method =="NCC":
                    score = self.calculate_NCC(self,descriptor1[kp1], descriptor2[kp2])
                if score < distance:
                    distance = score
                    y_index = kp2
            if method == "SSD":
                if distance <=  threshold:
                    feature = cv2.DMatch()
                    #The index of the feature in the first image
                    feature.queryIdx = kp1
                    # The index of the feature in the second image
                    feature.trainIdx = y_index
                    #The distance between the two features
                    feature.distance = distance
                    matched_features.append(feature)
            else:
                feature = cv2.DMatch()
                #The index of the feature in the first image
                feature.queryIdx = kp1
                # The index of the feature in the second image
                feature.trainIdx = y_index
                #The distance between the two features
                feature.distance = distance
                matched_features.append(feature)
        return matched_features        
    def draw(self,original_img,template_img,method,threshold):
        kp1,descriptor1 = computeKeypointsAndDescriptors(original_img)
        kp2,descriptor2 = computeKeypointsAndDescriptors(template_img)
        fff = self.feature_matching(self,descriptor1,descriptor2,method,threshold)
        im = cv2.drawMatches(original_img, kp1, template_img, kp2, fff, None,flags=cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)
        im = cv2.resize(im,(400,300))
        name = method.lower()
        cv2.imwrite(f'./static/imgs/{name}_img.jpg',im)