import cv2
import numpy as np
import test_csv
# import showPixelTemp as spt

show = False

def onTrackbarActivity(x):
    global show
    show = True
    pass

def showPixelValue(event, x, y, flags, param):
    global original, combinedResult, placeholder, tmin, tmax
    
    if event == cv2.EVENT_MOUSEMOVE:
        bgr = resultBGR[y, x]
        temperature = tmin + ((int(bgr[2]) + int(bgr[1]))/(510))*(tmax-tmin)
        temperature = round(temperature, 2)
        placeholder = np.zeros((resultBGR.shape[0], 400, 3), dtype=np.uint8)
        cv2.putText(placeholder, 'temp = {} C'.format(temperature), (20, 70), cv2.FONT_HERSHEY_COMPLEX, .9, (0,255,0), 1, cv2.LINE_AA)
        combinedResult = np.hstack([resultBGR, placeholder])
        cv2.imshow('Image', combinedResult)

#Перевод температуры в формат RGB относительно минимальной и максимальной температуры.
def tempToGR(temperature, tmin, tmax):
    R = 0
    G = 0 
    GR = 510*(temperature - tmin)/(tmax-tmin)
    if GR > 255:
        R = 255
        G = GR - 255
    else:
        G = 0
        R = GR
    return G, R

if __name__ == '__main__':
    
    global tmin, tmax, original, resultBGR
    
    fl = test_csv.readTemp('file/output.csv')
    i = 1
    filename = str(fl[i][0])
    filename = 'images/infrared/' + filename
    
    original = cv2.imread(filename)
    # mask = cv2.imread('images/mask/IR000002.bmp')
    wsize = 640
    hsize = 480
    # mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    # _, thresh = cv2.threshold(mask, 150, 255, cv2.THRESH_BINARY)
    # bitwiseAnd = cv2.bitwise_and(original, original, mask = thresh)
    
    original = cv2.resize(original, (wsize, hsize))
    resultBGR = original.copy()
    
    tmax = float(fl[i][2])
    tmin = float(fl[i][1])
    tmax = int(tmax)
    tmin = int(tmin)
    
    initialX = 20
    initialY = 20
    
    cv2.namedWindow('Image', cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow('SelectTemp', cv2.WINDOW_NORMAL)
    
    cv2.moveWindow('Image', initialX, initialY)
    cv2.moveWindow('SelectTemp', initialX, initialY+hsize+30)
    
    cv2.createTrackbar('Temp_Min','SelectTemp',tmin,tmax,onTrackbarActivity)
    cv2.createTrackbar('Temp_Max','SelectTemp',tmin,tmax,onTrackbarActivity)
    
    cv2.setMouseCallback('Image', showPixelValue)
    
    cv2.imshow('Image', original)
    k = 0
    while 1:
        # cv2.imshow('Image', original)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'):
            break
        
        if show:
            show = False
            Tmin = cv2.getTrackbarPos('Temp_Min','SelectTemp')
            Tmax = cv2.getTrackbarPos('Temp_Max','SelectTemp')
            
            GMin, RMin = tempToGR(Tmin, tmin, tmax)
            GMax, RMax = tempToGR(Tmax, tmin, tmax)
            
            minBGR = np.array([0, GMin, RMin])
            maxBGR = np.array([0, GMax, RMax])
            
            imageBGR = np.copy(original)
            
            maskBGR = cv2.inRange(imageBGR,minBGR,maxBGR)
            resultBGR = cv2.bitwise_and(original, original, mask = maskBGR)
            
            cv2.imshow('Image',resultBGR)
    
    cv2.destroyAllWindows()
            
            
            
