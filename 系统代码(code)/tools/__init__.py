from config import IMG_SIZE
import numpy as np
from config import SPACIAL_RELATIONSHIP as spatial_relationship,NUM_OF_CANDIDATES,FILELIST,UNCONTINOUS_SYMBOLS
from tools.img_preprocess import extract_img
from tools.cnn_model import cnn_symbol_classifier
from config import *
# 将输入的矩阵值转化成数据集图片那样的二值矩阵,即是将布尔型元素转化成只有0或者255的float型矩阵
# notes：数据集图片中是灰度图，并非二值图，可以考虑将数据集图片转化为二值图
def normalize_matrix_value(symbol_segment_list):
    symbols_to_be_predicted = []
    for i in range(len(symbol_segment_list)):
        one = symbol_segment_list[i].reshape(IMG_SIZE * IMG_SIZE)
        t = np.ones((IMG_SIZE * IMG_SIZE), np.uint8)
        for j in range(IMG_SIZE * IMG_SIZE):
            if one[j] == True:
                t[j] = 255
            else:
                t[j] = 0
        symbols_to_be_predicted.append(np.array(t, np.float32))
    return np.array(symbols_to_be_predicted,np.float32)

# 计算重合率
def get_overlap_ratio(rect1,rect2):
    larger_one = 1
    # 确保rect1是面积比较大的那个
    if(rect2[2]*rect2[3]>rect1[2]*rect1[3]):
        larger_one = 2
        t = rect1
        rect1 = rect2
        rect2 = t
    x11, y11, w1, h1 = rect1
    x21, y21, w2, h2 = rect2
    x12, y12 = x11 + w1, y11 + h1
    x22, y22 = x21 + w2, y21 + h2
    S1 = w1*h1
    S2 = w2*h2
    # print(x11,x12,y11,y12)
    # print(x21, x22, y21, y22)
    # 如果是包含，ratio = 1
    if (x11 <= x21 and y11 <= y21 and x12 >= x22 and y12 >= y22):
        return 1,larger_one
    # 如果相交，ratio = （S大-S小）/ S小
    elif x11<=x21 and y11 <= y21 and x12> x21 and y12 > y21 and x22 < x12 and y22 > y12:
        overlap_area = (x12-x21)*(y12-y21)
        return (overlap_area)/S2,larger_one
    else:
        return 0,larger_one
    # p1x = max(x11, x21);
    # p1y = max(y11, y21);
    #
    # p2x = min(x12,x22);
    # p2y = min(y12,y22);
    # overlap_area = 0
    # #  判断是否相交
    # if (p2x > p1x and p2y > p1y):
    #         # // 如果先交，求出相交面积
    #     overlap_area = (p2x - p1x) * (p2y - p1y)
    # if overlap_area>0:
    #     return overlap_area/float(S2),larger_one
    # else:
    #     return 0,larger_one
