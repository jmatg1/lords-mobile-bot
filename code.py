import os
import time
from datetime import datetime
from PIL import Image
from tkinter import Tk, Button, Text, END
from tkinter import ttk
import re
import cv2
import numpy as np
import math
import threading
from threading import Thread  # threading is better than the thread module
from subprocess import check_output

import cv2
import pytesseract
from datetime import datetime

tkWindow = Tk()
tkWindow.geometry('400x250')
tkWindow.title('Bullet ECho Bot v 4.3.1 By Jmatg1')


class Bot:
    work = 1
    screenshot = 0
    screenshotName = ''
    t1 = 0
    fight = 1
    device = 0
    controlsUnderBuilding = [(576, 431), (1059, 768)]
    thrdTrain = False
    runTimeTrain = False
    thrdAQ = False
    runTimeAQ = False
    thrdGQ = False
    runTimeGQ = False
    armySelectCord = [(356, 374), (650, 380), (1017, 491), (1234, 389)]
    armyCurrent = 0
    # def __init__(self):
    def shadeVariation(self, col, col2, shade=0):
        if shade == 0:
            return col == col2
        rezult = (abs(col[0] - col2[0]), abs(col[1] - col2[1]), abs(col[2] - col2[2]))
        shadowCount = 0
        for rgb in rezult:
            if rgb <= shade:
                shadowCount += 1
        return shadowCount == 3

    def getXYByColor(self, color, isGetSCreen=True, shade=0, startXY=(0, 0), endXY=(0, 0)):
        if (isGetSCreen):
            self.getScreen()
        img = self.screenshot
        coordinates = False

        if endXY[0] == 0 and endXY[1] == 0:
            endXY = (img.size[0], img.size[1])
        for x in range(img.size[0]):
            if not (startXY[0] < x < endXY[0]):
                continue

            for y in range(img.size[1]):
                if not (startXY[1] < y < endXY[1]):
                    continue
                if self.shadeVariation(img.getpixel((x, y))[:3], color, shade):
                    coordinates = (x, y)
                    continue
        return coordinates

    def pixelSearch(self, x1, y1, color):  # x2=1600, y2=900,
        # im = ImageOps.crop(im, (x1, y1, x2, y2))
        colorPixel = self.screenshot.getpixel((x1, y1))[:3]
        if colorPixel == color:
            return True
        else:
            return False

    def getScreen(self):
        self.shell(f'/system/bin/screencap -p /sdcard/{self.screenshotName}')
        # os.system('hd-adb shell /system/bin/screencap -p /sdcard/screenshot.png')
        # Using the adb command to upload the screenshot of the mobile phone to the current directory

        os.system(f'hd-adb -s {self.device} pull /sdcard/{self.screenshotName}')
        try:
            self.screenshot = Image.open(f"{self.screenshotName}")
        except ValueError:
            print(ValueError)
            self.getScreen()

    def getPixelColor(self, x1, y1):
        self.getScreen()
        im = Image.open(f"{self.screenshotName}")
        # im1 = ImageOps.crop(im, (0, 0, 1000, 300))
        # im1.show()
        pixelRGB = im.getpixel((x1, y1))[:3]
        return pixelRGB

    def click(self, x, y, timer=True):
        if (timer):
            time.sleep(1)
        # os.system(f'hd-adb shell input tap {x} {y}')
        self.shell(f'input tap {x} {y}')
        if (timer):
            time.sleep(1)

    def main(self):
        while self.work:
            self.getScreen()
            # self.getTimeTrain(942, 576, 152, 38, (255, 255, 255))

            self.detectAttack()

            self.getScreen()
            self.collectMysteryBox()

            self.getScreen()
            self.collectMysteryBox()

            if self.thrdTrain == False:
                self.startTrainBot()

            self.getScreen()
            if self.runTimeTrain == False:
                self.doTrainBot()

            self.getScreen()
            self.detectAttack()

            if self.thrdAQ == False:
                self.startAdminQuests()

            self.getScreen()
            if self.runTimeAQ == False:
                self.doQuestsAdmin()

            self.getScreen()
            self.detectAttack()

            if self.thrdGQ == False:
                self.startGuildQuests()

            self.getScreen()
            if self.runTimeGQ == False:
                self.doGuildQuests()

            self.getScreen()
            self.detectAttack()

            self.getScreen()
            self.helpTeam()


    def startAdminQuests(self):
        self.log('Open Quest')
        self.click(967, 834)
        self.log('Open Admin Quests')
        self.click(791, 189)
        self.getScreen()
        isAQExpiredSec = self.getTimeTrain(942, 576, 152, 38, (255, 255, 255))
        if isAQExpiredSec:
            self.log(f'Admin Quests Sleep: {str(isAQExpiredSec)} sec')
            self.thrdAQ = Thread(target=self.runAdminQuests, args=[isAQExpiredSec])
            self.thrdAQ.start()
        self.keyBack()

    def runAdminQuests(self, timeSec):
        self.thrdAQ = True
        self.runTimeAQ = True
        time.sleep(timeSec)
        self.thrdAQ = False
        self.runTimeAQ = False
        self.log('Stop Admin Quests')

    def doQuestsAdmin(self):
        self.log('Open Quest')
        self.click(967, 834)
        self.log('Open Admin Quests')
        self.click(791, 189)
        self.log('Double Click Quest Day')
        self.click(1278, 353)
        self.click(1278, 353)
        self.keyBack()

    def startGuildQuests(self):
        self.log('Open Guild')
        self.click(967, 834)
        self.log('Open Guild Quests')
        self.click(1065, 195)

        self.getScreen()

        isGQExpiredSec = self.getTimeTrain(942, 576, 152, 38, (255, 255, 255))
        if isGQExpiredSec:
            self.log(f'Guild Quests Sleep: {str(isGQExpiredSec)} sec')
            self.thrdGQ = Thread(target=self.runGuildQuests, args=[isGQExpiredSec])
            self.thrdGQ.start()
        else:
            self.log(isGQExpiredSec)
        self.keyBack()

    def runGuildQuests(self, timeSec):
        self.thrdGQ = True
        self.runTimeGQ = True
        time.sleep(timeSec)
        self.thrdGQ = False
        self.runTimeGQ = False
        self.log('Stop Guild Quests')

    def doGuildQuests(self):
        self.log('Open Guild')
        self.click(967, 834)
        self.log('Open Guild Quests')
        self.click(1065, 195)
        self.log('Double Click Guild')
        self.click(1278, 353)
        self.click(1278, 353)
        self.keyBack()

    def detectAttack(self):
        self.log('Check Attack...')
        cord = self.getXYByColor((212, 47, 47), True, 0, (1319, 83), (1386, 186))
        if cord:
            self.log('ATTACK!')
            self.log('Open Refuge')
            self.click(798, 326)
            isActive = self.getXYByColor((14, 97, 170), True, 0, (1040, 180), (1127, 240))
            if isActive:
                self.log('Shelter is active')
                self.keyBack()
                return
            self.log('Select 12h')
            self.click(989, 605)
            self.log('Open Army Refuge')
            self.click(798, 699)
            self.log('Activate Refuge')
            self.click(1239, 717)
    def collectMysteryBox(self):
        self.log('Check Mystery Box')
        isMysteryBoxReady = len(self.getText(1332, 722, 102, 31, (255,255,255))) > 6
        if isMysteryBoxReady:
            self.log('Open Mystery Box')
            self.click(1382, 650)
            self.log('Collect Mystery Box')
            cord = self.getXYByColor((176,118,44),True,0,(414,515),(1212, 867))
            if cord:
                self.click(cord[0], cord[1])
            else:
                self.log('Btn not found')
                self.keyBack()
        # else:
        #     self.log('Barak not Found')
    def startTrainBot(self):
        # cordBarak = self.getXYByImage()
        # if cordBarak:
        self.log('Open Train')
        self.click(1023, 654)
        self.getScreen()
        timeSec = self.getTimeTrain(1247, 194, 147, 45, (255,255,255))
        if timeSec:
            self.log(f'Train Sleep: {str(timeSec)} sec')
            self.thrdTrain = Thread(target=self.runTrain, args=[timeSec])
            self.thrdTrain.start()
        self.keyBack()
        # else:
        #     self.log('Barak not Found')

    def runTrain(self, timeSec):
        self.thrdTrain = True
        self.runTimeTrain = True
        time.sleep(timeSec)
        self.thrdTrain = False
        self.runTimeTrain = False
        self.log('Stop Train')

    def doTrainBot(self):
        self.log('Open Train')
        self.click(1023, 654)
        self.log('Select Army')
        self.click(self.armySelectCord[self.armyCurrent%4][0], self.armySelectCord[self.armyCurrent%4][1])
        self.armyCurrent+=1
        self.getScreen()
        self.addArmy()
        self.log('Train!')
        self.click(398, 422)
        self.getScreen()
        time.sleep(1)
        self.click(1380, 768)
        self.keyBack()
        self.getScreen()

    def helpTeam(self):
        self.log('Start Help Team')
        cord = self.getXYByColor((242, 192, 137), True, 1, (1440, 642), (1562, 743))
        if cord == False:
            cord = self.getXYByColor((237,175,121), True, 1, (1440, 642), (1562, 743))
        if cord:
            self.log('Collect Box')
            self.click(cord[0], cord[1])
            self.click(776, 819)
            self.keyBack()
        self.log('END Help Team\n')

    def clickBack(self):
        self.click(67, 50)

    def addArmy(self, ms=200):
        self.shell(f'input swipe 998 576 1367 576 {ms}')

    def keyQ(self):
        self.shell(f'input keyevent 45')

    def keyE(self):
        self.shell(f'input keyevent 33')

    def keyBack(self):
        self.shell(f'input keyevent 4')

    def start(self):
        self.device = inputDevice.get()
        self.screenshotName = self.device + '-screenshot.png'
        self.work = 1
        self.t1 = threading.Thread(target=self.main, args=[])
        self.t1.start()

    def stop(self):
        self.work = 0

    def closeWindow(self):
        self.work = 0
        tkWindow.destroy()

    def shell(self, cmd):
        os.system(f'hd-adb -s {self.device} shell {cmd}')

    def log(self, value):
        timeVal = datetime.now().strftime("%D %H:%M:%S")
        logString = "%s %s" % (timeVal, value)
        text.insert(END, logString + " \r\n")
        text.see("end")
        f = open("log.txt", "a")
        f.write(logString + " \r")
        f.close()

    def selectedDevice(self, event):
        self.device = inputDevice.get()

    def getXYByImage(self, imgSrc='icons/train.png'):
        img_rgb = cv2.imread(f"{self.screenshotName}")
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

        template = cv2.imread(imgSrc, 0)

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        threshold = 0.8
        loc = np.where(res >= threshold)
        if len(loc[0]) > 0:
            y = loc[0][0]
            x = loc[1][0]
            return (x, y)
        else:
            return False

    def getText(self, x, y, x1, y1, color):
        # img_rgb = cv2.imread('emulator-5554-screenshot.png')
        img_rgb = cv2.imread(self.screenshotName)
        (a, img_gray) = cv2.threshold(img_rgb, 127, 255, cv2.THRESH_BINARY)

        img_gray = img_gray[y:y + y1, x:x + x1]
        height, width, channels = img_gray.shape
        for x in range(height):
            for y in range(width):
                (b, g, r) = img_gray[x, y]
                if (b, g, r) != (255, 255, 255):
                    img_gray[x, y] = [0, 0, 0]

        # cv2.imshow('Detected', img_gray)
        # cv2.waitKey()
        cv2.imwrite('timeTrain.png', img_gray)

        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
        strTime = pytesseract.image_to_string('timeTrain.png').replace('\n', '').replace(' ', '')
        print(strTime)
        return (strTime)



    #
    getTimeTrainCount = 0
    def getTimeTrain(self, x,y, x1,y1, color):
        self.getTimeTrainCount+=1
        if self.getTimeTrainCount == 3:
            self.getTimeTrainCount = 0
            return None
        # img_rgb = cv2.imread('emulator-5554-screenshot.png')
        img_rgb = cv2.imread(self.screenshotName)
        (a, img_gray )= cv2.threshold(img_rgb, 127, 255, cv2.THRESH_BINARY)


        img_gray = img_gray[y:y+y1, x:x+x1]
        height, width, channels = img_gray.shape
        for x in range(height):
            for y in range(width):
                (b, g, r) = img_gray[x,y]
                if (b, g, r) != (255, 255, 255):
                    img_gray[x,y] = [0, 0, 0]
        # cv2.imshow('Detected', img_gray)
        # cv2.waitKey()
        cv2.imwrite('timeTrain.png', img_gray)
        # cv2.imshow('Detected', img_gray)

        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
        strTime = pytesseract.image_to_string('timeTrain.png').replace('\n', '').replace(' ', '')

        formatTime = '%H:%M:%S'
        print(len(strTime))
        print(strTime)

        if len(strTime) == 5 or len(strTime) == 7 or len(strTime) == 8:
            if len(strTime.split(':')) == 2:
                formatTime = '%M:%S'
            try:
                pt = datetime.strptime(strTime, formatTime)
            except ValueError:
                self.log('Time Train Invalid: ' + strTime)
                self.getScreen()
                self.getTimeTrain(x,y,x1,y1, color)
                return
            total_seconds = pt.second + pt.minute * 60 + pt.hour * 3600
            self.getTimeTrainCount = 0
            return (total_seconds)
        else:
            print('Error Time')
    # cv2.waitKey()


bot = Bot()
buttonStart = Button(tkWindow, text='Start', command=bot.start)
buttonStart.pack()
buttonStop = Button(tkWindow, text='Stop', command=bot.stop)
buttonStop.pack()

tkWindow.protocol("WM_DELETE_WINDOW", bot.closeWindow)
devList = check_output("hd-adb devices")
text = Text(tkWindow, height=10, width=50)
text.insert(END, devList)

print(devList)
devListArr = re.compile(r'emulator-\d\d\d\d').findall(str(devList))
print('ARRAY DEVICES', devListArr)
rezArr = []
for x in devListArr:
    if (x.startswith('emulator-')):
        rezArr.append(x)
print(rezArr)

inputDevice = ttk.Combobox(tkWindow, width=15)
inputDevice['values'] = rezArr
inputDevice.bind("<<ComboboxSelected>>", bot.selectedDevice)
inputDevice.current(0)
inputDevice.pack()
text.pack()

tkWindow.mainloop()
