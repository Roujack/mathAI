import cv2
import numpy as np
from skimage.morphology import skeletonize
from config import IMG_SIZE,FILELIST,MODEL_DIR,\
    SPACIAL_RELATIONSHIP as spartial_relationship,\
    LARGEST_NUMBER_OF_SYMBOLS,SCALSIZE
from matplotlib import pyplot as plot


#读取图片并将图片转化成二值图,返回原彩色图和二值图
def read_img_and_convert_to_binary(filename):
    #读取待处理的图片
    original_img = cv2.imread(filename)
    # print(original_img)
    #将原图分辨率缩小SCALSIZE倍，减少计算复杂度
    original_img = cv2.resize(original_img,(np.int(original_img.shape[1]/SCALSIZE),np.int(original_img.shape[0]/SCALSIZE)), interpolation=cv2.INTER_AREA)
    #降噪
    blur = cv2.GaussianBlur(original_img, (5, 5), 0)
    #将彩色图转化成灰度图
    img_gray = cv2.cvtColor(blur,cv2.COLOR_BGR2GRAY)
    #图片开（opening）处理，用来降噪，使图片中的字符边界更圆滑，没有皱褶
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(img_gray, cv2.MORPH_OPEN, kernel)

    kernel2 = np.ones((3,3), np.uint8)
    opening = cv2.dilate(opening, kernel2, iterations=1)
    # Otsu's thresholding after Gaussian filtering
    # 采用otsu阈值法将灰度图转化成只有0和1的二值图
    blur = cv2.GaussianBlur(opening,(13,13),0)
    #ret, binary_img = cv2.threshold(img_gray, 120, 1, cv2.THRESH_BINARY_INV)
    ret,binary_img = cv2.threshold(blur,0,1,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    return original_img,binary_img

# 从img截取location区域的图像，并归一化成IMG_SIZE*IMG_SIZE
def extract_img(location,img,contour=None):
    x,y,w,h=location
    # 只提取轮廓内的字符
    if contour is None:
        extracted_img = img[y:y + h, x:x + w]
    else:
        mask = np.zeros(img.shape, np.uint8)
        cv2.drawContours(mask, [contour], -1, 255, cv2.FILLED)
        img_after_masked = cv2.bitwise_and(mask, img)
        extracted_img = img_after_masked[y:y + h, x:x + w]
    # 将提取出的img归一化成IMG_SIZE*IMG_SIZE大小的二值图
    black = np.zeros((IMG_SIZE, IMG_SIZE), np.uint8)
    if (w > h):
        res = cv2.resize(extracted_img, (IMG_SIZE, (int)(h * IMG_SIZE / w)), interpolation=cv2.INTER_AREA)
        d = int(abs(res.shape[0] - res.shape[1]) / 2)
        black[d:res.shape[0] + d, 0:res.shape[1]] = res
    else:
        res = cv2.resize(extracted_img, ((int)(w * IMG_SIZE / h), IMG_SIZE), interpolation=cv2.INTER_AREA)
        d = int(abs(res.shape[0] - res.shape[1]) / 2)
        black[0:res.shape[0], d:res.shape[1] + d] = res
    extracted_img = skeletonize(black)
    extracted_img = np.logical_not(extracted_img)
    return extracted_img

#将二值图里面的字符切割成单个字符，返回三维数组，每一个元素是一个字典，包含字符所在位置大小location，以及字符切割图src_img
def binary_img_segment(binary_img,original_img=None):
    # binary_img = skeletonize(binary_img)
    # plot.imshow( binary_img,cmap = 'gray', interpolation = 'bicubic')
    # plot.show()
    #寻找每一个字符的轮廓，使用cv2.RETR_EXTERNAL模式，表示只需要每一个字符最外面的轮廓
    img, contours, hierarchy = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)#cv2.RETR_TREE
    #cv2.drawContours(img_original, contours, -1, (0, 255, 0), 2)
    if len(contours) > LARGEST_NUMBER_OF_SYMBOLS:
        raise ValueError('symtem cannot interpret this image!')
    symbol_segment_location = []
    # 将每一个联通体，作为一个字符
    symbol_segment_list = []
    index = 1
    for contour in contours:
        location = cv2.boundingRect(contour)
        x, y, w, h = location
        if(w*h<100):
            continue
        symbol_segment_location.append(location)
        # 只提取轮廓内的字符
        extracted_img = extract_img(location,img,contour)
        symbol_segment_list.append(extracted_img)
        if len(original_img):
            cv2.rectangle(original_img, (x, y), (x + w, y + h), (0, 0, 255), 3)
        symbols=[]
        for i in range(len(symbol_segment_location)):
            symbols.append({'location':symbol_segment_location[i],'src_img':symbol_segment_list[i]})
        # 对字符按字符横坐标排序
        symbols.sort(key=lambda x:x['location'][0])
    return symbols


