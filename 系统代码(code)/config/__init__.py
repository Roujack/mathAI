#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'下面是系统的一些配置参数'
'some system configuration will be defined as below'

__author__ = 'Ajay'

# 上传的文件夹路径
UPLOAD_FOLDER = './static/'
# 存放结果的文件夹路径
SAVE_FOLDER = './static/'

RELEVANT_URL = './dataset1'

MODEL_DIR = "./my_cnn_model_config5"

NUMBER_OF_PICTURES = 400

TRAINING_STEPS = 4000

PICTURE_SIZE = 45
IMG_SIZE = 45

TRAININT_RATIO = 0.6
EVAL_RATIO = 0.4
# this is all the symbol or function name in the CHROME dataset
# ['beta', 'pm, 'Delta', 'gamma', 'infty', 'rightarrow', '.DS_Store', 'div',
#  'gt', 'forward_slash', 'leq', 'mu', 'exists', 'in', 'times', 'point', 'sin',
#  'R', 'u', '9', '0', '{', '7', 'i', 'n', 'G', '+', ',', '6', 'z', '}', '1',
#  '8', 'T', 's', 'cos', 'a', '-', 'f', 'o', 'H', 'sigma', 'sqrt', 'pi', 'int',
#  'sum', 'lim', 'lambda', 'neq', 'log', 'ldots', 'forall', 'lt', 'theta', 'ascii_124',
#  'M', '!', 'alpha', 'j', 'c', ']', '(', 'd', 'v', 'prime', 'q', '=', '4', 'x', 'phi',
#  '3', 'tan', 'e', ')', '[', 'b', 'k', 'l', 'geq', '2', 'y', '5', 'p', 'w']

# frac是分数的符号，并不存在与数据集中，当识别的'-'是分数符号时，会自动转化成'frac'
SYMBOLS = ['0','1','2','3','4','5','6','7','8','9',',',
            '-','+','times','div','=','int','d','infty',
            'cos','x','sin','log','e','lim','rightarrow',
            'pi','(',')','point','sqrt','tan']
# SYMBOLS = ['0','1','2','3','4','5','6','7','8','9',
#             '-','+','times','div','=','int','a','b',
#             'c','x','y','z','s','i','n','l','o','e',
#             'pi','(',')','point','frac','sin','cos','log']
FILELIST = ['infty', 'rightarrow', 'div', 'times', 'point',
             'sin', '9', '0', '7', '+', ',', '6', '1', '8',
             'cos', '-', 'sqrt', 'pi', 'int', 'lim', 'log',
             '(', 'd', '=', '4', 'x', '3', 'tan', 'e', ')',
             '2', '5']
# FILELIST = ['div', 'times', 'point', '9', '0', '7',
#             'i', 'n', '+', '6', 'z', '1', '8', 's',
#             'a', '-', 'o', 'pi', 'int', 'c', '(',
#             '=', '4', 'x', '3', 'e', ')', 'b', 'l',
#             '2', 'y', '5','frac']

# 定义非黏连字符
UNCONTINOUS_SYMBOLS = ['div','=','rightarrow'] #,'sin','cos','tan','lim','ln','log']





# 定义空间关系
SPACIAL_RELATIONSHIP = {'including':0,'included':1,'unknown':2,
                        'superscript':3,'subscript':4,'up':5,
                        'down':6,'right':7,'left':8,'left_up':9,'left_down':10}

# 一个数学计算式能够包含的最多字符个数
LARGEST_NUMBER_OF_SYMBOLS = 50

# 原图缩放比例
SCALSIZE = 1

# 候选字符个数
NUM_OF_CANDIDATES = 1

# 定义token类型
TOKEN_TYPE = {'OPERATOR':0,'CONSTANT_INTEGER':1,'CONSTANT_DECIMAL':2,'FUNCTION':3,'VARIABLE':4,'CMP':5,'RESERVE':6,'ERROR':7,'END':8,'SPECIAL':9}
OPERATOR = ['+','-','times','div','sqrt']
DIGIT = ['0','1','2','3','4','5','6','7','8','9']
SPECIAL = ['(',')','d',',','rightarrow']
VARIABLE = ['x','y','z']
RESERVE = ['e','pi','infty']
FUNCTION = ['cos','sin','log','tan','lim']
CIRCULAR_FUNCTIONS = ['cos','sin','tan']
DECIMAL_POINT = ['point','1'] # 跟小数点很像的字符
CMP = ['=','<','>','le','ge']

# 定义DFA状态
DFA_STATE = {'START':0,'INCONSTANT':2,'INDECIMAL':3,'INRESERVE':4,'INVARIABLE':5,'INFUNCTION':6,'DONE':7}

# 定义解析树节点类型
NODE_TYPE = {'default':0,'bracket':1,'integer':2,'decimal':3,'variable':4,'t_pi':5,
             't':6,'e_pi':7,'e':8,'me':9,'me_pi':10,'fraction':11,'int':12,'power':13,
             'equation':14,'operator':15,'function':16,'empty':17,'f':18,'sqrt':19,'constant':20,'derivation':21,'limitation':22}
# 可以乘方的节点类型
POWERABLE = [2,3,4,20]

# 可以作为操作数的字符
OPERATABLE = ['0','1','2','3','4','5','6','7','8','9','x']

# 定义节点类型和token类型的定义关系，用于生成node list
TOKEN_TO_NODE = {0:15,1:2,2:3,3:16,4:4,5:0,6:20,7:0,8:0,9:0}

# 定义表达式类型
OP_TYPE = {'power':0,'int':1,'fraction':2,'equation':3,'normal':4,'sqrt':5,'function':6}

# 定义节点状态
# solved|当前的节点值是可计算的 poly1|当前节点是一个一元一次多项式 poly2|当前节点是一个一元二次多项式
# eq1|当前节点是一元一次方程 eq2|当前节点是一元二次方程
STATUS = {'solved':0,'poly1':1,'poly2':2,'eq1':3,'eq2':4,'other':5}
VARIABLE_STATUS = [1,2,5]

# 定义不能合并字符的情况
REJECT_SYMBOLS = ['0','d','2','3','4','5','6','7','8','9']

# 定义测试集路径
TEST_URL = '../testImgs'