# 获取两个矩形之间的空间关系（具体空间关系参见tools/config.py），矩形用(x,y,w,h)表示，其中x,y是坐标，w,h是宽高
# 返回rect2对rect1的关系 比如including表示rect1包含rect2 included则表示rect2包含rect1
def get_spatial_relationship(rect1,rect2):
    x11,y11,w1,h1 = rect1
    x21,y21,w2,h2 = rect2
    x12,y12 = x11+w1,y11+h1
    x22,y22 = x21+w2,y21+h2
    overlap_ratio,larger_one = get_overlap_ratio(rect1,rect2)
    # print(overlap_ratio)
    # 包含关系判定
    if(overlap_ratio > 0.5 and larger_one == 1):
        return spatial_relationship['including']
    # 被包含关系判定
    elif(overlap_ratio > 0.5 and larger_one == 2):
        return spatial_relationship['included']
    elif overlap_ratio == 0:
        # 判断其他空间关系
        cx1,cy1 = (x11+x12)/2,(y11+y12)/2
        cx2,cy2 = (x21+x22)/2,(y21+y22)/2
        if(cx2==cx1):
            if(cy1>cy2):
                return spatial_relationship['up']
            else:
                return spatial_relationship['down']
        else:
            # 计算空间位置关系特征值
            # 中心点角度angle、高度比HR，两个字符之间的相对水平距离比DR
            angle = np.degrees(np.arctan((cy1-cy2)/(cx2-cx1)))
            HR = h2/h1
            WR = w2/w1
            w = max(w1,w2)
            w = max(w,max(h1,h2))
            DR1 = (x21-x12)/w
            DR2 = (x21-x12)/w2
            # print('relationship feature:',angle,HR,DR1,DR2,cx1,cx2,cy1,cy2)
            if angle > -18 and angle < 18 and (cx2 > cx1):
                return spatial_relationship['right']
            elif angle >=18 and angle <= 75 and HR <=1.2 and DR1 <= 2:
                return spatial_relationship['superscript']
            elif angle <= -18 and angle >= -75 and HR <= 0.7 and cx1<cx2 and cy1 < cy2:
                return spatial_relationship['subscript']
            elif (angle >75 and angle <= 90 or angle <-75 and angle >=-90) and WR > 0.4 and cy1 < cy2:
                return spatial_relationship['up']
            elif (angle >75 and angle <=90 or angle <-75 and angle >= -90) and WR > 0.4 and cy2 < cy1:
                return spatial_relationship['down']
            elif angle > -15 and angle <15 and DR2 <=2 and DR2 >=0 :
                return spatial_relationship['left']
            elif angle <= -15 and angle >=-75 and cx1 > cx2:
                if(cy1 > cy2):
                    return spatial_relationship['left_up']
                else:
                    return spatial_relationship['left_down']
    return spatial_relationship['unknown']

# 判断某一个矩形是否跟矩形列表的某一个矩形构成特定的关系
def verify_spatial_relationship(rect,rects,specified_relationship):
    for rect1 in rects:
        relationship = get_spatial_relationship(rect,rect1)
        if (relationship in specified_relationship):
            return True
    return False

# 从cnn分类器返回的结果中返回前n个概率最大的字符
def get_candidates(estimated_probabilities):
    indexes_of_top_n_largest_probability = np.argsort(-estimated_probabilities)[:NUM_OF_CANDIDATES]
    candidates = []
    for i in range(NUM_OF_CANDIDATES):
        index = indexes_of_top_n_largest_probability[i]
        candidates.append({'symbol':FILELIST[index],'probability':estimated_probabilities[index]})
    return candidates

# 获取投影 projection_type = 0|竖直投影 1|水平投影
def get_projection(characters,projection_type):
    locations = [x['location'] for x in characters]
    i = projection_type
    projection = [[locations[0][i], locations[0][i] + locations[0][i + 2]]]
    for location in locations:
        # print(location)
        start = location[i]
        end = location[i] + location[i + 2]
        line_segment1 = [start, end]
        line_segment2 = projection[-1]
        # 思路跟空闲盘块的回收类似
        # print(line_segment1,line_segment2)
        # 判定线段（start，end）与线段e的关系
        # 对不同线段之间的关系，有不同的处理
        # 如果是包含
        # print(line_segment1,line_segment2)
        if (line_segment1[0] >= line_segment2[0] and line_segment2[1] >= line_segment1[1]):
            continue
        elif (line_segment2[0] >= line_segment1[0] and line_segment1[1] >= line_segment2[1]):
            projection[-1][0] = line_segment1[0]
            projection[-1][1] = line_segment1[1]
        # 如果是相交
        elif line_segment1[0] >= line_segment2[0] and line_segment1[0] <= line_segment2[1] and line_segment1[1] >= \
                line_segment2[1]:
            line_segment2[1] = line_segment1[1]
            projection[-1][1] = line_segment1[1]
        elif line_segment2[0] >= line_segment1[0] and  line_segment2[0] <= line_segment1[1] and line_segment2[1] >= \
            line_segment1[1]:
            line_segment2[0] = line_segment1[0]
            projection[-1][0] = line_segment1[0]
        # 如果与e1和e2相离
        elif line_segment1[0] >= line_segment2[1]:
            projection.append(line_segment1)
        else:
            raise ValueError('sort_character:logic error')
    # print('投影结果：', projection)
    return projection
