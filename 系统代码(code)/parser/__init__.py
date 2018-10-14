import scan
import config
import numpy as np
import tools
import sympy

characters = []
current_node = {'type':config.NODE_TYPE['default'],'structure':0,'location':[0,0,1,1]}
next_index = 0
node_list = []
def parser(temp_node_list):
    length = len(temp_node_list)
    if length == 0:
        raise (ValueError,'parser:node_list length = 0!')
    if length == 1:
        return temp_node_list[0]
    global current_node,next_index,node_list
    next_index = 0
    node_list = temp_node_list
    # if next_index < length:
    current_node = node_list[next_index]
    next_index += 1
    # 采用递归下降法解析单行表达式
    parser_tree = E()
    return parser_tree

# 匹配当前token是否为预期的token类型expected
def match(expected):
    global current_node,node_list,next_index
    length = len(node_list)
    #print('matching node:',current_node)
    #print('expected node:', expected,next_index,length)

    # #print('length,index',length,next_index)
    if isinstance(expected,np.str) and current_node['structure'] == expected:
        if next_index<length:
            current_node = node_list[next_index]
            next_index = next_index+1
        else:
            pass
        # #print('current_node:',current_node)
    elif isinstance(expected,np.int) and current_node['type'] == expected and next_index<length:
        # current_node = node_list[next_index]
        # next_index = next_index + 1
        if next_index<length:
            current_node = node_list[next_index]
            next_index = next_index+1
        else:
            pass
        # #print('current_node:',current_node)
    # elif isinstance(expected,dict) and next_index < length:
    #     current_node = node_list[next_index]
    #     next_index = next_index + 1
    elif isinstance(expected,dict):
        if(next_index < length):
            current_node = node_list[next_index]
        next_index = next_index+1

    else:
        raise(ValueError,'unexpected node!')

# 创建树节点
def new_node(node_type=config.NODE_TYPE['default']):
    node = {}
    if(node_type == config.NODE_TYPE['bracket']):
        node = {'structure':['(',{},')'],'type':config.NODE_TYPE['bracket']}
    elif node_type == config.NODE_TYPE['integer']:
        node = {'structure':0,'type':config.NODE_TYPE['integer']}
    elif node_type == config.NODE_TYPE['decimal']:
        node = {'structure':0,'type':config.NODE_TYPE['decimal']}
    elif node_type == config.NODE_TYPE['variable']:
        node = {'structure':'x','type':config.NODE_TYPE['variable'],'coefficient':1}
    elif node_type == config.NODE_TYPE['int']:
        node = {'structure':[],'type':node_type,'upper_bound':0,'lower_bound':0,'integral_var':0}
    elif node_type == config.NODE_TYPE['sqrt']:
        node = {'structure':[],'type':node_type,'times':2}
    # elif node_type == config.NODE_TYPE['t_pi']:
    #     node = {'structure':1,'type':node_type}
    elif node_type in [x[1] for x in config.NODE_TYPE.items()]:
        node = {'structure':[],'type':node_type}
    else:
        raise(ValueError,'new node:unknown node type')
    return node

def token_to_node(token):
    c = token['token_string']
    node = new_node()
    #print('token_to_node:', token)
    if c in config.SPECIAL or c in config.CMP:
        node = new_node(config.NODE_TYPE['default'])
        node['structure'] = c
    elif token['token_type']==config.TOKEN_TYPE['OPERATOR']:
        node = new_node(config.NODE_TYPE['operator'])
        node['structure'] = c
    elif token['token_type'] == config.TOKEN_TYPE['CONSTANT_INTEGER']:
        node = new_node(config.NODE_TYPE['integer'])
        node['structure'] = int(c)
        # match(config.TOKEN_TYPE['CONSTANT_INTEGER'])
    elif token['token_type'] == config.TOKEN_TYPE['CONSTANT_DECIMAL']:
        node = new_node(config.NODE_TYPE['decimal'])
        node['structure'] = float(c)
        # match(config.TOKEN_TYPE['CONSTANT_DECIMAL'])
    elif token['token_type'] == config.TOKEN_TYPE['VARIABLE']:
        node = new_node(config.NODE_TYPE['variable'])
        node['structure'] = c
        node['coefficient'] = token['coefficient']
        # match(config.TOKEN_TYPE['VARIABLE'])
    elif token['token_string'] in config.RESERVE or token['token_string'] in config.FUNCTION:
        # #print('wtf',config.TOKEN_TO_NODE[token['token_type']])
        node = new_node(config.TOKEN_TO_NODE[token['token_type']])
        node['structure'] = c
    # elif current_token['token_type'] == config.TOKEN_TYPE['']

    else:

        raise (ValueError, 'token to node:unresolved token type')
    node['location'] = token['location']
    # #print('token_to_node',node)
    return node

