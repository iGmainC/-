import cv2
from PIL import Image,ImageFont,ImageDraw
import numpy as np
from copy import copy

cap = cv2.VideoCapture(0)
#cap.set(3,1920)
#cap.set(4,1080)
cap.set(3,160)
cap.set(4,120)
'''
创建摄像头对象
0为第一个摄像头
'''
font = ImageFont.truetype('1.ttf',index=0)
ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")

def opencv_to_pil(img):
    return Image.fromarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))

def pil_to_opencv(img):
    return cv2.cvtColor(np.asarray(img),cv2.COLOR_RGB2BGR)

def get_char(gray):
    return ascii_char[int(gray / ((256.0 + 1) / len(ascii_char)))]

def r_rw(li):
    List = []
    if str(type(li[0][0])) == "<class 'numpy.uint8'>":
        for x in range(len(li)):
            List_line = []
            for y in range(len(li[0])):
                List_line.append(li[x][y])
            List.append(List_line)
    else:
        for x in range(len(li)):
            List_line = []
            for y in range(len(li[0])):
                List_line.append(tuple(li[x][y]))
            List.append(List_line)
    return List

def img_to_charimg(img):
    img = opencv_to_pil(img)
    x,y = img.size
    img_ = img.resize((x,int(y * 0.5)))
    img_L = r_rw(np.asarray(img_.convert('L')))
    img_RGB = r_rw(np.asarray(img_))
    for x in range(len(img_L)):
        for y in range(len(img_L[0])):
            img_L[x][y] = get_char(img_L[x][y])
    img_draw = Image.new('RGB',(len(img_L[0]) * 5,len(img_L) * 10),(255,255,255))
    draw = ImageDraw.Draw(img_draw)
    for ch_l,color_l,y in zip(img_L,img_RGB,range(len(img_L))):
        for ch,color,x in zip(ch_l,color_l,range(len(img_L[0]))):
            draw.text((x * 5,y * 10),ch,fill=color,font=font)
    return pil_to_opencv(img_draw)

while(1):
    ret,frame = cap.read()
    if not ret:
        print('摄像头未打开')
        cap.open()
        continue
    cv2.imshow('qqq',frame)
    if list(frame[0][0]) == [0,0,0]:
        l = len(frame)
        frame = frame[int(l/8):int(l/8*6)]
    cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    #cv2.fastNlMeansDenoisingColored(frame,None,10,10,7,21)
    frame = img_to_charimg(frame)
    frame = np.asarray(frame)
    cv2.imshow('video',frame)
    a = cv2.waitKey(1)
    print(a)
    if a == 27:
        break
cap.release()
'''
关闭摄像头
'''

cv2.destroyAllWindows()
