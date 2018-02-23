from PIL import Image
import pytesseract
import glob


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

theme = 'lishi'

# read from current directory
dataFile = open(theme + ".txt", "r+")
for line in dataFile:
    que, ans = line.split('\t')
    dirc[que] = ans

for filename in glob.glob(theme + '/*.png'):
    print('-------------------------------')
    img_org = Image.open(filename)
    pix_data = img_org.load()
    ans = -1  # index of correct ans (green)
    for i, v in enumerate(ans_sum):
        if pix_data[v][1] == 204:
            ans = i
            break

    # not a valid screenshot
    if ans == -1:
        print('does not find an answer')
        continue

    question_im = img_org.crop((que_left_up[0], que_left_up[1], que_right_down[0], que_right_down[1]))
    ans_img = img_org.crop(
        (ans_sum[ans][0], ans_sum[ans][1], ans_sum[ans][0] + ans_width, ans_sum[ans][1] + ans_height))

    que_new = ocr(question_im)
    ans_new = ocr(ans_img)
    if que_new == '' or ans_new == '':
        continue

    if que_new in dirc:
        print('**existing: ' + que_new + dirc[que_new])
    else:
        dirc[que_new] = ans_new
        dataFile.write(que_new + '\t' + ans_new + '\n')
        print('add: ' + que_new + '\t' + ans_new)

dataFile.close()
