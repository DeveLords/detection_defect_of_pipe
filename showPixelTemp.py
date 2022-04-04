import cv2, argparse
import numpy as np

def showPixelValue(event, x, y, flags, param):
    global img, combinedResult, placeholder
    
    if event == cv2.EVENT_MOUSEMOVE:
        bgr = img[y, x]
        temperature = 20 + (bgr[-1] + bgr[1])/510*(100-20)
        temperature = round(temperature, 2)
        placeholder = np.zeros((img.shape[0], 400, 3), dtype=np.uint8)
        cv2.putText(placeholder, 'temp = {}'.format(temperature), (20, 70), cv2.FONT_HERSHEY_COMPLEX, .9, (255,255,255), 1, cv2.LINE_AA)
        combinedResult = np.hstack([img, placeholder])
        cv2.imshow('Img', combinedResult)
        
global img
img = cv2.imread('images/testInfra.bmp') 
    
cv2.namedWindow('Img')
cv2.setMouseCallback('Img', showPixelValue)
temp = img.copy()
k = 0
while k!=113:
    cv2.imshow('Img', img)
    k = cv2.waitKey(0)
cv2.destroyAllWindows()
       