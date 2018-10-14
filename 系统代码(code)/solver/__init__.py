from tools.image_input import read_img_file
import tensorflow as tf
from tools.cnn_model import cnn_model_fn
from tools.cnn_model import cnn_symbol_classifier
from tools import *
import process
from config import FILELIST
import numpy as np
from matplotlib import pyplot as plt
from tools.img_preprocess import read_img_and_convert_to_binary,binary_img_segment
import cv2
import parser
import tools
from calculator import *
import time


# 程序入口,输入一张图片，输出一张图片
def solve(filename,mode = 'product'):
    original_img, binary_img = read_img_and_convert_to_binary(filename)
    symbols = binary_img_segment(binary_img, original_img)
    sort_symbols = sort_characters(symbols)
    process.detect_uncontinous_symbols(sort_symbols, binary_img)
    length = len(symbols)
    column = length/3+1
    index = 1
    # for symbol in symbols:
    #     # print(symbol)
    #     plt.subplot(column,3,index)
    #     plt.imshow(symbol['src_img'], cmap='gray')
    #     plt.title(index), plt.xticks([]), plt.yticks([])
    #     index += 1
    # temp_img = original_img[:, :, ::-1]
    # # cv2.imshow('img',temp_img)
    # # cv2.waitKey(0)
    # # cv2.destroyAllWindows()
    # plt.subplot(column,3,index)
    # plt.imshow(temp_img, cmap = 'gray', interpolation = 'bicubic')
    # plt.title(index),plt.xticks([]), plt.yticks([])
    # plt.show()

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

    modify_characters(characters)

    # print('排序后的字符序列')
    # print([[x['location'], x['candidates']] for x in characters])
    tokens = process.group_into_tokens(characters)
    # print('识别出的token')
    # print(tokens)
    # 先将每一个token初始化成一个树节点，得到一个节点列表node_list
    node_list = parser.characters_to_nodes(characters)

    parser_tree = parser.decompose(node_list)
    # print(parser_tree)
    set_forward_step(0)
    post_order(parser_tree)
    y_start = 0.9
    y_stride = 0.2
    if parser_tree['status'] == STATUS['solved']:
        latex_strs = []
        i = 5
        j = 0

        while j < i and isinstance(parser_tree['structure'], list):
            set_forward_step(1)
            latex_str = post_order(parser_tree)
            latex_strs.append(latex_str)
            j = j + 1
        # for latex_str in latex_strs:
        #     print(latex_str)
        # print(parser_tree)

        for i, latex_str in enumerate(latex_strs):
            if i == 0:
                expression_str = r'$expression:' + latex_str + '$'
            else:
                expression_str = r'$step' + str(i) + ':' + latex_str + '$'
            # print(expression_str)
            font_size = 18
            if len(latex_str) > 12:
                font_size = 15
            plt.text(0.1, y_start, expression_str, fontsize=font_size)
            y_start = y_start - y_stride
        latex_str = latex_strs[0]
    else:
        set_forward_step(0)
        latex_str = post_order(parser_tree)
        expression_str = r'$expression:' + latex_str + '$'
        font_size = 18
        if len(latex_str) > 12:
            font_size=15
        plt.text(0.1, y_start, expression_str, fontsize=font_size)
        y_start = y_start - y_stride

    # print(solve_expression(parser_tree))
    solution = ''
    answer=''
    if parser_tree['status'] == STATUS['solved']:
        # print(latex(parser_tree['value']))
        if isinstance(parser_tree['value'], int) or isinstance(parser_tree['value'], float):
            solution = r'$result:' + str(parser_tree['value']) + '$'
            answer = str(parser_tree['value'])
        else:
            solution = r'$result:' + str(latex(parser_tree['value'])) + '$'
            answer = str(latex(parser_tree['value']))
    elif parser_tree['type'] == NODE_TYPE['derivation'] or parser_tree['type'] == NODE_TYPE['limitation']:
        solution = r'$result:' + str(latex(parser_tree['value'])) + '$'
        answer = str(latex(parser_tree['value']))
    elif parser_tree['status'] == STATUS['eq1'] or parser_tree['status'] == STATUS['eq2']:

        result = solve_expression(parser_tree)
        # print(result)
        solution = r'$result:' + result_to_str(result) + '$'
        answer = result
    elif parser_tree['status'] == STATUS['other']:
        answer = latex(parser_tree['value'])
        # print(answer)
    else:
        result = solve_expression(parser_tree)
        # print(str(result))
        solution = r'$solution:' + latex_str + '$'
    print('答案：',solution)
    print('处理结果请到static文件夹下的最新生成的图片查看')
    plt.text(0.1, y_start, solution, fontsize=18)

    #
    # expression_str = r'$expression:' + latex_str + '$'
    # print(expression_str)
    # plt.text(0.1, 0.9, expression_str, fontsize=20)
    # # print(solve_expression(parser_tree))
    # solution = ''
    # answer =''
    # if parser_tree['status'] == STATUS['solved']:
    #     if isinstance(parser_tree['value'], int) or isinstance(parser_tree['value'], float):
    #         solution = r'$result:' + str(parser_tree['value']) + '$'
    #         answer = str(parser_tree['value'])
    #     else:
    #         solution = r'$result:' + str(latex(parser_tree['value'])) + '$'
    #         answer = str(latex(parser_tree['value']))
    #
    #
    # elif parser_tree['status'] == STATUS['eq1'] or parser_tree['status'] == STATUS['eq2']:
    #     solution = r'$result:' + str(latex(parser_tree['value'])) + '$'
    #     result = solve_expression(parser_tree)
    #     print(result)
    #     answer = result
    # elif parser_tree['status'] == STATUS['other']:
    #     answer = latex(parser_tree['value'])
    #     print(answer)
    # else:
    #     solution = r'$solution:' + latex_str + '$'
    #     answer = latex_str
    # plt.text(0.1, 0.5, solution, fontsize=20)



    plt.xticks([]),plt.yticks([])
    # print(filename.rsplit('.',1)[1])
    save_filename = str(int(time.time()))
    save_filename_dir = SAVE_FOLDER+save_filename
    plt.savefig(save_filename_dir)
    # plt.show()
    plt.close()
    if mode == 'product':
        return save_filename
    elif mode == 'test':
        return latex_str,answer



