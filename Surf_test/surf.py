import cv2
import numpy as np
import csv
import os, subprocess

############### Parameters to be tweaked ###############
inputDir = "ImageData"
topN = 1

# Running surf detector
surf = cv2.xfeatures2d.SURF_create(1000)
with open('information.csv', 'w', newline = '') as f:
    writer = csv.writer(f)
    for file in os.listdir(inputDir):
        if file.endswith(".jpg"):
            print("{} is loaded.".format(file))
            img_path = inputDir + '/' + file
            img1 = cv2.imread(img_path,1)
            scale_percent = 60
            width = int(img1.shape[1] * scale_percent / 100)
            height = int(img1.shape[0] * scale_percent / 100)
            dim = (width, height)
            img1 = cv2.resize(img1, dim, interpolation = cv2.INTER_AREA)
            img = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            key_points, descriptors = surf.detectAndCompute(img,None)
            dim = descriptors.shape
            edge = []
            # Labelling of corner or edge points
            for i in range(topN):   
                out_img = np.copy(img)
                print(i)
                key_points_f = []
                key_points_f.append(key_points[i])
                # Drawing points
                cv2.drawKeypoints(img, key_points_f, out_img, (0,0,0), flags = cv2.DRAW_MATCHES_FLAGS_DRAW_OVER_OUTIMG)
                cv2.imshow("window", out_img)
                cv2.waitKey(200)
                a = int(input("label :- "))
                if a==1:
                    edge.append(i)
            # Writing data in csv file
            f_data = []
            for i in range(topN):
                temp = []
                if i in edge:
                    temp.append(1)
                else:
                    temp.append(0)
                temp.append(key_points[i])
                for j in range(dim[1]):
                    temp.append(descriptors[i][j])
                f_data.append(temp)
            writer.writerows(f_data)

