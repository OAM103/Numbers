
import cv2
import pytesseract

for k in range(3):
    flag = 0
    capImg = cv2.VideoCapture('2.mp4')
    while(capImg.isOpened() and flag == 0):
        ret, image = capImg.read()
        if image is None:
            break

        if k == 0:
            crop_image = image[750:1000, 0:950]
        if k == 1:
            crop_image = image[550:800, 1000:2550]
        if k == 2:
            crop_image = image[350:600, 0:1150]

        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        # teractTess — свободная компьютерная программа для распознавания текстов
        # Оттенки серого, размытие по Гауссу
        gray_crp = cv2.cvtColor(crop_image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray_crp, (3,3), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # Преобразование для удаления шума и инвертирования изображения
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
        invert = 255 - opening

        # Выполнить извлечение текста
        data = pytesseract.image_to_data(gray_crp, config="--psm 6", output_type=pytesseract.Output.DICT)

        word_occurences = [i for i, word in enumerate(data['text'])]
        #print(data['text'])
        for i in word_occurences:
            for j in range(len(data['text'][i])):
                if data['text'][i][j].isdigit() is True:
                    print(data['text'][i][j])
                    flag = 1
                    break

cv2.imshow('1', image[750:1000, 0:950])
cv2.imshow('2', image[550:800, 1000:2550])
cv2.imshow('3', image[350:600, 0:1150])
cv2.waitKey()