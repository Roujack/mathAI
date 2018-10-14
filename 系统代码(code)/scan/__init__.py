from config import  DFA_STATE
import config
from tools import get_spatial_relationship,join_locations,get_keys

# 获取下一个字符，当且仅当(1)存在右边字符时,(2)小数点才返回，其它一律返回终结符'#'
def get_next_char(characters,start_index,char_cnt):
    if(start_index<len(characters)):
        c = characters[start_index]['candidates'][0]['symbol']
        # 如果是第一个字符，不过它跟前面字符的位置关系是什么，都直接返回
        if (char_cnt == 0):
            # 对分数符还需做特殊处理
            if c == '-' and start_index>0:
                pre_location = characters[start_index - 1]['location']
                cx1 = (pre_location[0]+pre_location[0]+pre_location[2])/2

                location = characters[start_index]['location']

                relationship = get_spatial_relationship(pre_location,location)
                if relationship == config.SPACIAL_RELATIONSHIP['up'] or cx1>=location[0] and\
                        cx1 < location[0]+location[2]:
                    return 'f',start_index+1,char_cnt+1
            return c, start_index + 1,char_cnt+1
        if start_index>0:
            previous_c = characters[start_index-1]['candidates'][0]['symbol']
            pre_location = characters[start_index-1]['location']
            cx1 = (pre_location[0] + pre_location[0] + pre_location[2]) / 2
            location = characters[start_index]['location']
            relationship = get_spatial_relationship(pre_location,location)
            # print('relationship,pc,c',get_keys(config.SPACIAL_RELATIONSHIP,relationship),previous_c,c)
            if relationship == config.SPACIAL_RELATIONSHIP['right'] or \
                (previous_c in config.DECIMAL_POINT and relationship == config.SPACIAL_RELATIONSHIP['left_down']):#需要修改，小数点在前的空间关系还没有定义
                return c,start_index+1,char_cnt+1
            elif (c in config.DECIMAL_POINT and relationship == config.SPACIAL_RELATIONSHIP['subscript']):
                return '.',start_index+1,char_cnt+1
            # 如果-符号上方或者斜上方有字符，说明是分数符
            elif (c == '-' and relationship == config.SPACIAL_RELATIONSHIP['up'] or cx1>=location[0] and\
                        cx1 < location[0]+location[2]):
                return 'f',start_index+1,char_cnt+1
            else:
                return '#',start_index+1,char_cnt+1


    return '#',start_index+1,char_cnt+1

# 从characters的start_index位置开始识别出第一个token，并返回token以及下一次getToken的初始下标
def get_token(characters,start_index=0):
    token = []
    token_string = ''
    index = start_index
    state = DFA_STATE['START']
    token_type = config.TOKEN_TYPE['ERROR']
    coefficient = 1
    char_cnt = 0
    while(state != DFA_STATE['DONE'] and index <= len(characters)):
        c,index,char_cnt = get_next_char(characters,index,char_cnt)
        # print('自动机状态：',get_keys(config.DFA_STATE,state),' 字符：',c,' 索引：',index)
        save = True
        if state == DFA_STATE['START']:
            if c.isdigit():
                state = DFA_STATE['INCONSTANT']
            else:
                state = DFA_STATE['DONE']
                if c in config.RESERVE:
                    token_type = config.TOKEN_TYPE['RESERVE']
                elif c in config.VARIABLE:
                    token_type = config.TOKEN_TYPE['VARIABLE']
                elif c in config.FUNCTION:
                    token_type = config.TOKEN_TYPE['FUNCTION']
                elif c in config.OPERATOR:
                    token_type = config.TOKEN_TYPE['OPERATOR']
                elif c in config.SPECIAL:
                    token_type = config.TOKEN_TYPE['SPECIAL']
                elif c in config.CMP:
                    token_type = config.TOKEN_TYPE['CMP']
                elif c == '#':
                    token_type = config.TOKEN_TYPE['END']
                elif c == 'f':
                    token_type = config.TOKEN_TYPE['OPERATOR']
                elif c == 'int':
                    token_type = config.TOKEN_TYPE['OPERATOR']
                else:
                    token_type = config.TOKEN_TYPE['ERROR']
        elif state == DFA_STATE['INCONSTANT']:
            if c == '.':
                state = DFA_STATE['INDECIMAL']
            elif c.isdigit():
                state = DFA_STATE['INCONSTANT']
            elif c in config.RESERVE:
                state = DFA_STATE['INRESERVE']
            elif c in config.VARIABLE:
                state = DFA_STATE['INVARIABLE']
            else:
                save = False
                token_type = config.TOKEN_TYPE['CONSTANT_INTEGER']
                state = DFA_STATE['DONE']
        elif state == DFA_STATE['INDECIMAL']:
            if c.isdigit():
                state = DFA_STATE['INDECIMAL']
            elif c in config.RESERVE:
                state = DFA_STATE['INRESERVE']
            elif c in config.VARIABLE:
                state = DFA_STATE['INVARIABLE']
            else:
                save = False
                token_type = config.TOKEN_TYPE['CONSTANT_DECIMAL']
                state = DFA_STATE['DONE']
        elif state == DFA_STATE['INVARIABLE']:
            save = False
            state = DFA_STATE['DONE']
            token_type = config.TOKEN_TYPE['VARIABLE']
            coefficient = token_string[0:-1]
            token_string = token_string[-1]
        elif state == DFA_STATE['INRESERVE']:
            save = False
            state = DFA_STATE['DONE']
            token_type = config.TOKEN_TYPE['RESERVE']
            coefficient = token_string[0:-1]
            token_string = token_string[-1]
        else:
            raise(ValueError,'未处理的自动机状态')

        if state == DFA_STATE['DONE'] and not save:
                index -= 1
        if save :
            token_string += c
    # 合并多个symbol组合成的token，变成一个大矩形
    if characters[index-1]['candidates'][0]['symbol'] == 'x':
        location = join_locations([x['location'] for x in characters[index-1:index]])
    else:
        location = join_locations([x['location'] for x in characters[start_index:index]])
    token = {'location':location,'token_string':token_string,
             'token_type':token_type}
    if(token_type == config.TOKEN_TYPE['RESERVE'] or token_type == config.TOKEN_TYPE['VARIABLE']):
        token = {'location': location, 'token_string': token_string,
                 'token_type': token_type,
                 'coefficient': coefficient}
    # print('token,index=',token,index)
    return token,index