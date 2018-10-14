from config import *
from sympy import *

# 根据一颗解析树计算表达式的值,每一个节点有不同的行为，因此需要对每一种节点类型定义处理办法
def calculate(node):
    value = 0
    if isinstance(node,dict) and len(node):
        child = node['structure']
        if node['type']==NODE_TYPE['e']:
            t = calculate(child[0])
            if len(child)>1:
                type,e_pi = calculate(child[1])
                if type:
                    return t-e_pi
                return t+e_pi
            return t
        elif node['type']==NODE_TYPE['e_pi']:
            if len(child)>0:
                t = calculate(child[1])
                type,e_pi = calculate(child[2])
                if type == 0:
                    result = t+e_pi
                else:
                    result = t-e_pi
                if child[0]=='-':
                    return 1,result
                return 0,result
            else:
                return 0,0
        elif node['type']==NODE_TYPE['t']:
            f = calculate(child[0])
            if len(child)>1:
                type,t_pi = calculate(child[1])
                if type == 0:
                    return f*t_pi
                else:
                    return f/t_pi
            return f
        elif node['type']==NODE_TYPE['t_pi']:
            if len(child)>0:
                f = calculate(child[1])
                type,t_pi = calculate(child[2])
                if type==0:
                    result = f*t_pi
                else:
                    result = f/t_pi
                if child[0] == 'div':
                    return 1,result
                return 0,result
            else:
                return 0,1
        elif node['type']==NODE_TYPE['bracket']:
            return calculate(child[1])
        elif node['type'] == NODE_TYPE['integer']:
            return int(child)
        elif node['type'] == NODE_TYPE['decimal']:
            return float(child)
    return value

# 定义变量符号表，自动求值时需要使用
# key是字符串，value是使用字符串创建的sympy对象
x = Symbol('x')
y = Symbol('y')
z = Symbol('z')
variable_table = {'x':x,'y':y,'z':z}

forward_step = 1

def set_forward_step(steps):
    global forward_step
    forward_step = steps
# 简化节点，打印计算过程
def simplify_node(node):
    global forward_step

    if node['status'] == STATUS['solved'] and forward_step > 0:
        forward_step = forward_step - 1
        node['structure'] = node['value']

