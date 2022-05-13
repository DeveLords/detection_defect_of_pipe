import cv2 as cv

img1 = cv.imread('images/testImage/bg.jpg')
img2 = cv.imread('dice.png')

brows, bcols = img1.shape[:2]
rows,cols,channels = img2.shape
# Ниже я изменил roi, чтобы картинка выводилась посередине, а не в левом верхнем углу
roi = img1[int(brows/2)-int(rows/2):int(brows/2)+int(rows/2), int(bcols/2)- 
int(cols/2):int(bcols/2)+int(cols/2) ]

img2gray = cv.cvtColor(img2,cv.COLOR_BGR2GRAY)
ret, mask = cv.threshold(img2gray, 10, 255, cv.THRESH_BINARY)
mask_inv = cv.bitwise_not(mask)

img1_bg = cv.bitwise_and(roi,roi,mask = mask_inv)

img2_fg = cv.bitwise_and(img2,img2,mask = mask)

dst = cv.add(img1_bg,img2_fg)
img1[int(brows/2)-int(rows/2):int(brows/2)+int(rows/2), int(bcols/2)- 
int(cols/2):int(bcols/2)+int(cols/2) ] = dst
cv.imwrite('res.jpg',img1)