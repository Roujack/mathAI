#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a module to read image for trainning, evaluation and prediction '

__author__ = 'Ajay'


import os
import cv2
import numpy as np
from config import *
# FILELIST = ['infty', 'rightarrow', 'div', 'times', 'point',
#              'sin', '9', '0', '7', '+', ',', '6', '1', '8',
#              'cos', '-', 'sqrt', 'pi', 'int', 'lim', 'log',
#              '(', 'd', '=', '4', 'x', '3', 'tan', 'e', ')',
#              '2', '5']
def read_img_file(type):
    fileList1 = [x for x in os.listdir(RELEVANT_URL) if x in SYMBOLS]
    # print(fileList1)
    num_of_symbol = len(fileList1)
    # print('num of symbol:',num_of_symbol)
    distribute_table = []
    train_total = 0
    eval_total = 0
    for j in range(num_of_symbol):
        characterPath = os.path.join(RELEVANT_URL, fileList1[j])
        fileList2 = [x for x in os.listdir(characterPath) if x.split('.')[-1] == 'jpg']
        # print(fileList2)
        length = len(fileList2)
        if length >= NUMBER_OF_PICTURES:
            distribute = {'num_of_train': int(TRAININT_RATIO * NUMBER_OF_PICTURES),
                          'num_of_eval': int(EVAL_RATIO * NUMBER_OF_PICTURES),
                          'start_train':int(train_total),
                          'start_eval':int(eval_total)}
            train_total = train_total + int(TRAININT_RATIO * NUMBER_OF_PICTURES)
            eval_total = eval_total + int(EVAL_RATIO * NUMBER_OF_PICTURES)
        else:
            distribute = {'num_of_train': int(TRAININT_RATIO * length),
                          'num_of_eval': int(EVAL_RATIO * length),
                          'start_train': int(train_total),
                          'start_eval': int(eval_total)
                          }
            train_total = train_total + int(TRAININT_RATIO * length)
            eval_total = eval_total + int(EVAL_RATIO * length)
        distribute_table.append(distribute)
    # for i in range(num_of_symbol):
    #     print(i,distribute_table[i])
    # print(train_total,eval_total)
    if type == 'train':
        images = np.ndarray((train_total , PICTURE_SIZE * PICTURE_SIZE), np.float32)
        images_label = np.ndarray(train_total, np.int32)
    else:
        images = np.ndarray((eval_total , PICTURE_SIZE * PICTURE_SIZE), np.float32)
        images_label = np.ndarray(eval_total , np.int32)

    for j in range(num_of_symbol):
        characterPath = os.path.join(RELEVANT_URL, fileList1[j])
        fileList2 = [x for x in os.listdir(characterPath) if x.split('.')[-1] == 'jpg']
        if type == 'train':
            for i in range(distribute_table[j]['num_of_train']):
                # print(j,distribute_table[j]['start_train'])
                # print(os.path.join(characterPath, fileList2[i]))
                img = cv2.imread(os.path.join(characterPath, fileList2[i]), 0)
                images[distribute_table[j]['start_train'] + i] = img.reshape(img.shape[0] * img.shape[1])
                images_label[distribute_table[j]['start_train'] + i] = j
        elif type == 'eval':
            for i in range(distribute_table[j]['num_of_eval']):
                # # print(j, distribute_table[j]['start_eval'])
                s = os.path.join(characterPath, fileList2[i+distribute_table[j]['num_of_train']])
                if s.split('.')[-1] != 'jpg':
                    print(s)
                img = cv2.imread(os.path.join(characterPath, fileList2[i +distribute_table[j]['num_of_train']]), 0)
                images[distribute_table[j]['start_eval'] + i] = img.reshape(img.shape[0] * img.shape[1])
                images_label[distribute_table[j]['start_eval'] + i] = j
        else:
            raise ValueError('type must be one of those value:train or eval')
    return images, images_label

# def read_img_file(type):
#   fileList1 = [x for x in os.listdir(RELEVANT_URL) if x in SYMBOLS]
#   print(fileList1)
#   num_of_symbol = len(fileList1)
#   images = np.ndarray((NUMBER_OF_PICTURES * num_of_symbol, PICTURE_SIZE * PICTURE_SIZE), np.float32)
#   images_label = np.ndarray(NUMBER_OF_PICTURES * num_of_symbol, np.int32)
#
#   for j in range(num_of_symbol):
#       characterPath = os.path.join(RELEVANT_URL, fileList1[j])
#       fileList2 = [x for x in os.listdir(characterPath)]
#       for i in range(NUMBER_OF_PICTURES):
#           if type == 'train':
#               img = cv2.imread(os.path.join(characterPath, fileList2[i]), 0)
#           elif type == 'eval':
#               img = cv2.imread(os.path.join(characterPath, fileList2[i+NUMBER_OF_PICTURES]), 0)
#           elif type == 'predict':
#               img = cv2.imread(os.path.join(characterPath, fileList2[i + NUMBER_OF_PICTURES+NUMBER_OF_PICTURES]), 0)
#           else:
#               raise ValueError('type must be one of those value:train eval predict')
#           images[j * NUMBER_OF_PICTURES + i] = img.reshape(img.shape[0] * img.shape[1])
#           if(type == 'train' or type == 'eval'):
#             images_label[j * NUMBER_OF_PICTURES + i] = j
#   return images,images_label,fileList1
#
#
