import cv2, argparse
import numpy as np
import test_csv

def showPixelValue(event, x, y, flags, param):
    global img, combinedResult, placeholder, t_min, t_max
    
    if event == cv2.EVENT_MOUSEMOVE:
        bgr = img[y, x]
        temperature = t_min + ((int(bgr[2]) + int(bgr[1]))/(510))*(t_max-t_min)
        temperature = round(temperature, 2)
        placeholder = np.zeros((img.shape[0], 400, 3), dtype=np.uint8)
        cv2.putText(placeholder, 'temp = {} C'.format(temperature), (20, 70), cv2.FONT_HERSHEY_COMPLEX, .9, (0,255,0), 1, cv2.LINE_AA)
        combinedResult = np.hstack([img, placeholder])
        cv2.imshow('Image', combinedResult)
        
global img, t_max, t_min

fl = test_csv.readTemp('file/output.csv')

i = 1

filename = str(fl[i][0])

filename = 'images/infrared/' + filename

img = cv2.imread(filename)
img = cv2.resize(img, (640, 480))
t_max = float(fl[i][2])
t_min = float(fl[i][1])

    
cv2.namedWindow('Image')
cv2.setMouseCallback('Image', showPixelValue)
temp = img.copy()
k = 0
while k!=113:
    cv2.imshow('Img', img)
    k = cv2.waitKey(0)
cv2.destroyAllWindows()
       