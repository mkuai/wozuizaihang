from PIL import Image
import pytesseract

img = Image.open("test4.png")


# 二值化算法
def binarizing(img, threshold):
    pixdata = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            if pixdata[x, y] < threshold:
                pixdata[x, y] = 0
            else:
                pixdata[x, y] = 255
    return img

# Galaxy S8
question_im = img.crop((0, 500, 1080, 700))
ans0_im = img.crop((80, 1170, 1000, 1360))
ans1_im = img.crop((80, 1412, 1000, 1600))
ans2_im = img.crop((80, 1658, 1000, 1845))
ans3_im = img.crop((80, 1900, 1000, 2085))


ans0_im = question_im.convert('L')
ans0_im = binarizing(ans0_im, 190)
ans0_im.show()
ans = pytesseract.image_to_string(ans0_im, lang='chi_sim')
ans = ans.replace("\n", "")

print(ans)

# question = pytesseract.image_to_string(question_im, lang='chi_sim')
# question = question.replace("\n", "")
# print(question)
#
# for ans_im in (ans0_im, ans1_im, ans2_im, ans3_im):
#     ans = pytesseract.image_to_string(ans_im, lang='chi_sim')
#     ans = ans.replace("\n", "")
#     print(ans)