def F():
    global current_node
    c = current_node['structure']
    # #print(current_node)
    # #print('calling F()', current_node['type'],c)
    node = new_node()
    if c == '(':
        node = new_node(config.NODE_TYPE['bracket'])
        match('(')
        node['structure'][1] = E()
        match(')')
    else:
        node = current_node
        match(current_node)
    # elif current_node['token_type'] == config.TOKEN_TYPE['CONSTANT_INTEGER']:
    #     node = new_node(config.NODE_TYPE['integer'])
    #     node['structure'] = int(c)
    #     match(config.TOKEN_TYPE['CONSTANT_INTEGER'])
    # elif current_node['token_type'] == config.TOKEN_TYPE['CONSTANT_DECIMAL']:
    #     node = new_node(config.NODE_TYPE['decimal'])
    #     node['structure'] = float(c)
    #     match(config.TOKEN_TYPE['CONSTANT_DECIMAL'])
    # elif current_node['token_type'] == config.TOKEN_TYPE['VARIABLE']:
    #     node = new_node(config.NODE_TYPE['variable'])
    #     node['structure'] = c
    #     node['coefficient'] = current_node['coefficient']
    #     match(config.TOKEN_TYPE['VARIABLE'])
    #     #print(current_node)
    # else:
    #     raise (ValueError,'F():cannot find suitable production')
    return node

def T_pi():
    # #print('calling T_pi()')
    global current_node
    node = new_node(config.NODE_TYPE['t_pi'])
    # #print(current_node)
    c = current_node['structure']
    if c == 'times' or c == 'div':
        match(c)
        f = F()
        t_pi = T_pi()
        node = new_node(config.NODE_TYPE['t_pi'])
        node['structure'].append(c)
        node['structure'].append(f)
        if len(t_pi['structure']) > 0:
            node['structure'].append(t_pi)
    # else:
    #     node['structure'] = 1
    return node

def T():
    # #print('calling T()')
    global current_node
    f = F()
    t_pi = T_pi()
    node = new_node(config.NODE_TYPE['t'])
    node['structure'].append(f)
    if len(t_pi['structure'])>0:
        node['structure'].append(t_pi)
    return node

def E_pi():
    global current_node
    # #print('calling E_pi(),current_node',current_node)

    node = new_node(config.NODE_TYPE['e_pi'])
    c = current_node['structure']
    if c == '+' or c == '-':
        match(c)
        t = T()
        e_pi = E_pi()
        node['structure'].append(c)
        node['structure'].append(t)
        if len(e_pi['structure'])>0:
            node['structure'].append(e_pi)
    # else:
    #     node['structure'] = 0
    return node
# 这里的E是指single line expression
def E():
    # #print('calling E()')
    global current_node
    t = T()
    e_pi = E_pi()
    node = new_node(config.NODE_TYPE['e'])
    node['structure'].append(t)
    if len(e_pi['structure'])>0:
        node['structure'].append(e_pi)
    return node

# 从characters的index开始，查找第一个可以解构的表达式
def find_first_op(node_list,index):
    relationship = config.SPACIAL_RELATIONSHIP['unknown']
    length = len(node_list)
    while index < length:
        node  = node_list[index]

        if index>=1:
            pre_node = node_list[index-1]
            relationship = tools.get_spatial_relationship(pre_node['location'],node['location'])
        #print('find_first_op', node, tools.get_keys(config.SPACIAL_RELATIONSHIP, relationship))
        if node['type'] == config.NODE_TYPE['operator']:
            if node['structure'] == 'f':
                return config.OP_TYPE['fraction'],index
            # elif  node['structure']=='int':
            #     return config.OP_TYPE['int'],index
            elif node['structure'] == 'sqrt':
                return config.OP_TYPE['sqrt'],index
        if node['structure'] == '=':
            return config.OP_TYPE['equation'],index
        if relationship == config.SPACIAL_RELATIONSHIP['superscript'] and node['type'] in config.POWERABLE \
                and index>0 and (node_list[index-1]['type'] in config.POWERABLE or node_list[index-1]['structure']==')'):
            return config.OP_TYPE['power'],index-1
        index = index + 1
    return config.OP_TYPE['normal'],len(node_list)
# 查找第一个积分符d
def find_first_d(node_list,index):
    length = len(node_list)
    for index,node in enumerate(node_list):
        if(node['structure']=='d'):
            return index
    return length
