import cv2
import argparse
import numpy as np

img= cv2.imread("braille_scan.png",cv2.CV_8UC1)

#Invert the image
cv2.bitwise_not(img)
cv2.imwrite('E:\\Semester 4\\MiniProject\\Braille-OCR-master\\Mask\\img.jpg',img)

#conversion in threshold using the RGB value of the pixel
ret, thresh = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
cv2.imwrite('E:\\Semester 4\\MiniProject\\Braille-OCR-master\\Mask\\t1.jpg',thresh)
blur = cv2.blur(thresh,(5,5))
cv2.imwrite('E:\\Semester 4\\MiniProject\\Braille-OCR-master\\Mask\\blur.jpg',blur)

kernel = np.ones((5,5),np.uint8)
cv2.imwrite('E:\\Semester 4\\MiniProject\\Braille-OCR-master\\Mask\\kernel.jpg',kernel)
print(kernel)
erosion = cv2.erode(blur,kernel,iterations = 1)
ret, thresh2 = cv2.threshold(erosion, 12, 255, cv2.THRESH_BINARY)
cv2.imwrite('E:\\Semester 4\\MiniProject\\Braille-OCR-master\\Mask\\t2.jpg',thresh2)
cv2.imwrite('E:\\Semester 4\\MiniProject\\Braille-OCR-master\\Mask\\erosion.jpg',erosion)

kernel = np.ones((3,2),np.uint8)
print(kernel)
cv2.imwrite('E:\\Semester 4\\MiniProject\\Braille-OCR-master\\Mask\\kernel1.jpg',kernel)
mask = cv2.dilate(thresh2,kernel,iterations = 1)
rows,cols=mask.shape
cv2.imwrite('E:\\Semester 4\\MiniProject\\Braille-OCR-master\\Mask\\mask.jpg',mask)

# cropping 
refPt = []
cropping = False
 
def click_and_crop(event, x, y, flags, param):
        global refPt, cropping
 
        # if the left mouse button was clicked, record the starting
        # (x, y) coordinates and indicate that cropping is being
        # performed
        if event == cv2.EVENT_LBUTTONDOWN:
                refPt = [(x, y)]
                cropping = True
 
        # check to see if the left mouse button was released
        elif event == cv2.EVENT_LBUTTONUP:
                # record the ending (x, y) coordinates and indicate that
                # the cropping operation is finished
                refPt.append((x, y))
                cropping = False
 
                # draw a rectangle around the region of interest
                cv2.rectangle(mask, refPt[0], refPt[1], (255, 255, 255), 2)
                cv2.namedWindow('image',cv2.WINDOW_NORMAL)
                cv2.resizeWindow('image',  rows,cols)
                cv2.imshow("image", mask)

# load the image, clone it, and setup the mouse callback function
clone = mask.copy()
cv2.namedWindow("image" ,cv2.WINDOW_NORMAL)
cv2.resizeWindow('image',  rows,cols)
cv2.setMouseCallback("image", click_and_crop)
 
# keep looping until the 'q' key is pressed
while True:
        # display the image and wait for a keypress
        cv2.namedWindow("image" ,cv2.WINDOW_NORMAL) 
        cv2.resizeWindow('image',  rows,cols)
        cv2.imshow("image", mask)
        key = cv2.waitKey(1) & 0xFF
 
        # if the 'r' key is pressed, reset the cropping region
        if key == ord("r"):
                image = clone.copy()
 
        # if the 'c' key is pressed, break from the loop
        elif key == ord("c"):
                break
 
# if there are two reference points, then crop the region of interest from the image and display it
if len(refPt) == 2:
        roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
        cv2.imwrite('roi.jpg',roi)

        cv2.namedWindow("ROI" ,cv2.WINDOW_NORMAL)
        cv2.resizeWindow('ROI',refPt[0][1]-refPt[1][1], refPt[0][0]-refPt[1][0] )
        cv2.imshow("ROI", roi)
       
cv2.waitKey(0)
cv2.destroyAllWindows()