# 采用自顶向下分析方法，将识别出的字符按人们的书写习惯，即从上到下，从左到右的方式排列
# 主要方法是递归调用基准线+投影法对字符序列进行划分
def sort_characters(characters,i=0):
    if(len(characters)<=1):
        return characters
    # 先竖直投影，寻找竖直切割点
    # 然后水平投影，寻找水平切割点

    # if i==0:
    #     print('竖直投影')
    # else:
    #     print('水平投影')
    # 先对characters按x/y值进行预排序
    presort_characters = sorted(characters,key=lambda x:x['location'][i])
    # print('sort 方法调用的排序算法：')
    # print(presort_characters)
    pre_locations = [x['location'] for x in presort_characters]
    # print('待排序的location')
    # for location in locations:
    #     print('(',location[i],',',location[i]+location[i+2],')','||',end='')
    # print()
    projection = get_projection(presort_characters,i)
    # 如果存在分割点，则分割
    if(len(projection)>1):
        # 如果能够分割，才对字符进行真正排序
        characters.sort(key=lambda x: x['location'][i])
        locations = [x['location'] for x in characters]
        start_index = 0
        end_index = 0
        # 对于每一个分割，获得在这个分割里面的characters
        for line_segment in projection:
            # 确定属于line_segment的characters
            start_index = end_index
            for end_index in range(start_index,len(locations)):
                x11,x12 = locations[end_index][i],locations[end_index][i]+locations[end_index][i+2]
                x21,x22 = line_segment[0],line_segment[1]
                if(x11>=x21 and x12<=x22):
                    end_index += 1
                else:
                    break
            # 截取characters[start_index:end_index],如果长度大于1，继续递归调用sort_characters排序
            location_segment = locations[start_index:end_index]
            character_segment = characters[start_index:end_index]
            # print('切割后的location',location_segment)
            if(len(location_segment)>1):
                projection_type = (i+1)%2
                sorted_character_segment = sort_characters(character_segment,projection_type)
                characters[start_index:end_index] = sorted_character_segment
    # 如果找不到竖直或者水平切割点，则返回排好序的字符序列
    # 处理立方根
    length = len(characters)
    for i in range(length):
        character = characters[i]
        # if i+1 <length:
            # print('modify 1',get_spatial_relationship(character['location'], characters[i + 1]['location']) == \
            #     SPACIAL_RELATIONSHIP['left_up'])
        if i + 1 < length and get_spatial_relationship(character['location'], characters[i + 1]['location']) == \
                SPACIAL_RELATIONSHIP['left_up']:
            t = character
            characters[i] = characters[i + 1]
            characters[i + 1] = t
            i = i + 1
            # print('sqrt modify',node_list)
    return characters

