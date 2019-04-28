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


# 解析characters，是解析整个表达式的入口
def decompose(node_list):
    # 目前只能处理一维的算术表达式，其它表达式的处理方法暂不公开。
    return parser(node_list)