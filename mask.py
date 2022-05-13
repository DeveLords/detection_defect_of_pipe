import cv2
import numpy as np

# Функция позволяет определеить среднее значение матрицы, 
# в случае, если среднее значение уже определено, 
# то можно передать в эту функцию второй параметр, 
# являющися значением, расчитанным по этой же функции
def findMean(matrixSum, matrixMean= None, oper= None): 
    lenght = 0
    summa = 0
    if matrixMean == None:
        for i in range(len(matrixSum)):
            for j in range(len(matrixSum[i])):
                if matrixSum[i][j]:
                    summa += matrixSum[i][j]
                    lenght += 1
    else:
        if oper == None or oper == '>':
            for i in range(len(matrixSum)):
                for j in range(len(matrixSum[i])):
                    if matrixSum[i][j] > matrixMean:
                        summa += matrixSum[i][j]
                        lenght += 1
        elif oper == '<':
            for i in range(len(matrixSum)):
                for j in range(len(matrixSum[i])):
                    if matrixSum[i][j] != 0 and matrixSum[i][j] < matrixMean:
                        summa += matrixSum[i][j]
                        lenght += 1
    mean = summa / lenght
    return mean, lenght

#Функция перевода из rgb в температуру по палитре горячий металл  
def rgbToTemperature(rg, tMin, tMax):
    temp = tMin + rg / 510 * (tMax - tMin)
    return temp

# Поиск области в пределах конкретных температур
def findArea(originalImage, matrixSumRGB, mean):
    for i in range(len(matrixSumRGB)):
        for j in range(len(matrixSumRGB[i])):
            if matrixSumRGB[i][j] < mean:
                originalImage[i][j] = [0, 0, 0]
    return originalImage

# Объединенеие изображений по требуемым пределам
def combineImage(originalImage, infraImage):
    rows, cols = originalImage.shape[:2]
    irows, icols = infraImage.shape[:2]
    x = int((rows - irows) / 2 - 1)
    y = int((cols - icols) / 2 - 1)
    for i in range(len(infraImage)):
        for j in range(len(infraImage[i])):
            if infraImage[i][j].sum():
                rgb = infraImage[i][j]
                originalImage[x+i][y+j] = rgb
    return originalImage        
    
visible = cv2.imread('images/visible/IR000002.bmp')
original = cv2.imread('images/infrared/IR000002.bmp')
mask = cv2.imread('images/mask/IR000002.bmp')

mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

_, threshMask = cv2.threshold(mask, 150, 255, cv2.THRESH_BINARY)

combinedImage = cv2.bitwise_and(original, original, mask= threshMask)

matrixSumrgb = np.zeros((240, 320), dtype= np.uint16)

for i in range(len(combinedImage)):
    for j in range(len(combinedImage[i])):
        matrixSumrgb[i][j] = combinedImage[i][j].sum()

imgMean, lenMean = findMean(matrixSumrgb)
meanCold, lenCold = findMean(matrixSumrgb, imgMean, '>')
meanHot, lenHot = findMean(matrixSumrgb, imgMean, '<')

temp = rgbToTemperature(imgMean, 21, 70)
tempMeanCold = rgbToTemperature(meanCold, 21, 70)
tempMeanHot = rgbToTemperature(meanHot, 21, 70)

newImage = findArea(combinedImage, matrixSumrgb, meanCold)

combImage = combineImage(visible, newImage)

cv2.imshow('newImage', newImage)
cv2.imshow('original', original)
cv2.imshow('visible', visible)
cv2.imshow('combImage', combImage)
cv2.waitKey(0)