# 查找分数符号的作用域,区间是[start_index,end_index)
def search_bounds(node_list,index):
    location = node_list[index]['location']
    left = location[0]
    right = left+location[2]
    up = location[1]
    down = location[3]+up
    length = len(node_list)
    # 查找分数线上边
    start_index = index
    i = index-1
    y_min= 0
    y_max= 0
    while i >= 0:
        node = node_list[i]
        current_left = node['location'][0]
        current_right = current_left+node['location'][2]
        y1 = node['location'][1]
        y2 = node['location'][3]+y1
        cy = (y1+y2)/2
        # #print('search bounds',node)
        # #print(i,start_index,index,left,right,current_left,current_right,cy,y_min,y_max)
        # 只要线段有重叠，且中心纵坐标跟之前字符
        if (start_index == index or (cy>=y_min and cy<=y_max and y2< up)) and (current_left>=left and current_right<= right or current_left<left and current_right>left\
            or current_left<right and current_right >right):
            start_index = i
            if start_index == index-1:
                y_min = node['location'][1]
                y_max = y_min+node['location'][3]
            else:
                if y1<y_min:
                    y_min = y1
                if y2>y_max:
                    y_max = y2

        else:
            break
        i = i-1
    # 处理分数线下边
    end_index = index
    i = index + 1
    y_min = 0
    y_max = 0
    while i < length:
        node = node_list[i]
        # #print('处理分母',node)
        current_left = node['location'][0]
        current_right = current_left + node['location'][2]
        y1 = node['location'][1]
        y2 = node['location'][1] + y1
        cy = (y1 + y2) / 2
        # 只要线段有重叠，且中心纵坐标跟之前字符
        if (end_index == index or (cy >= y_min and cy <= y_max and y1>down)) and (
                current_left >= left and current_right <= right or current_left < left and current_right > left \
                or current_left < right and current_right > right):
            end_index = i
            # #print(node_list[end_index])
            if end_index == index:
                y_min = node_list[i][1]
                y_max = y_min + node_list[i][3]
            else:
                if y1 < y_min:
                    y_min = y1
                if y2 > y_max:
                    y_max = y2
        else:
            break
        i = i + 1
    # start_index = length
    # end_index = length
    # cnt = 0
    # for index,node in enumerate(node_list):
    #     current_left = node['location'][0]
    #     current_right = current_left+node['location'][2]
    #     # 只要线段有重叠，且中心纵坐标跟之前字符
    #     if current_left>=left and current_right<= right or current_left<left and current_right>left\
    #         or current_left<right and current_right >right:
    #         if cnt == 0:
    #             start_index = index
    #         cnt = cnt+1
    # end_index = start_index+cnt
    return start_index,end_index+1

# 查找各种特殊表达式的作用域
def search_sqrt_field(node_list,index):
    length = len(node_list)
    i = index+1
    if i >= length:
        raise (ValueError,'search_sqrt_field:no symbol after sqrt!')
    node = node_list[index]
    # # 处理立方根
    # if i < length and node_list[i]['type'] == config.NODE_TYPE['integer'] and \
    #         tools.get_spatial_relationship(node['location'], node_list[i]['location']) == \
    #         config.SPACIAL_RELATIONSHIP['left_up']:
    #     t = node
    #     node_list[index] = node_list[index + 1]
    #     node_list[index + 1] = t
    #     index = index+1
    #     i = index+1
    #     #print('sqrt modify',node_list)
    spacial_relationship = tools.get_spatial_relationship(node['location'],node_list[index+1]['location'])
    # #print('sqrttttttttt',spacial_relationship)
    while( i<length and tools.get_spatial_relationship(node_list[index]['location'],node_list[i]['location'])==config.SPACIAL_RELATIONSHIP['including'] ):
        i = i + 1
    if index>0 and tools.get_spatial_relationship(node_list[index]['location'],node_list[index-1]['location'])==\
                                                  config.SPACIAL_RELATIONSHIP['left_up'] and node_list[index-1]['type']\
        == config.NODE_TYPE['integer']:
        return index-1,i

    else:
        return index,i
# 查找平方的作用域
def search_power_field(node_list,index):
    length = len(node_list)
    node = node_list[index]
    if node['structure'] == ')':
        i = index-1
        while i>=0 and node_list[i]['structure']!='(':
            i = i-1
        return i
    else:
        return index
# 查找同级的节点
def search_same_level_nodes(node_list,index):
    length = len(node_list)
    i = index+1
    # if i<length:
        #print(tools.get_spatial_relationship(node_list[i-1]['location'],node_list[i]['location']))
    while i<length and tools.get_spatial_relationship(node_list[i-1]['location'],node_list[i]['location'])==\
                                                  config.SPACIAL_RELATIONSHIP['right']:
        i = i+1
    return i
# 解析分数表达式
def fraction_expression():
    pass

# 将characters转化成node list
def characters_to_nodes(characters):
    # global left_bracket_cnt
    length = len(characters)
    index = 0
    node_list = []
    while index < length:
        current_token, index = scan.get_token(characters, index)
        # 将token转化为node
        node  = token_to_node(current_token)
        node_list.append(node)
    # modify_nodes(node_list)
    return node_list

# 对节点序列做预处理
def modify_nodes_1(node_list):
    pass

# 第三个级别的公式解析
def modify_nodes_2(node_list):
   pass

# 将多个节点合并成一个节点
def replace_nodes_to_one(node_list,start_index,end_index,node):
    # #print('replace before',node_list)
    for i in range(end_index-start_index):
        node_list.remove(node_list[start_index])
    node_list.insert(start_index,node)
    # #print('after replace',node_list)
# 解析characters，是解析整个表达式的入口
def decompose(node_list):
    pass