#! /usr/bin/python3
# -*- coding: utf-8 -*-

'''
| author:
| Belal HMEDAN, LIG lab/ Marven Team, France, 2021.
| image processing script.
'''
"""
Reference:
https://stackoverflow.com/a/66863584
"""

# Importing cv2 and numpy:
import numpy as np
import cv2

#=======================
# class imageProcessor |
#=======================
class imageProcessor():

    def __init__(self, imgPath, imgName='image.jpg', verbose=False):
        """
        Class imageProcessor: Read and Process image to get world state.
        ---
        Parameters:
        @param: imgPath, string, the path to the image to process.
        @param: imgName, string, the name of the image including the extension.
        @param: verbose, boolean, to show the output of the function.
        """

        self.imgPath = imgPath
        self.imgName = imgName
        self.workspaceCoords = None
        self.cellsState = {
        # First column
        0:  ['ws_11', 'g'],
        1:  ['ws_12', 'g'],
        2:  ['ws_13', 'g'],
        3:  ['ws_14', 'g'],
        # Second column
        4:  ['ws_21', 'g'],
        5:  ['ws_22', 'g'],
        6:  ['ws_23', 'g'],
        7:  ['ws_24', 'g'],
        # Third column
        8:  ['ws_31', 'g'],
        9:  ['ws_32', 'g'],
        10: ['ws_33', 'g'],
        11: ['ws_34', 'g'],
        # Fourth column
        12: ['ws_41', 'g'],
        13: ['ws_42', 'g'],
        14: ['ws_43', 'g'],
        15: ['ws_44', 'g']
        }
        self.swapState = {
        # Swap
        0: ['s1'   , 'g'],
        1: ['s2'   , 'g'],
        2: ['s3'   , 'g']
        }

    def HSV_mask(self, lower=[127, 0, 95], upper=[179, 255, 255], verbose=False):
        """
        Function: HSV_mask, to threshold the image in HSV colorspace within given range.
        ---
        Parameters:
        @param: lower, list, the lower values of the Hue, Saturaion, Value.
        @param: upper, list, the upper values of the Hue, Saturaion, Value.
        @param: verbose, boolean, to show the output of the function.
        ---
        @return: mask, nd array binary mask resulting from HSV masking,
                inputCopy, nd array, deepcopy of the original image.
        """

        # Reading an image in default mode:
        inputImage = cv2.imread(self.imgPath + self.imgName)
        # Store a deep copy for results:
        inputCopy = inputImage.copy()

        # Convert the image to HSV:
        hsvImage = cv2.cvtColor(inputImage, cv2.COLOR_BGR2HSV)

        # The HSV mask values (Red):
        lowerValues = np.array(lower)
        upperValues = np.array(upper)

        # Create the HSV mask
        mask = cv2.inRange(hsvImage, lowerValues, upperValues)

        # Visualize results
        if(verbose):
            cv2.namedWindow('HSV mask', cv2.WINDOW_NORMAL)
            cv2.imshow('HSV mask', mask)
            cv2.waitKey(0)

        return mask, inputCopy

    def Morhology(self, mask, k=5, iters=10, verbose=False):
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
                maskCopy, nd array, deepcopy of the mask in BGR.
        """
        # Get the structuring element:
        maxKernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(k, k))
        # Perform closing:
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, maxKernel, None, None, iters, cv2.BORDER_REFLECT101)

        # Visualize results
        if(verbose):
            cv2.namedWindow('Morphology mask', cv2.WINDOW_NORMAL)
            cv2.imshow('Morphology mask', mask)
            cv2.waitKey(0)

        # Create a deep copy, convert it to BGR for results:
        maskCopy = mask.copy()
        maskCopy = cv2.cvtColor(maskCopy, cv2.COLOR_GRAY2BGR)

        return mask, maskCopy

    def findMarkersContour(self, mask):
        """
        Function: findMarkersContour, to find the contours of the red markers.
        ---
        Parameters:
        @param: mask, nd array binary mask resulting from HSV masking, and Morpholigical closing.
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

            # Set a min area threshold
            minArea = 100

            # Filter blobs by area:
            if rectArea > minArea:
                #Store the rect:
                boundRectsList.append(boundRect)

        # Sort the list based on ascending y values:
        boundRectsSorted = sorted(boundRectsList, key=lambda x: x[1])

        return boundRectsSorted

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
            thickness = -1
            centerX = rectX + borderPoint[0]
            centerY = rectY + borderPoint[1]
            radius = 50
            cv2.circle(maskCopy, (centerX, centerY), radius, color, thickness)

            # Mark the circle
            org = (centerX - 20, centerY + 20)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(maskCopy, str(rectCounter), org, font,
                    2, (0, 0, 0), 5, cv2.LINE_8)

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
            cv2.waitKey(0)

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
        if(self.workspaceCoords is not None):
            # Check out the big rectangle at the center:
            bigRectX = self.workspaceCoords[0]
            bigRectY = self.workspaceCoords[1]
            bigRectWidth = self.workspaceCoords[2]
            bigRectHeight = self.workspaceCoords[3]
            # Draw the big rectangle:
            cv2.rectangle(maskCopy, (int(bigRectX), int(bigRectY)), (int(bigRectX + bigRectWidth),
                                 int(bigRectY + bigRectHeight)), (0, 0, 255), 5)

            # Visualize results
            if(verbose):
                cv2.namedWindow("Big Rectangle", cv2.WINDOW_NORMAL)
                cv2.imshow("Big Rectangle", maskCopy)
                cv2.waitKey(0)

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
            cv2.waitKey(0)

        return cellList, cellCenters

    def cellAnalyser(self, centerPortion, cellList, cellCenters, verbose=False):
        """
        Function: cellAnalyser, to recognize the color of each cell.
        ---
        Parameters:
        @param: centerPortion, nd array, cropped workspace.
        @param: cellList, list, cells coordinates list.
        @param: cellCenters, list, cells centers list.
        @param: verbose, boolean, to show the output of the function. 
        ---
        @return: None
        """
        # HSV dictionary - color ranges and color name:
        colorDictionary = {0: ([93, 64, 21], [121, 255, 255], "blue"  ),
                           1: ([20, 64, 21], [30, 255,  255], "yellow"),
                           2: ([55, 64, 21], [92, 255,  255], "green" )}

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
                    self.cellsState[c]=colorDictionary[m][2][0]
            # Get cell center, add an x offset:
            textX = int(cellCenters[cellCounter][0]) - 100
            textY = int(cellCenters[cellCounter][1])

            # Draw text on cell's center:
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(centerPortion, cellColor, (textX, textY), font,
                            2, (0, 0, 255), 5, cv2.LINE_8)

            # Increase cellCounter:
            cellCounter += 1

        # Visualize results
        if(verbose):
            cv2.namedWindow("centerPortion", cv2.WINDOW_NORMAL)
            cv2.imshow("centerPortion", centerPortion)
            cv2.waitKey(0)

    def swapAnalyser(self, inputCopy, swapBorders):
        """
        Function: swapAnalyser, to recognize the color of each swap cell.
        ---
        Parameters:
        @param: inputCopy, nd array, deepcopy of the original image.
        @param: swapBorders, list, swap border points list.
        ---
        @return: None
        """
        # HSV dictionary - color ranges and color name:
        colorDictionary = {0: ([93, 64, 21], [121, 255, 255], "blue"  ),
                           1: ([20, 64, 21], [30, 255,  255], "yellow"),
                           2: ([55, 64, 21], [92, 255,  255], "green" )}

        for idx, border in enumerate(swapBorders):
             # Get current Cell:
            currentCell = inputCopy[border[0]:border[2], border[1]:border[3]]
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
                    self.swapState[idx]=colorDictionary[m][2][0]

    def stateAnalyzer(self):
        """
        Function: stateAnalyzer, to get the state of the workspace/swap.
        ---
        Parameters:
        @param: None
        ---
        @return: None
        """
        mask, inputCopy       = self.HSV_mask()
        mask, maskCopy        = self.Morhology(mask)
        boundRectsSorted      = self.findMarkersContour(mask)
        maskCopy              = self.centerMarkersContour(maskCopy, boundRectsSorted)
        centerPortion         = self.cropWorkspace(inputCopy, maskCopy)
        cellList, cellCenters = self.gridWorkspace(centerPortion)
        self.cellAnalyser(centerPortion, cellList, cellCenters)
        # These borderes to be modified later when fixing the camera.
        swapBorders = [(0, 0, 1, 1), (1, 1, 2, 2), (2, 2, 3, 3), (3, 3, 4, 4)]
        self.swapAnalyser(inputCopy, swapBorders)

    def handDetector(self, verbose=False):
        """
        Function: handDetector, to detect whether if ther is a hand in the workspace.
        ---
        Parameters:
        @param: None
        ---
        @return: boolean, True if hand is detected, and False otherwise.
        """
        # Read image
        img = cv2.imread(self.imgPath + self.imgName)
        #converting from gbr to hsv color space
        img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        #skin color range for hsv color space 
        HSV_mask = cv2.inRange(img_HSV, (0, 15, 0), (17,170,255)) 
        HSV_mask = cv2.morphologyEx(HSV_mask, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))

        #converting from gbr to YCbCr color space
        img_YCrCb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
        #skin color range for hsv color space 
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
            minArea = 1200

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

                # Draw contour rect:
                cv2.rectangle(global_mask, (int(rectX), int(rectY)), (int(rectX + rectWidth),
                                         int(rectY + rectHeight)), (0, 255, 0), 5)     
            # show the detection
            cv2.namedWindow("handMask", cv2.WINDOW_NORMAL)
            cv2.imshow("handMask", global_mask)
            cv2.waitKey(0)

        if(len(boundRectsList)!=0):
            return True
        return False
#----------------------------------------------------------------------------------

# proc = imageProcessor('F:/Grenoble/Semester_4/Project_Codes/Problem_Domain/New_Domain_Problem/')
# proc.handDetector(verbose=True)
# proc.stateAnalyzer()
# print(proc.cellsState, proc.swapState)