import os
from PIL import Image
import pytesseract
import time


# Chinese extraction
def ocr(img):
    def binarizing(threshold):
        pixdata = img.load()
        w, h = img.size
        for y in range(h):
            for x in range(w):
                if pixdata[x, y] < threshold:
                    pixdata[x, y] = 0
                else:
                    pixdata[x, y] = 255
        return img
    img = img.convert('L')
    img = binarizing(190)
    words = pytesseract.image_to_string(img, lang='chi_sim')
    words = words.strip().replace("\n", "").replace("\t", "").replace(' ', '')
    return words


# Galaxy S8 conf
que_left_up = (50, 500)
que_right_down = (1030, 700)
ans0_left_up = (80, 1170)
ans1_left_up = (80, 1412)
ans2_left_up = (80, 1660)
ans3_left_up = (80, 1900)
ans_sum = (ans0_left_up, ans1_left_up, ans2_left_up, ans3_left_up)
ans_width = 920
ans_height = 188

dirc = {}
theme = 'shishang'

# read from current directory
dataFile = open(theme + ".txt", "r+")
for line in dataFile:
    que, ans = line.split('\t')
    dirc[que] = ans

while 1:
    go = input('输入回车继续运行,输入 n 回车结束运行: ')
    if go == 'n':
        break
    os.system('adb shell screencap -p /sdcard/screenshot.png')
    os.system('adb pull /sdcard/screenshot.png .')
    img_org = Image.open('screenshot.png')
    question_im = img_org.crop((que_left_up[0], que_left_up[1], que_right_down[0], que_right_down[1]))
    que_new = ocr(question_im)
    print('question: ' + que_new)
    if que_new in dirc:
        print(dirc[que_new])
    elif que_new != '':
        print('XXXXX')
        time.sleep(4)
        os.system('adb shell screencap -p /sdcard/screenshot.png')
        os.system('adb pull /sdcard/screenshot.png .')
        img_org = Image.open('screenshot.png')
        pix_data = img_org.load()
        ans = -1  # index of correct ans (green)
        for i, v in enumerate(ans_sum):
            if pix_data[v][1] == 204:
                ans = i
                break
        # not a valid screenshot
        if ans == -1:
            continue
        ans_img = img_org.crop(
            (ans_sum[ans][0], ans_sum[ans][1], ans_sum[ans][0] + ans_width, ans_sum[ans][1] + ans_height))

        ans_new = ocr(ans_img)
        if ans_new == '':
            continue
        dirc[que_new] = ans_new
        dataFile.write(que_new + '\t' + ans_new + '\n')
        print('add: ' + que_new + '\t' + ans_new)
    else:
        print('XXXXX')

dataFile.close()
