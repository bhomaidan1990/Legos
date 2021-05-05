#! /usr/bin/python3
# -*- coding: utf-8 -*-
'''
| author:
| Belal HMEDAN, 
| LIG lab/ Marven Team, 
| France, 2021.
| image processing script.
'''
"""
Reference:
https://stackoverflow.com/a/66863584
"""

import os
import sys
import numpy as np
import cv2
from functools import cmp_to_key  
#=======================
# class imageProcessor |
#=======================
class imageProcessor():
    def __init__(self, imgPath, imgName='image.jpg'):
        """
        Class imageProcessor: Read and Process image to get world state.
        ---
        Parameters:
        @param: imgPath, string, the path to the image to process.
        @param: imgName, string, the name of the image including the extension.
        """

        self.imgPath = imgPath
        self.imgName = imgName
        self.workspaceCoords = None
        self.greenRects = None
        self.cellList = None
        self.cellCenters = None
        self.redMask = None
        self.redMaskBGR = None

        self.cellsState = {
        # First column
        15:  ['p_10_04', 'g'], 14:  ['p_11_04', 'g'], 13:  ['p_12_04', 'g'], 12:  ['p_13_04', 'g'],
        # Second column
        11:  ['p_10_05', 'g'], 10:  ['p_11_05', 'g'], 9:  ['p_12_05', 'g'], 8:  ['p_13_05', 'g'],
        # Third column
        7:  ['p_10_06', 'g'], 6:  ['p_11_06', 'g'], 5: ['p_12_06', 'g'], 4: ['p_13_06', 'g'],
        # Fourth column
        3: ['p_10_07', 'g'], 2: ['p_11_07', 'g'], 1: ['p_12_07', 'g'], 0: ['p_13_07', 'g']
        }

        self.swapState = {
        # Swap
        'p_07_06' : 'g', 'p_07_07' : 'g'}

        self.humanStock = {
        'b_2x2': 1, 'b_2x4': 1, 'y_2x2': 1, 'y_2x4': 1 }

    def undistort(self, img):
        """
        Function: undistort, to undistort fisheyes lens distortion.
        ---
        Parameters:
        @param: img, ndarray, image frame of shape [height, width, 3(BGR)].
        ---
        @return: undistorted_img, ndarray, the undistorted image.
        """
        dim = img.shape[:2][::-1]
        cv_file = cv2.FileStorage(self.imgPath+"cam_01.yaml", cv2.FILE_STORAGE_READ)
        K  = cv_file.getNode("camera_matrix").mat()
        D  = cv_file.getNode("dist_coeff").mat()
        cv_file.release()
        new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(K, D, dim, np.eye(3), balance=1)
        map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D , np.eye(3), new_K, dim, cv2.CV_16SC2)
        undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
        
        return undistorted_img

    def HSV_mask(self, img, color):
        """
        Function: check_HSV, to get the ratio of the marked pixels of specific color in the frame,
          using HSV space.
        ---
        Parameters:
        @param: img, ndarray, image frame of shape [height, width, 3(BGR)].
        @param: color, string, defines the color from ["red", "green", "blue", "yellow"]
        ---
        @return: mask, ndarray, the masked image for the given color.
        """

        colors = ['red', 'green', 'blue', 'yellow']
        if not color in colors:
            print('Please Note that the color has to be either: red, green, blue, or yellow]\n')
            return np.zeros_like(img)[...,0]

        hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

        # Dictionary to map the range of the Hue, Saturation, Value(illumination) of each color.
        HSV_ranges = {
        "red":      ( 174,  12) + (140, 255) + (20, 255),
        "green":    (  55,  90) + (150, 255) + (20, 255),
        "blue":     (  95, 115) + (115, 255) + (20, 255),
        "yellow":   (  20,  30) + (190, 255) + (20, 255)
        }

        HSV= HSV_ranges[color]
        # checking the marked pixels in the captured_hsv_frame
        if HSV[0]<HSV[1] :
            mask=cv2.inRange(hsv_img,HSV[0::2],HSV[1::2])
        else:
            # Red color has two ranges
            mask1 = cv2.inRange(hsv_img,(0,HSV[2],HSV[4]), (HSV[1],HSV[3],HSV[5]))
            mask2 = cv2.inRange(hsv_img, (HSV[0],HSV[2],HSV[4]), (180,HSV[3],HSV[5]))
            mask  = cv2.bitwise_or(mask1, mask2)
            mask  = cv2.medianBlur(mask, 5)                                # <---------#
        return mask

    def Morhology(self, mask, th=50, k=5, iters=10, verbose=False):
        """
        Function: Morhology, to do morhological closing to the mask.
        ---
        Parameters:
        @param: mask, nd array binary mask resulting from HSV masking.
        @param: k, integer, kernel (structuring element) size.
        @param: iters, integer, operation iterations.
        @param: verbose, boolean, to show the output of the function.
        ---
        @return: mask, nd array binary mask resulting from HSV masking,
                maskBGR, nd array, deepcopy of the mask in BGR.
        """

        # Gaussian Filter
        mask = cv2.GaussianBlur(mask,(5,5),3)
        # Get the structuring element:
        maxKernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(k, k))
        # Perform closing:
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, maxKernel, None, None, iters, cv2.BORDER_REFLECT101)
        # Threshold
        mask[mask<th] = 0
        mask[mask>=th] = 255
        # Visualize results
        if(verbose):
            cv2.namedWindow('Morphology mask', cv2.WINDOW_NORMAL)
            cv2.imshow('Morphology mask', mask)
            cv2.waitKey(1000)
            cv2.destroyAllWindows()
        # Create a deep copy, convert it to BGR for results:
        maskBGR = mask.copy()
        maskBGR = cv2.cvtColor(maskBGR, cv2.COLOR_GRAY2BGR)

        return mask, maskBGR

    def rect_sort(self, a, b):
        """
        Function: findMarkersContour, to find the contours of the red markers.
        Reference: https://stackoverflow.com/a/67105599
        ---
        Parameters:
        @param: mask, nd array binary mask resulting from HSV masking, and Morpholigical closing.
        @param: minArea, integer, the min size of the rectangle to be considered.
        ---
        @return: boundRectsSorted, list, bounding rectangles list sorted.
        """

        if abs(a[1] - b[1]) <= 15:
            return a[0] - b[0]
        return a[1] - b[1]

    def findMarkersContour(self, mask, minArea=100):
        """
        Function: findMarkersContour, to find the contours of the red markers.
        ---
        Parameters:
        @param: mask, nd array binary mask resulting from HSV masking, and Morpholigical closing.
        @param: minArea, integer, the min size of the rectangle to be considered.
        ---
        @return: boundRectsSorted, list, bounding rectangles list sorted.
        """

        # Find the big contours/blobs on the filtered image:
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

        # Bounding Rects are stored here:
        boundRectsList = []

        # Process each contour 1-1:
        for i, c in enumerate(contours):

            # Approximate the contour to a polygon:
            contoursPoly = cv2.approxPolyDP(c, 3, True)

            # Convert the polygon to a bounding rectangle:
            boundRect = cv2.boundingRect(contoursPoly)

            # Get the bounding rect's data:
            rectX = boundRect[0]
            rectY = boundRect[1]
            rectWidth = boundRect[2]
            rectHeight = boundRect[3]

            # Estimate the bounding rect area:
            rectArea = rectWidth * rectHeight

            # Filter blobs by area:
            if rectArea > minArea:
                #Store the rect:
                boundRectsList.append(boundRect)
        # Sort the list based on ascending y values:
        boundRectsSorted = sorted(boundRectsList, key=cmp_to_key(self.rect_sort))

        return boundRectsSorted

    def cropPlatform(self, boundRectsSorted, img, offset=5):
        """
        Function: cropPlatform, to crop the green platform.
        ---
        Parameters:
        @param: boundRectsSorted, list of rectangles coordinates [(x, y, w, h)]
        @param: img, nd array to be cropped.
        ---
        @return: boundRectsSorted, list, bounding rectangles list sorted.
        """
        areas = [(boundRectsSorted[i][2]) * (boundRectsSorted[i][3]) for i in range(len(boundRectsSorted))]
        idx = areas.index(max(areas))
        myRect = boundRectsSorted[idx]
        
        x0 = myRect[0] - offset
        y0 = myRect[1] - offset
        w  = myRect[2]
        x1 = x0 + w   + 2*offset
        h  = myRect[3]
        y1 = y0 + h   + 2*offset

        cropped = img[y0:y1, x0:x1]

        return cropped

    def centerMarkersContour(self, maskCopy, boundRectsSorted, verbose=False):
        """
        Function: centerMarkersContour, to find the contour of the center workspace.
        ---
        Parameters:
        @param: maskCopy, nd array, deepcopy of the mask in BGR.
        @param: boundRectsSorted, list, bounding rectangles list sorted.
        @param: verbose, boolean, to show the output of the function.
        ---
        @return: maskCopy, nd array, marked copy of the mask deepcopy.
        """

        # Rectangle dictionary:
        # Each entry is an index of the currentRect list
        # 0 - X, 1 - Y, 2 - Width, 3 - Height
        # Additionally: -1 is 0 (no dimension):
        pointsDictionary = {0: (2, 3),
                            1: (-1, 3),
                            2: (2, -1),
                            3: (-1, -1)}

        # Store center rectangle coordinates here:
        centerRectangle = [None]*4

        # Process the sorted rects:
        rectCounter = 0

        for i in range(len(boundRectsSorted)):

            # Get sorted rect:
            currentRect = boundRectsSorted[i]

            # Get the bounding rect's data:
            rectX = currentRect[0]
            rectY = currentRect[1]
            rectWidth = currentRect[2]
            rectHeight = currentRect[3]

            # Draw sorted rect:
            cv2.rectangle(maskCopy, (int(rectX), int(rectY)), (int(rectX + rectWidth),
                                     int(rectY + rectHeight)), (0, 255, 0), 5)

            # Get the inner points:
            currentInnerPoint = pointsDictionary[i]
            borderPoint = [None]*2

            # Check coordinates:
            for p in range(2):
                # Check for '0' index:
                idx = currentInnerPoint[p]
                if idx == -1:
                    borderPoint[p] = 0
                else:
                    borderPoint[p] = currentRect[idx]

            # Draw the border points:
            color = (0, 0, 255)
            thickness = 2
            centerX = rectX + borderPoint[0]
            centerY = rectY + borderPoint[1]
            radius = 10
            cv2.circle(maskCopy, (centerX, centerY), radius, color, thickness)

            # Mark the circle
            org = (centerX - 5, centerY + 5)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(maskCopy, str(rectCounter), org, font,
                    2, (0, 0, 0), 2, cv2.LINE_8)

            # Store the coordinates into list
            if rectCounter == 0:
                centerRectangle[0] = centerX
                centerRectangle[1] = centerY
            else:
                if rectCounter == 1:
                    centerRectangle[2] = centerX - centerRectangle[0]
                else:
                    if rectCounter == 2:
                        centerRectangle[3] = centerY - centerRectangle[1]
            # Increase rectCounter:
            rectCounter += 1

        # store the workspace coords
        self.workspaceCoords = centerRectangle

        # Visualize results
        if(verbose):
            # Show the circles:
            cv2.namedWindow("Sorted Rects", cv2.WINDOW_NORMAL)
            cv2.imshow("Sorted Rects", maskCopy)
            cv2.waitKey(1000)
            cv2.destroyAllWindows()

        return maskCopy

    def cropWorkspace(self, inputCopy, maskCopy, verbose=False):
        """
        Function: cropWorkspace, to crop the desired workspace.
        ---
        Parameters:
        @param: inputCopy, nd array, deepcopy of the original image.
        @param: maskCopy, nd array, marked copy of the mask deepcopy.
        @param: verbose, boolean, to show the output of the function.
        ---
        @return: centerPortion, nd array, cropped workspace.
        """
        if(not None in self.workspaceCoords):
            # Check out the big rectangle at the center:
            bigRectX = self.workspaceCoords[0]
            bigRectY = self.workspaceCoords[1]
            bigRectWidth = self.workspaceCoords[2]
            bigRectHeight = self.workspaceCoords[3]
            # Draw the big rectangle:
            cv2.rectangle(maskCopy, (int(bigRectX), int(bigRectY)), (int(bigRectX + bigRectWidth),
                                 int(bigRectY + bigRectHeight)), (0, 0, 255), 2)

            # Visualize results
            if(verbose):
                cv2.namedWindow("Big Rectangle", cv2.WINDOW_NORMAL)
                cv2.imshow("Big Rectangle", maskCopy)
                cv2.waitKey(1000)
                cv2.destroyAllWindows()
            # Crop the center portion:
            centerPortion = inputCopy[bigRectY:bigRectY + bigRectHeight, bigRectX:bigRectX + bigRectWidth]

        else:
            print("Error: cropping coordinates are None!")
            centerPortion = None

        return centerPortion

    def gridWorkspace(self, centerPortion, gridSize=4, verbose=False):
        """
        Function: gridWorkspace, to find the contours of the red markers.
        ---
        Parameters:
        @param: centerPortion, nd array, cropped workspace.
        @param: gridSize, integer, lenght/width or the Workspace.
        @param: verbose, boolean, to show the output of the function. 
        ---
        @return: cellList, list, cells coordinates list,
                cellCenters, list, cells centers list.
        """
        # Store a deep copy for results:
        centerPortionCopy = centerPortion.copy()

        # Divide the image into a grid:
        verticalCells = gridSize
        horizontalCells = gridSize

        # Cell dimensions
        bigRectWidth = self.workspaceCoords[2]
        bigRectHeight = self.workspaceCoords[3]

        cellWidth = bigRectWidth / verticalCells
        cellHeight = bigRectHeight / horizontalCells

        # Store the cells here:
        cellList = []

        # Store cell centers here:
        cellCenters = []

        # Loop thru vertical dimension:
        for j in range(verticalCells):

            # Cell starting y position:
            yo = j * cellHeight

            # Loop thru horizontal dimension:
            for i in range(horizontalCells):

                # Cell starting x position:
                xo = i * cellWidth

                # Cell Dimensions:
                cX = int(xo)
                cY = int(yo)
                cWidth = int(cellWidth)
                cHeight = int(cellHeight)

                # Crop current cell:
                currentCell = centerPortion[cY:cY + cHeight, cX:cX + cWidth]

                # into the cell list:
                cellList.append(currentCell)

                # Store cell center:
                cellCenters.append((cX + 0.5 * cWidth, cY + 0.5 * cHeight))

                # Draw Cell
                cv2.rectangle(centerPortionCopy, (cX, cY), (cX + cWidth, cY + cHeight), (255, 255, 0), 5)

        # Visualize results
        if(verbose):
            cv2.namedWindow("Grid", cv2.WINDOW_NORMAL)
            cv2.imshow("Grid", centerPortionCopy)
            cv2.waitKey(1000)

        return cellList, cellCenters

    def cellAnalyser(self, centerPortion, cellList, cellCenters, verbose=False):
        """
        Function: cellAnalyser, to recognize the color of each cell.
        ---
        Parameters:
        @param: centerPortion, nd array, cropped workspace.
        @param: cellList, list, cells arrays list.
        @param: cellCenters, list, cells centers list.
        @param: verbose, boolean, to show the output of the function. 
        ---
        @return: None
        """
        # HSV dictionary - color ranges and color name:
        colorDictionary = {0: ([95, 115, 0], [115, 255, 255], "blue"  ),
                           1: ([20, 190, 0], [30, 255,  255], "yellow"),
                           2: ([55, 150, 0], [90, 255,  255], "green" )}

        # Cell counter:
        cellCounter = 0

        for c in range(len(cellList)):

            # Get current Cell:
            currentCell = cellList[c]
            # Convert to HSV:
            hsvCell = cv2.cvtColor(currentCell, cv2.COLOR_BGR2HSV)

            # Some additional info:
            (h, w) = currentCell.shape[:2]

            # Process masks:
            maxCount = 10
            cellColor = "None"

            for m in range(len(colorDictionary)):

                # Get current lower and upper range values:
                currentLowRange = np.array(colorDictionary[m][0])
                currentUppRange = np.array(colorDictionary[m][1])

                # Create the HSV mask
                mask = cv2.inRange(hsvCell, currentLowRange, currentUppRange)

                # Get max number of target pixels
                targetPixelCount = cv2.countNonZero(mask)
                if targetPixelCount > maxCount:
                    maxCount = targetPixelCount
                    # Get color name from dictionary:
                    cellColor = colorDictionary[m][2]
                    state     = self.cellsState[c]
                    state[1]  = colorDictionary[m][2][0]
                    self.cellsState[c] = state
            

            # Increase cellCounter:
            cellCounter += 1

        # Visualize results
        if(verbose):

            cv2.namedWindow("centerPortion", cv2.WINDOW_NORMAL)
            cv2.imshow("centerPortion", centerPortion)
            cv2.waitKey(1000)

    def swapAnalyser(self, greenPlatform, greenShape=(378, 733)):
        """
        Function: swapAnalyser, to recognize the color of each swap cell,
         and check the human stock.
        ---
        Parameters:
        @param: greenPlatform, ndarray, the cropped green space.
        ---
        @return: None.
        """
        if(not greenPlatform.shape != greenShape):
            greenPlatform = cv2.resize(greenPlatform, greenShape)

        swap = {
        'p_07_06' : greenPlatform[145:170, 490:520, :],
        'p_07_07' : greenPlatform[115:140, 490:520, :]
        }

        for zone in swap:

            for color in ['green', 'yellow', 'blue']:
                mask = self.HSV_mask(swap[zone], color)
                pixelsCount = np.count_nonzero(mask)
                if(pixelsCount>250):
                    self.swapState[zone] = color[0]

        humanStock = {
        'b_2x4': greenPlatform[100:125, 620:725, :],
        'b_2x2': greenPlatform[160:185, 620:725, :],
        'y_2x4': greenPlatform[220:245, 620:725, :],
        'y_2x2': greenPlatform[280:305, 620:725, :]
        }

        for zone in humanStock: 
            mask1 = self.HSV_mask(humanStock[zone], 'yellow')
            mask2 = self.HSV_mask(humanStock[zone], 'blue')
            mask  = cv2.bitwise_or(mask1, mask2) 
            pixelsCount = np.count_nonzero(mask)
            if(not pixelsCount>250):
                self.humanStock[zone] = 0 

    def stateAnalyzer(self, verbose=False):
        """
        Function: stateAnalyzer, to get the color state of the workspace.
        ---
        Parameters:
        @param: verbose, boolean, to show the output of the function. 
        ---
        @return: None
        """

        # check if the image exists.
        directory = self.imgPath+self.imgName
        if(not os.path.isfile(directory)):
            sys.exit("Error: Image doesn't exist!\n")
        # read the image
        img = cv2.imread(directory)
        # check the image file validity
        if(img is None):
            sys.exit("Error: Image isn't valid!\n")

        # remove fisheye lens destortion
        undistorted = self.undistort(img)

        if self.greenRects is None:
            # mask the green color
            greenMask = self.HSV_mask(undistorted, 'green')
            greenMask, greenMaskBGR = self.Morhology(greenMask, th=240 ,verbose=verbose)
            # find the large rectangles
            self.greenRects = self.findMarkersContour(greenMask, minArea=10000)
            
        # crop the large rectangle
        greenPlatform = self.cropPlatform(self.greenRects, undistorted)
        # detect swap, and human stock
        hand = self.handDetector() 
        if(not hand):
            self.swapAnalyser(greenPlatform)
            if None in [self.redMask, self.redMaskBGR]:
                # mask the red color
                redMask = self.HSV_mask(greenPlatform, 'red')
                # Morpholoical closing
                self.redMask, self.redMaskBGR = self.Morhology(redMask, th=50, verbose=verbose)

                # find the red markers
                redRects  = self.findMarkersContour(self.redMask, minArea=800)
                # safe the coordinated of the markers
                if self.workspaceCoords is None:
                    _ = self.centerMarkersContour(self.redMaskBGR, redRects, verbose=verbose)

            # crop the workspace
            workspace = self.cropWorkspace(greenPlatform, self.redMaskBGR, verbose=verbose)

            if(None in [self.cellList, self.cellCenters]):
                # grid workspace
                self.cellList, self.cellCenters = self.gridWorkspace(workspace, verbose=verbose)

            # analyse workspace
            self.cellAnalyser(workspace, self.cellList, self.cellCenters, verbose=verbose)


    def handDetector(self, verbose=False):
        """
        Function: handDetector, to detect whether if ther is a hand in the workspace.
        ---
        Parameters:
        @param: verbose, boolean, to show the output of the function. 
        ---
        @return: boolean, True if hand is detected, and False otherwise.
        """
        # Read image
        directory = self.imgPath+self.imgName
        if(not os.path.isfile(directory)):
            sys.exit("Error: Image doesn't exist!\n")

        img = cv2.imread(directory)
        undistorted = self.undistort(img)

        if self.greenRects is None:
            # mask the green color
            greenMask = self.HSV_mask(undistorted, 'green')
            greenMask, greenMaskBGR = self.Morhology(greenMask)
            # find the large rectangles
            self.greenRects = self.findMarkersContour(greenMask, minArea=10000)

        # crop the large rectangle
        greenPlatform = self.cropPlatform(self.greenRects, undistorted)

        #converting from gbr to hsv color space
        img_HSV = cv2.cvtColor(greenPlatform, cv2.COLOR_BGR2HSV)
        #skin color range for hsv color space  (0, 15, 0), (17,170,255)
        HSV_mask = cv2.inRange(img_HSV,(12, 145, 0), (22,210,255))
        HSV_mask = cv2.morphologyEx(HSV_mask, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))

        #converting from gbr to YCbCr color space
        img_YCrCb = cv2.cvtColor(greenPlatform, cv2.COLOR_BGR2YCrCb)
        #skin color range for hsv color space (0, 135, 85), (255,180,135)
        YCrCb_mask = cv2.inRange(img_YCrCb, (0, 135, 85), (255,180,135))
        YCrCb_mask = cv2.morphologyEx(YCrCb_mask, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))

        #merge skin detection (YCbCr and hsv)
        global_mask = cv2.bitwise_and(YCrCb_mask,HSV_mask)
        global_mask = cv2.medianBlur(global_mask,9)
        # global_mask = cv2.GaussianBlur(global_mask, (5, 5), 0)
        global_mask = cv2.morphologyEx(global_mask, cv2.MORPH_OPEN, np.ones((11, 11), np.uint8))

        # Find the big contours/blobs on the filtered image:
        contours, hierarchy = cv2.findContours(global_mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

        # Bounding Rects are stored here:
        boundRectsList = []

        # Process each contour 1-1:
        for i, c in enumerate(contours):

            # Approximate the contour to a polygon:
            contoursPoly = cv2.approxPolyDP(c, 3, True)

            # Convert the polygon to a bounding rectangle:
            boundRect = cv2.boundingRect(contoursPoly)

            # Get the bounding rect's data:
            rectX = boundRect[0]
            rectY = boundRect[1]
            rectWidth = boundRect[2]
            rectHeight = boundRect[3]

            # Estimate the bounding rect area:
            rectArea = rectWidth * rectHeight

            # Set a min area threshold
            minArea = 1000

            # Filter blobs by area:
            if rectArea > minArea:
                #Store the rect:
                boundRectsList.append(boundRect)

        # Visualize results
        if(verbose):        
            global_mask = np.stack([global_mask, global_mask, global_mask], axis=2)
            for i in range(len(boundRectsList)):

                # Get sorted rect:
                currentRect = boundRectsList[i]

                # Get the bounding rect's data:
                rectX = currentRect[0]
                rectY = currentRect[1]
                rectWidth = currentRect[2]
                rectHeight = currentRect[3]

            # show the detection
            cv2.namedWindow("handMask", cv2.WINDOW_NORMAL)
            cv2.imshow("handMask", cv2.bitwise_and(global_mask, greenPlatform))
            cv2.waitKey(1000)
            cv2.destroyAllWindows()

        if(len(boundRectsList)!=0):
            return True
        return False
#----------------------------------------------------------------------------------

# mypath = 'G:/Grenoble/Semester_4/Project_Codes/Problem_Domain/New_Domain_Problem/'

# proc = imageProcessor(imgPath=mypath, imgName='image.jpg')

# proc.stateAnalyzer(verbose=True)

# hand = proc.handDetector(verbose=True)
# print(hand)
# print(proc.cellsState, '\n', proc.swapState, '\n', proc.humanStock)

# {0: ['ws_11', 'b'], 1: ['ws_12', 'y'], 2: ['ws_13', 'g'], 3: ['ws_14', 'y'], 
#  4: ['ws_21', 'g'], 5: ['ws_22', 'y'], 6: ['ws_23', 'y'], 7: ['ws_24', 'y'], 
#  8: ['ws_31', 'b'], 9: ['ws_32', 'b'],10: ['ws_33', 'y'],11: ['ws_34', 'b'], 
# 12: ['ws_41', 'y'],13: ['ws_42', 'y'],14: ['ws_43', 'g'],15: ['ws_44', 'y']} 
# {'s1': 'g', 's2': 'g', 's3': 'g'}
# {'b_2x2': 1, 'b_2x4': 1, 'y_2x2': 1, 'y_2x4': 1}