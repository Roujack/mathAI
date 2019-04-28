# 此文件和test.py文件类似，不过可以看到更详细中间输出结果，可以用来调试


from tools.image_input import read_img_file
import tensorflow as tf
from tools.cnn_model import cnn_model_fn
from tools.cnn_model import cnn_symbol_classifier
from tools import normalize_matrix_value,get_spatial_relationship,\
    verify_spatial_relationship,get_candidates,sort_characters
import process
from config import FILELIST
import numpy as np
from matplotlib import pyplot as plt
from tools.img_preprocess import read_img_and_convert_to_binary,binary_img_segment
import cv2
import parser
import tools
from calculator import *


#test
original_img, binary_img = read_img_and_convert_to_binary('./testImgs/easy +/3.jpg')

symbols = binary_img_segment(binary_img,original_img)
symbols = process.detect_uncontinous_symbols(symbols,binary_img)
length = len(symbols)
column = length/3+1
index = 1
for symbol in symbols:
    # print(symbol)
    plt.subplot(column,3,index)
    plt.imshow(symbol['src_img'], cmap='gray')
    plt.title(index), plt.xticks([]), plt.yticks([])
    index += 1
temp_img = original_img[:, :, ::-1]
# cv2.imshow('img',temp_img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
plt.subplot(column,3,index)
plt.imshow(temp_img, cmap = 'gray', interpolation = 'bicubic')
plt.title(index),plt.xticks([]), plt.yticks([])
plt.show()

symbols_to_be_predicted = normalize_matrix_value([x['src_img'] for x in symbols])

predict_input_fn = tf.estimator.inputs.numpy_input_fn(
    x={"x": np.array(symbols_to_be_predicted)},
    shuffle=False)

predictions = cnn_symbol_classifier.predict(input_fn=predict_input_fn)

characters = []
for i,p in enumerate(predictions):
    # print(p['classes'],FILELIST[p['classes']])
    candidates = get_candidates(p['probabilities'])
    characters.append({'location':symbols[i]['location'],'candidates':candidates})
#print([x['location'] for x in characters])

sorted_characters = sort_characters(characters)
# print('排序前的字符列表')
# print(characters)
# print('排序后的字符序列')
# print([[x['location'],x['candidates']] for x in sorted_characters])
tokens = process.group_into_tokens(sorted_characters)
print('识别出的token')
print(tokens)
# 先将每一个token初始化成一个树节点，得到一个节点列表node_list
node_list = parser.characters_to_nodes(sorted_characters)

parser_tree = parser.decompose(node_list)
print(parser_tree)
latex_str = post_order(parser_tree)
print(latex_str)
print(parser_tree['value'])
# parser_tree = parser.parser(sorted_characters)
# for i in range(10):
#     print()
# print('识别的表达式：')
# latex_str = tools.print_parser_tree(parser_tree,"")
# print()
# value = calculate(parser_tree)
# print('计算结果：',value)
#
# print('转化成的latex语句:')
#
expression_str = r'$result:'+latex_str+'='+latex(parser_tree['value'])+'$'
print(expression_str)
import os
if not os.path.exists('./result'):
    os.mkdir('./result')
plt.text(0.1,0.9,expression_str,fontsize=20)

plt.xticks([]),plt.yticks([])
plt.savefig('./result/1.jpg')
plt.close()



