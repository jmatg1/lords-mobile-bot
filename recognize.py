import cv2
import pytesseract
from datetime import datetime
#
def getTimeTrain(screenshotName):
    img_rgb = cv2.imread(screenshotName)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    img_gray=img_gray[197:197+37, 1274:1274+115]
    cv2.imwrite('timeTrain.png', img_gray)
    # cv2.imshow('Detected', img_gray)

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
    strTime = pytesseract.image_to_string('timeTrain.png').replace('\n','').replace(' ','')

    formatTime = '%H:%M:%S'
    print(len(strTime))
    print(strTime)
    if len(strTime) == 5 or len(strTime) == 7 or len(strTime) == 8:
        if len(strTime.split(':')) == 2:
            formatTime = '%M:%S'

        pt = datetime.strptime(strTime, formatTime)
        total_seconds = pt.second + pt.minute * 60 + pt.hour * 3600
        return (total_seconds)
    else:
        print('Error Time')
# cv2.waitKey()