# 后序遍历表达式树，自底向上传递树节点的状态、属性、值
def post_order(node):
    global variable_table,forward_step
    latex_str = ''
    # 若该节点不空
    if isinstance(node, dict) and len(node):

        child  = node['structure']
        # 对于任意一个非叶节点，都是先遍历其子节点，再遍历该节点
        # 对于任意一个叶节点，直接根据节点类型确定其节点状态status和值value
        if node['type'] == NODE_TYPE['constant']:
            print('post_order constant')
            node['status'] = STATUS['solved']
            if node['structure'] == 'pi':
                node['value'] = pi
            elif node['structure'] == 'e':
                node['value'] = E
            latex_str = latex(node['value'])
        elif node['type'] == NODE_TYPE['integer'] or node['type'] == NODE_TYPE['decimal']:
            # print('post_order integer|decimal')
            node['status'] = STATUS['solved']
            # node['attribute'] = ATTRIBUTE['constant']
            if node['type'] == NODE_TYPE['integer']:
                node['value'] = int(node['structure'])
            else:
                node['value'] = float(node['structure'])
            latex_str = str(node['value'])
        elif node['type'] == NODE_TYPE['variable']:
            # print('post_order variable')
            node['status'] = STATUS['poly1']
            # node['attribute'] = ATTRIBUTE['variable']
            # 将变量转化成字符串

            if node['structure'] in variable_table:
                # print('coefficient:',node['coefficient'])
                if isinstance(node['coefficient'],int):
                    node['coefficient'] = int(node['coefficient'])
                if isinstance(node['coefficient'],float):
                    node['coefficient'] = float(node['coefficient'])
                node['value'] = int(node['coefficient'])*variable_table[node['structure']]
                # print(node['value'])
            # node['value'] = str(node['coefficient'])+'*'+node['structure']
            else:
                raise (ValueError,'post_order variable:unrecognized variable')
            # print('coefficient=',node['coefficient'])
            if node['coefficient'] == 1:
                latex_str = node['structure']
            elif node['coefficient'] == -1:
                latex_str = '-'+node['structure']
            else:
                # print('yessss')
                # print(type(node['coefficient']))
                latex_str = str(node['coefficient'])+node['structure']
        elif not isinstance(node['structure'],list):
            return str(node['structure'])
        elif node['type'] == NODE_TYPE['bracket']:
            # print('post_order bracket',child)
            in_bracket = post_order(child[1])
            node['status'] = child[1]['status']
            # node['attribute'] = child[1]['attribute']
            # 如果是含未知数的表达式，则值value为其字符串
            # 如果是不含未知数的表达式，则值为一个常数，是可以直接计算的
            if node['status'] in [ STATUS['poly1'] , STATUS['poly2'],STATUS['other']]:
                node['value'] = (child[1]['value'])
            elif node['status'] == STATUS['solved']:
                node['value'] = child[1]['value']
            else:
                raise(ValueError,'post_order:unresolved node status')
            latex_str = '('+in_bracket+')'



        # elif node['type'] == NODE_TYPE['f']:

        elif node['type'] == NODE_TYPE['t_pi']:
            # print('post_order t_pi')
            if len(child)==2:
                f = post_order(child[1])
                node['status'] = child[1]['status']
                node['value'] = child[1]['value']
                if child[0] == 'times':
                    node['flag'] = 0
                    latex_str = '\\times'+f
                elif child[0] == 'div':
                    node['flag'] = 1
                    latex_str = '\\div'+f
            elif len(child)>2:
                f = post_order(child[1])
                t_pi = post_order(child[2])
                node['status'] = max(child[1]['status'],child[2]['status'])
                if child[2]['flag'] == 1:
                    node['flag'] = 1
                    if node['status']== STATUS['solved']:
                        if child[1]['value']%child[2]['value']==0:
                            # 若两个数能够整除，则要将结果转化成整型，避免python自动转换
                            node['value'] = int(child[1]['value']/(child[2]['value']))
                        else:
                            node['value'] = child[1]['value'] / (child[2]['value'])
                    elif node['status'] == STATUS['poly1'] or node['status'] == STATUS['poly2']:
                        node['value'] = child[1]['value']/child[2]['value']
                    else:
                        raise (ValueError,'post_order:t_pi')
                    latex_str = '\\times'+f+t_pi
                else:
                    node['flag'] = 0
                    if node['status']== STATUS['solved']:
                        node['value'] = child[1]['value']*(child[2]['value'])
                    elif node['status'] == STATUS['poly1'] or node['status'] == STATUS['poly2']:
                        node['value'] = child[1]['value']*(child[2]['value'])
                    else:
                        raise (ValueError,'post_order:t_pi')
                    latex_str = '\\div' + f + t_pi
                simplify_node(node)
            else:
                node['status'] = STATUS['solved']
                node['value'] = 1
                node['flag'] = 0
            # print(node['value'])
        elif node['type']==NODE_TYPE['t']:
            # print('post_order t',child[0])
            f = post_order(child[0])
            node['status'] = child[0]['status']
            node['value'] = child[0]['value']
            latex_str = f
            if len(child)>1:
                t_pi = post_order(child[1])
                latex_str = latex_str  + t_pi
                node['status'] = max(child[0]['status'],child[1]['status'])
                if child[1]['flag'] == 1:

                    if node['status'] == STATUS['solved']:
                        if child[0]['value']%child[1]['value']==0:
                            # 若两个数能够整除，则要将结果转化成整型，避免python自动转换
                            node['value'] = int(child[0]['value']/(child[1]['value']))
                        else:
                            node['value'] = child[0]['value'] / (child[1]['value'])
                    elif node['status'] == STATUS['poly1'] or node['status'] == STATUS['poly2']:
                        node['value'] = child[0]['value']/child[1]['value']
                    else:
                        raise (ValueError,'post_order:t')
                else:

                    if node['status']== STATUS['solved']:
                        node['value'] = child[0]['value']*(child[1]['value'])
                    elif node['status'] in VARIABLE_STATUS:
                        node['value'] = child[0]['value']*child[1]['value']
                    else:
                        raise (ValueError,'post_order:t')
                simplify_node(node)
        elif node['type']==NODE_TYPE['e_pi']:
            # print('post_order e_pi')
            # print('post_order e_pi:',node)
            if len(child) == 2:
                t = post_order(child[1])
                latex_str = child[0]+t
                node['status'] = child[1]['status']
                if child[0] == '+':
                    node['value'] = child[1]['value']
                    node['flag'] = 0
                else:
                    node['value'] = -child[1]['value']
                    node['flag'] = 1
            elif len(child)>2:
                t = post_order(child[1])
                e_pi = post_order(child[2])
                latex_str = child[0] + t + e_pi

                node['status'] = max(child[1]['status'],child[2]['status'])
                if child[0] == '-':
                    child[1]['value'] = -child[1]['value']
                if child[2]['flag'] == 0:
                    if node['status'] == STATUS['solved']:
                        node['value'] = child[1]['value']+child[2]['value']
                    elif node['status'] == STATUS['poly1'] or node['status'] == STATUS['poly2']:
                        node['value'] = child[1]['value'] + child[2]['value']
                    else:
                        raise (ValueError,'post_order:e_pi')
                else:
                    if node['status'] == STATUS['solved']:
                        node['value'] = child[1]['value']+child[2]['value']
                    elif node['status'] == STATUS['poly1'] or node['status'] == STATUS['poly2']:
                        node['value'] = child[1]['value'] + child[2]['value']
                    else:
                        raise (ValueError,'post_order:e_pi')
                if child[0]=='-':
                    node['flag'] = 1
                else:
                    node['flag'] = 0
                simplify_node(node)
            else:
                node['structure'] = 0
                node['status'] = STATUS['solved']
                node['value'] = 0
                node['flag'] = 0
            # print(node['value'])
        elif node['type'] == NODE_TYPE['e']:
            # print('post_order e')
            t = post_order(child[0])
            node['status'] = child[0]['status']
            node['value'] = child[0]['value']
            latex_str = t
            if len(child) > 1:
                e_pi = post_order(child[1])
                latex_str = latex_str + e_pi
                node['status'] = max(child[0]['status'], child[1]['status'])
                # if child[1]['value'] == 3:
                # print('child1',child[1])
                if child[1]['flag'] == 1:

                    if node['status'] == STATUS['solved']:
                        node['value'] = child[0]['value'] + child[1]['value']
                    elif node['status'] == STATUS['poly1'] or node['status'] == STATUS['poly2']:
                        node['value'] = child[0]['value'] + child[1]['value']
                    else:
                        raise (ValueError, 'post_order:e')
                else:
                    if node['status'] == STATUS['solved']:
                        node['value'] = child[0]['value'] + child[1]['value']
                    elif node['status'] in VARIABLE_STATUS:
                        node['value'] = child[0]['value'] + child[1]['value']
                    else:
                        raise (ValueError, 'post_order:t_pi')
                simplify_node(node)
        elif node['type'] == NODE_TYPE['fraction']:
            # print('post_order fraction')
            numerator = post_order(child[0])
            denominator = post_order(child[1])
            latex_str = '\\frac{'+numerator+'}{'+denominator+'}'
            node['status'] = max(child[0]['status'],child[1]['status'])
            if node['status'] == STATUS['solved']:
                if child[0]['value'] != pi and child[0]['value'] != E and \
                        child[1]['value'] != pi and child[1]['value'] != E:
                    node['value'] = Rational(child[0]['value'], child[1]['value'])
                elif child[1]['value'] != 0:
                    node['value'] = child[0]['value']/child[1]['value']
                else:
                    raise ValueError('post_order:denominator =0!')
            else:
                node['value'] = child[0]['value'] / child[1]['value']
        elif node['type'] == NODE_TYPE['int']:
            # print('post_order int')
            # 默认定积分的状态是可以求值的
            integrate_function = post_order(child[0])
            lower_bound = post_order(node['lower_bound'])
            upper_bound = post_order(node['upper_bound'])
            # print(child[0]['value'])
            node['status'] = STATUS['solved']
            node['value'] = integrate(child[0]['value'],\
                            (variable_table[node['integral_var']],node['lower_bound']['value'],node['upper_bound']['value']))
            latex_str = '\\int_{' + lower_bound + '}^{' + upper_bound \
                        + '}' + integrate_function + '\\mathrm{d}' + node['integral_var']
            simplify_node(node)
        elif node['type'] == NODE_TYPE['power']:
            # print('post_order power')
            base_number = post_order(child[0])
            exponent = post_order(child[1])

            if child[0]['status'] == STATUS['solved'] and child[1]['status'] == STATUS['solved']:
                node['status'] = STATUS['solved']
                node['value'] = pow(child[0]['value'],child[1]['value'])
                simplify_node(node)
            elif child[0]['status'] == STATUS['poly1'] and child[1]['status'] == STATUS['solved']:
                node['status'] = STATUS['poly2']
                # 处理平方的trick，如果系数为1，则不变，如果不为1，则4*(4*x/4)**2
                # coefficient = child[0]['coefficient'])
                # print('bbbbb',child[0])
                if  'coefficient' in [child[0].keys] and isinstance(child[0]['coefficient'],int) and child[0]['coefficient']==1:
                    node['value'] = (child[0]['value'])**(child[1]['value'])
                elif ('coefficient' in [child[0].keys] and isinstance(child[0]['coefficient'],int) and child[0]['coefficient']!=1)\
                        or child[0]['type'] == NODE_TYPE['variable'] and (isinstance(child[0]['coefficient'],str) or isinstance(child[0]['coefficient'],int)):
                    # print('yesssssss')
                    coefficient = int(child[0]['coefficient'])
                    exp = child[0]['value'] / coefficient
                    node['value'] = coefficient * exp ** child[1]['value']

                else:
                    node['value'] = child[0]['value'] **child[1]['value']
                    # print(child[0]['value'])

            elif child[0]['status'] == STATUS['solved'] and child[1]['status'] == STATUS['poly1']:
                node['status'] = STATUS['other']
                node['value'] = child[0]['value']**child[1]['value']
            else:
                raise (ValueError,'post_order:power error')

            if len(exponent)>1:
                latex_str = base_number + '^{' + exponent + '}'
            else:
                latex_str = base_number + '^' + exponent
            if node['status'] in VARIABLE_STATUS:
                latex_str = '('+latex_str+')'
        elif node['type'] == NODE_TYPE['equation']:
            # print('post_order equation')
            left = post_order(child[0])
            right = post_order(child[1])
            latex_str = left + '=' + right
            if (child[0]['status'] == STATUS['solved'] and child[1]['status'] == STATUS['solved']) or\
                child[0]['status'] == STATUS['eq1'] or child[0]['status'] == STATUS['eq2'] or \
                child[1]['status'] == STATUS['eq1'] or child[1]['status'] == STATUS['eq2']:
                raise(ValueError,'post_order:equation error')
            else:
                node['status'] = max(child[0]['status'],child[1]['status'])+2
                node['value'] = [child[0]['value'],child[1]['value']]
        elif node['type'] == NODE_TYPE['sqrt']:
            # print('post_order sqrt expression',child[0])
            in_sqrt = post_order(child[0])
            node['status'] = child[0]['status']
            if node['times'] == 2:
                latex_str = '\\sqrt{'+in_sqrt+'}'
                node['value'] = sqrt(child[0]['value'])
            else:
                latex_str = '\\sqrt['+str(node['times'])+']{'+in_sqrt+'}'
                node['value'] = pow(child[0]['value'],S(1)/node['times'])
            simplify_node(node)
        elif node['type'] == NODE_TYPE['function']:
            # print('post_order function')
            if len(child) == 0:
                raise (ValueError,'post_order:no element after function')
            in_function = post_order(child[0])
            node['status'] = child[0]['status']
            c = node['name']
            if c != 'log':
                if c == 'sin':
                    node['value'] = sin(child[0]['value'])
                elif c== 'cos':
                    node['value'] = cos(child[0]['value'])
                elif c == 'tan':
                    node['value'] = tan(child[0]['value'])
                latex_str = '\\'+node['name']+in_function
            else:
                if node['radix'] == 'e':
                    node['value'] = ln(child[0]['value'])
                    latex_str = '\\ln'+in_function
                else:
                    node['value'] = log(child[0]['value'],node['radix'])
                    latex_str = '\\log_{'+str(node['radix'])+'}'+str(child[0]['value'])
            simplify_node(node)
        elif node['type'] == NODE_TYPE['derivation']:
            # print('post_order:derivation:',child[0])
            in_derivation = post_order(child[0])
            latex_str = in_derivation + '\''
            if child[0]['status'] == STATUS['solved']:
                node['value'] = 0
                node['status'] = STATUS['solved']

            elif child[0]['status'] in [STATUS['poly1'],STATUS['poly2'],STATUS['other']]:
                node['status'] = STATUS['other']
                node['value'] = diff(child[0]['value'],x)
                # print(node['value'])
            else:
                raise ValueError('post_order:unresolved derivation status')
        elif node['type'] == NODE_TYPE['limitation']:
            in_limitation = post_order(child[0])

            node['status'] = STATUS['solved']
            variable = variable_table[node['variable']]
            if isinstance(node['near_to_value'],int):
                latex_str = '\\lim_{x\\to' + str(node['near_to_value']) + '}' + in_limitation
                node['value'] = limit(child[0]['value'],variable,node['near_to_value'])
            elif node['near_to_value'] == 'infty':
                latex_str = '\\lim_{x\\to\infty}' + in_limitation
                node['value'] = limit(child[0]['value'], variable,oo)
            else:
                raise ValueError('near to value error')
            simplify_node(node)
    return latex_str

# 求解表达式树
def solve_expression(parser_tree):
    global x
    post_order(parser_tree)
    if parser_tree['type'] == NODE_TYPE['equation']:
        child = parser_tree['structure']
        # print(child[0]['value'],child[1]['value'])
        return solve(Eq(child[0]['value'],child[1]['value']),x)
    else:
        return parser_tree['value']