# 添加经验规则
# 1.若右括号数为0，'）'识别为1
# 2.若乘号右边仍是操作符或者为最后一个token，识别为x
def modify_characters(characters):
    length = len(characters)
    left_bracket = 0
    for i in range(length):
        c = characters[i]['candidates'][0]['symbol']
        # print('(((((((((((((',c,left_bracket)
        # print(left_bracket)
        # if c == '(':
        #     j = i+1
        #     # 如果（后续无），则匹配成1
        #     while j<length and characters[j]['candidates'][0]['symbol']!=')':
        #         j = j+1
        #     if j<length:
        #         left_bracket = left_bracket + 1
        #     else:
        #         characters[i]['candidates'][0]['symbol'] = '1'
        # if c == ')':
        #     # print(')))))))))))))',left_bracket)
        #     if left_bracket == 0:
        #         characters[i]['candidates'][0]['symbol'] = '1'
        #     else:
        #         left_bracket = left_bracket - 1
        if c == 'times' and (i == length-1 or\
             characters[i+1]['candidates'][0]['symbol'] in OPERATOR \
            or characters[i+1]['candidates'][0]['symbol'] in CMP):
            characters[i]['candidates'][0]['symbol'] = 'x'
        if c == 'times' and i>0 and not(characters[i-1]['candidates'][0]['symbol'] in OPERATABLE):
            characters[i]['candidates'][0]['symbol'] = 'x'
        if c == 'times' and i+1 <length and characters[i + 1]['candidates'][0]['symbol'] == 'd':
            characters[i]['candidates'][0]['symbol'] = 'x'
        if c == 'times' and i+1 <length and characters[i + 1]['candidates'][0]['symbol'].isdigit() and\
                get_spatial_relationship(characters[i]['location'],characters[i+1]['location'])==SPACIAL_RELATIONSHIP['superscript']:
            characters[i]['candidates'][0]['symbol'] = 'x'

        # if c == 'x' and isinstance(int(characters[i+1]['candidates'][0]['symbol']),int):
        #     characters[i]['candidates'][0]['symbol'] = 'times'
        if c == 'pi' and i>0 and characters[i-1]['candidates'][0]['symbol'] == 'lim':
            characters[i]['candidates'][0]['symbol'] = 'x'
        if c ==',' and i>0 and get_spatial_relationship(characters[i-1]['location'],characters[i]['location'])\
                == SPACIAL_RELATIONSHIP['superscript'] and (characters[i-1]['candidates'][0]['symbol'] in [')','x'] or \
                                                            characters[i - 1]['candidates'][0]['symbol'].isdigit()) :
            pass
        elif c == ',':
            characters[i]['candidates'][0]['symbol'] = '1'
        if c == 'd' and i+1<length and characters[i+1]['candidates'][0]['symbol'] == 'pi':
            characters[i + 1]['candidates'][0]['symbol'] = 'x'
        #  默认lim后面跟着x
        if c == 'lim' and i+1<length and characters[i+1]['candidates'][0]['symbol'] != 'x':
            characters[i + 1]['candidates'][0]['symbol'] = 'x'
        # if c == '1' and i>0 and get_spatial_relationship(characters[i-1]['location'],characters[i]['location'])\
        #         == SPACIAL_RELATIONSHIP['superscript']:
        #     characters[i ]['candidates'][0]['symbol'] = ','

# 合并多个矩形，返回一个大矩形
def join_locations(locations):
    boundarys = [[x[0],x[1],x[0]+x[2],x[1]+x[3]] for x in locations]
    # print(boundarys)
    minx,miny,maxx,maxy = np.infty,np.infty,0,0
    for boundary in boundarys:
        # print(boundary,[minx,miny,maxx,maxy])
        if(boundary[0]<minx):
            minx=boundary[0]
        if (boundary[1] < miny):
            miny = boundary[1]
        if (boundary[2] > maxx):
            maxx = boundary[2]
        if (boundary[3] > maxy):
            maxy = boundary[3]
    return [minx,miny,maxx-minx,maxy-miny]

# 生成一个location1 到 location2中间的location,默认两个location不相交
def get_location_between(location1,location2):
    height = min(location1[3],location2[3])
    weight = location2[0]-location1[0]-location1[2]-2
    x = location1[0]+location1[2]+1
    y = location1[1]
    return [x,y,weight,height]

# 通过value获取字典的key
def get_keys(d, value):
    return [k for k,v in d.items() if v == value]

# 打印解析树，先序遍历parser_tree,如果是叶子节点，即打印
def print_parser_tree(node,latex_str):
    if isinstance(node,dict) and len(node) and isinstance(node['structure'],list):
        for child in node['structure']:
            latex_str = print_parser_tree(child,latex_str)
    elif isinstance(node,dict) and len(node):
        print(node['structure'],end='')
        latex_str = latex_str + str(node['structure'])

    else:
        if node == 'div':
            print('/',end = '')
            latex_str = latex_str + "\\div"
        elif node == 'times':
            print('*',end='')
            latex_str = latex_str + "\\times"
        else:
            print(node,end='')
            latex_str = latex_str + node
    return latex_str


# 定义从解到输出结果的格式
def result_to_str(result):
    result_str = ''
    if len(result)==1:
        result_str = 'x='+str(result[0])
        return result_str
    for i in range(len(result)-1):
        x = result[i]
        result_str = result_str + 'x'+str(i+1)+'=' + str(x) + ','
    result_str = result_str + 'x'+str(len(result))+'=' + str(result[len(result)-1])
    return result_str