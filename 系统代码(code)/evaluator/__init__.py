# 求极限测试样例:https://github.com/sympy/sympy/blob/master/sympy/series/tests/test_demidovich.py
from solver import *
import os
from config import *
answer = [
{'number': '63', 'level': 'easy', 'latex': '\\sqrt{64},', 'answer': '8'},
{'number': '64', 'level': 'easy', 'latex': '\\sqrt{9},', 'answer': '3'},
{'number': '73', 'level': 'easy', 'latex': '\\sqrt[3]{64},', 'answer': '4'},
{'number': '71', 'level': 'easy', 'latex': '\\sqrt[3]{8},', 'answer': '2'},
{'number': '70', 'level': 'easy', 'latex': '\\sqrt{100},', 'answer': '10'},
{'number': '68', 'level': 'easy', 'latex': '\\sqrt{49},', 'answer': '7'},
{'number': '61', 'level': 'easy', 'latex': '\\sqrt{1},', 'answer': '1'},
{'number': '69', 'level': 'easy', 'latex': '\\sqrt{81},', 'answer': '9'},
{'number': '67', 'level': 'easy', 'latex': '\\sqrt{36},', 'answer': '6'},
{'number': '62', 'level': 'easy', 'latex': '\\sqrt{4},', 'answer': '2'},
{'number': '66', 'level': 'easy', 'latex': '\\sqrt{25},', 'answer': '5'},
{'number': '65', 'level': 'easy', 'latex': '\\sqrt{16},', 'answer': '4'},
{'number': '74', 'level': 'easy', 'latex': '\\sqrt[3]{125},', 'answer': '5'},
{'number': '72', 'level': 'easy', 'latex': '\\sqrt[3]{27},', 'answer': '3'},
{'number': '75', 'level': 'easy', 'latex': '\\sqrt[3]{216},', 'answer': '6'},
{'number': '111', 'level': 'easy', 'latex': '\\int_{0},^{1},x\\mathrm{d},x', 'answer': '\\frac{1},{2},'},
{'number': '114', 'level': 'easy', 'latex': '\\int_{0},^{\\pi},\\sinx\\mathrm{d},x', 'answer': '2'},
{'number': '113', 'level': 'easy', 'latex': '\\int_{1},^{e},\\frac{1},{x},\\mathrm{d},x', 'answer': '1'},
{'number': '109', 'level': 'easy', 'latex': '\\int_{0},^{\\pi},\\cosx\\mathrm{d},x', 'answer': '0'},
{'number': '106', 'level': 'easy', 'latex': '\\int_{3},^{4},x\\mathrm{d},x', 'answer': '\\frac{7},{2},'},
{'number': '112', 'level': 'easy', 'latex': '\\int_{1},^{2},x\\mathrm{d},x', 'answer': '\\frac{3},{2},'},
{'number': '108', 'level': 'easy', 'latex': '\\int_{5},^{6},1\\mathrm{d},x', 'answer': '1'},
{'number': '107', 'level': 'easy', 'latex': '\\int_{4},^{5},x\\mathrm{d},x', 'answer': '\\frac{9},{2},'},
{'number': '110', 'level': 'easy', 'latex': '\\int_{0},^{1},2x\\mathrm{d},x', 'answer': '1'},
{'number': '115', 'level': 'easy', 'latex': '\\int_{0},^{\\frac{\\pi},{2},},\\cosx\\mathrm{d},x', 'answer': '1'},
{'number': '46', 'level': 'easy', 'latex': '\\frac{1},{4},\\times\\frac{7},{3},', 'answer': '\\frac{7},{12},'},
{'number': '50', 'level': 'easy', 'latex': '\\frac{6},{30},-\\frac{5},{30},', 'answer': '\\frac{1},{30},'},
{'number': '57', 'level': 'easy', 'latex': '\\frac{3},{7},+\\frac{2},{3},', 'answer': '\\frac{23},{21},'},
{'number': '47', 'level': 'easy', 'latex': '\\frac{3},{2},\\times\\frac{1},{4},', 'answer': '\\frac{3},{8},'},
{'number': '49', 'level': 'easy', 'latex': '\\frac{7},{5},-\\frac{4},{3},', 'answer': '\\frac{1},{15},'},
{'number': '53', 'level': 'easy', 'latex': '\\frac{7},{10},+\\frac{1},{2},', 'answer': '\\frac{6},{5},'},
{'number': '48', 'level': 'easy', 'latex': '\\frac{2},{7},+\\frac{1},{3},', 'answer': '\\frac{13},{21},'},
{'number': '52', 'level': 'easy', 'latex': '\\frac{4},{9},-\\frac{2},{3},', 'answer': '-\\frac{2},{9},'},
{'number': '59', 'level': 'easy', 'latex': '\\frac{1},{9},\\times\\frac{9},{10},', 'answer': '\\frac{10},{81},'},
{'number': '41', 'level': 'easy', 'latex': '\\frac{1},{2},+\\frac{4},{3},', 'answer': '\\frac{11},{6},'},
{'number': '55', 'level': 'easy', 'latex': '\\frac{12},{3},\\div\\frac{4},{3},', 'answer': '3'},
{'number': '60', 'level': 'easy', 'latex': '\\frac{3},{9},\\div\\frac{1},{3},', 'answer': '1'},
{'number': '43', 'level': 'easy', 'latex': '\\frac{1},{2},\\times\\frac{4},{3},', 'answer': '\\frac{2},{3},'},
{'number': '54', 'level': 'easy', 'latex': '\\frac{6},{11},+\\frac{1},{2},', 'answer': '\\frac{23},{22},'},
{'number': '58', 'level': 'easy', 'latex': '\\frac{4},{2},+\\frac{7},{5},', 'answer': '\\frac{17},{5},'},
{'number': '56', 'level': 'easy', 'latex': '\\frac{2},{4},\\div\\frac{1},{2},', 'answer': '1'},
{'number': '51', 'level': 'easy', 'latex': '\\frac{7},{8},+\\frac{1},{8},', 'answer': '1'},
{'number': '44', 'level': 'easy', 'latex': '\\frac{5},{3},\\times\\frac{4},{5},', 'answer': '\\frac{4},{3},'},
{'number': '45', 'level': 'easy', 'latex': '\\frac{11},{33},+\\frac{22},{33},', 'answer': '1'},
{'number': '42', 'level': 'easy', 'latex': '\\frac{6},{5},-\\frac{3},{5},', 'answer': '\\frac{3},{5},'},
{'number': '160', 'level': 'hard', 'latex': '\\frac{1},{3},\\times\\frac{3},{2},+\\lim_{x\\to1},\\frac{\\sqrt{x},-1},{x-1},-\\int_{1},{e},\\frac{1},{x},\\mathrm{d},x', 'answer': '0'},
{'number': '157', 'level': 'hard', 'latex': 'x^{2},-\\int_{0},^{\\frac{\\pi},{2},},\\cosx\\mathrm{d},x=3', 'answer': '[-2,2]'},
{'number': '156', 'level': 'hard', 'latex': '\\lim_{x\\to\\infty},\\frac{2^{x+1},+3^{x+1},},{2^{x},+3^{x},},', 'answer': '3'},
{'number': '159', 'level': 'hard', 'latex': '12+(200-25\\times4)-56', 'answer': '56'},
{'number': '158', 'level': 'hard', 'latex': '\\int_{0},^{1},2x\\mathrm{d},x+\\lim_{x\\to0},\\frac{\\tanx},{x},', 'answer': '2'},
{'number': '154', 'level': 'medium', 'latex': "(x^3-3x^2+1)'", 'answer': '3x^{2},-6x'},
{'number': '148', 'level': 'medium', 'latex': 'lim_{x\\to0},\\frac{\\sin{3x},},{x},', 'answer': '3'},
{'number': '146', 'level': 'medium', 'latex': '\\frac{x+5},{2},=1', 'answer': '[-3]'},
{'number': '149', 'level': 'medium', 'latex': '\\lim_{x\\to1},\\frac{\\sqrt{x},-1},{x-1},', 'answer': '\\frac{1},{2},'},
{'number': '141', 'level': 'medium', 'latex': '2\\times4+6\\div3', 'answer': '10'},
{'number': '153', 'level': 'medium', 'latex': "(\\frac{1},{3},\\times(x^3)+2x+1)'", 'answer': 'x^{2},+2'},
{'number': '152', 'level': 'medium', 'latex': "(x\\times(e^x))'", 'answer': 'xe^{x},+e^{x},'},
{'number': '150', 'level': 'medium', 'latex': '(2x^2)+3x-4=(x^2)+4x+8', 'answer': '[-3,4]'},
{'number': '144', 'level': 'medium', 'latex': '7+8\\times5+3', 'answer': '50'},
{'number': '151', 'level': 'medium', 'latex': '(4x^2)-(3x^2)+3x+1=x', 'answer': '[-1]'},
{'number': '142', 'level': 'medium', 'latex': '10+2\\times6-4', 'answer': '18'},
{'number': '147', 'level': 'medium', 'latex': '\\lim_{x\\to\\infty},\\frac{(x+1)^2},{x^2+1},', 'answer': '1'},
{'number': '145', 'level': 'medium', 'latex': '12\\div4+9\\times11', 'answer': '102'},
{'number': '143', 'level': 'medium', 'latex': '2\\times4-6\\div3', 'answer': '6'},
{'number': '155', 'level': 'medium', 'latex': '\\int_{0},^{1},(2x+1)\\mathrm{d},x', 'answer': '2'},
{'number': '31', 'level': 'easy', 'latex': '9\\times10', 'answer': '90'},
{'number': '24', 'level': 'easy', 'latex': '9\\times6', 'answer': '54'},
{'number': '22', 'level': 'easy', 'latex': '3\\times4', 'answer': '12'},
{'number': '34', 'level': 'easy', 'latex': '7\\times5', 'answer': '35'},
{'number': '21', 'level': 'easy', 'latex': '2\\times1', 'answer': '2'},
{'number': '29', 'level': 'easy', 'latex': '5\\times6', 'answer': '30'},
{'number': '33', 'level': 'easy', 'latex': '100\\times2', 'answer': '200'},
{'number': '30', 'level': 'easy', 'latex': '7\\times8', 'answer': '56'},
{'number': '32', 'level': 'easy', 'latex': '3\\times3', 'answer': '9'},
{'number': '23', 'level': 'easy', 'latex': '4\\times2', 'answer': '8'},
{'number': '126', 'level': 'easy', 'latex': "x'", 'answer': '1'},
{'number': '128', 'level': 'easy', 'latex': "(2x)'", 'answer': '2'},
{'number': '129', 'level': 'easy', 'latex': "1'", 'answer': '0'},
{'number': '131', 'level': 'easy', 'latex': "((e^x))'", 'answer': 'e^x'},
{'number': '132', 'level': 'easy', 'latex': "(\\sinx)'", 'answer': '\\cos{\\left(x\\right)},'},
{'number': '134', 'level': 'easy', 'latex': "(2x)'", 'answer': '2'},
{'number': '135', 'level': 'easy', 'latex': "(2x^2)'", 'answer': '4x'},
{'number': '130', 'level': 'easy', 'latex': "(\\lnx)'", 'answer': '\\frac{1},{x},'},
{'number': '127', 'level': 'easy', 'latex': "(\\frac{1},{x},)'", 'answer': '-\\frac{1},{x^{2},},'},
{'number': '133', 'level': 'easy', 'latex': "(\\sqrt{x},)'", 'answer': '\\frac{1},{2\\sqrt{x},},'},
{'number': '27', 'level': 'easy', 'latex': '10\\div5', 'answer': '2'},
{'number': '38', 'level': 'easy', 'latex': '33\\div3', 'answer': '11'},
{'number': '35', 'level': 'easy', 'latex': '9\\div3', 'answer': '3'},
{'number': '37', 'level': 'easy', 'latex': '14\\div7', 'answer': '2'},
{'number': '40', 'level': 'easy', 'latex': '108\\div4', 'answer': '27'},
{'number': '26', 'level': 'easy', 'latex': '6\\div3', 'answer': '2'},
{'number': '25', 'level': 'easy', 'latex': '4\\div2', 'answer': '2'},
{'number': '28', 'level': 'easy', 'latex': '121\\div11', 'answer': '11'},
{'number': '39', 'level': 'easy', 'latex': '18\\div9', 'answer': '2'},
{'number': '36', 'level': 'easy', 'latex': '12\\div6', 'answer': '2'},
{'number': '91', 'level': 'easy', 'latex': '\\sin0', 'answer': '0'},
{'number': '93', 'level': 'easy', 'latex': '\\cos0', 'answer': '1'},
{'number': '101', 'level': 'easy', 'latex': '\\cos\\pi', 'answer': '-1'},
{'number': '100', 'level': 'easy', 'latex': '\\cos\\frac{\\pi},{4},', 'answer': '\\frac{\\sqrt{2},},{2},'},
{'number': '102', 'level': 'easy', 'latex': '\\tan\\frac{\\pi},{4},', 'answer': '1'},
{'number': '99', 'level': 'easy', 'latex': '\\sin\\pi', 'answer': '0'},
{'number': '96', 'level': 'easy', 'latex': '\\log_{2},4', 'answer': '2'},
{'number': '105', 'level': 'easy', 'latex': '\\lne^2', 'answer': '2'},
{'number': '104', 'level': 'easy', 'latex': '\\lne', 'answer': '1'},
{'number': '103', 'level': 'easy', 'latex': '\\log_{2},8', 'answer': '3'},
{'number': '95', 'level': 'easy', 'latex': '\\log_{2},2', 'answer': '1'},
{'number': '94', 'level': 'easy', 'latex': '\\cos\\frac{\\pi},{6},', 'answer': '\\frac{\\sqrt{3},},{2},'},
{'number': '97', 'level': 'easy', 'latex': '\\sin\\frac{\\pi},{4},', 'answer': '\\frac{\\sqrt{2},},{2},'},
{'number': '98', 'level': 'easy', 'latex': '\\sin\\frac{\\pi},{3},', 'answer': '\\frac{\\sqrt{3},},{2},'},
{'number': '92', 'level': 'easy', 'latex': '\\sin\\frac{\\pi},{6},', 'answer': '\\frac{1},{2},'},
{'number': '86', 'level': 'easy', 'latex': '5^2+6^2', 'answer': '61'},
{'number': '89', 'level': 'easy', 'latex': '8^2-4^3', 'answer': '0'},
{'number': '87', 'level': 'easy', 'latex': '3^2+4^2', 'answer': '25'},
{'number': '84', 'level': 'easy', 'latex': '2^4', 'answer': '16'},
{'number': '76', 'level': 'easy', 'latex': '2^2', 'answer': '4'},
{'number': '80', 'level': 'easy', 'latex': '3^4', 'answer': '81'},
{'number': '85', 'level': 'easy', 'latex': '1^{100},', 'answer': '1'},
{'number': '90', 'level': 'easy', 'latex': '1+3^2', 'answer': '10'},
{'number': '83', 'level': 'easy', 'latex': '4^4', 'answer': '256'},
{'number': '88', 'level': 'easy', 'latex': '10^2-9^2', 'answer': '19'},
{'number': '77', 'level': 'easy', 'latex': '2^3', 'answer': '8'},
{'number': '82', 'level': 'easy', 'latex': '4^3', 'answer': '64'},
{'number': '78', 'level': 'easy', 'latex': '3^2', 'answer': '9'},
{'number': '79', 'level': 'easy', 'latex': '3^3', 'answer': '27'},
{'number': '81', 'level': 'easy', 'latex': '4^2', 'answer': '16'},
{'number': '2', 'level': 'easy', 'latex': '2+3', 'answer': '5'},
{'number': '12', 'level': 'easy', 'latex': '71+9', 'answer': '80'},
{'number': '9', 'level': 'easy', 'latex': '5+6', 'answer': '11'},
{'number': '1', 'level': 'easy', 'latex': '1+1', 'answer': '2'},
{'number': '13', 'level': 'easy', 'latex': '99+1', 'answer': '100'},
{'number': '4', 'level': 'easy', 'latex': '25+6', 'answer': '31'},
{'number': '3', 'level': 'easy', 'latex': '12+33', 'answer': '45'},
{'number': '14', 'level': 'easy', 'latex': '123+321', 'answer': '444'},
{'number': '10', 'level': 'easy', 'latex': '4+7', 'answer': '11'},
{'number': '11', 'level': 'easy', 'latex': '8+9', 'answer': '17'},
{'number': '18', 'level': 'easy', 'latex': '71-9', 'answer': '62'},
{'number': '17', 'level': 'easy', 'latex': '9-8', 'answer': '1'},
{'number': '8', 'level': 'easy', 'latex': '25-6', 'answer': '19'},
{'number': '19', 'level': 'easy', 'latex': '99-1', 'answer': '98'},
{'number': '15', 'level': 'easy', 'latex': '6-5', 'answer': '1'},
{'number': '16', 'level': 'easy', 'latex': '7-4', 'answer': '3'},
{'number': '5', 'level': 'easy', 'latex': '2-1', 'answer': '1'},
{'number': '6', 'level': 'easy', 'latex': '4-3', 'answer': '1'},
{'number': '7', 'level': 'easy', 'latex': '33-12', 'answer': '21'},
{'number': '20', 'level': 'easy', 'latex': '321-123', 'answer': '198'},
{'number': '116', 'level': 'easy', 'latex': '(x^2)=1', 'answer': '[-1,1]'},
{'number': '119', 'level': 'easy', 'latex': '(x^2)=16', 'answer': '[-4,4]'},
{'number': '118', 'level': 'easy', 'latex': '(x^2)=9', 'answer': '[-3,3]'},
{'number': '125', 'level': 'easy', 'latex': '(2x^2)-3x+1=0', 'answer': '[\\frac{1},{2},,1]'},
{'number': '123', 'level': 'easy', 'latex': '(4x^2)=16', 'answer': '[-2,2]'},
{'number': '124', 'level': 'easy', 'latex': '(x^2)-4x+3=0', 'answer': '[1,3]'},
{'number': '120', 'level': 'easy', 'latex': '(x^2)=25', 'answer': '[-5,5]'},
{'number': '121', 'level': 'easy', 'latex': '(x^2)+2x+1=0', 'answer': '[-1]'},
{'number': '117', 'level': 'easy', 'latex': '(x^2)=4', 'answer': '[-2,2]'},
{'number': '122', 'level': 'easy', 'latex': '(x^2)-2x+1=0', 'answer': '[1]'},
{'number': '139', 'level': 'easy', 'latex': '\\lim_{x\\to0},\\cosx', 'answer': '1'},
{'number': '140', 'level': 'easy', 'latex': '\\lim_{x\\to0},\\sinx', 'answer': '0'},
{'number': '137', 'level': 'easy', 'latex': '\\lim_{x\\to\\infty},\\frac{1},{x},', 'answer': '0'},
{'number': '138', 'level': 'easy', 'latex': '\\lim_{x\\to0},\\frac{\\sinx},{x},', 'answer': '1'},
{'number': '136', 'level': 'easy', 'latex': '\\lim_{x\\to0},x', 'answer': '0'}
]
# print([x for x in answer if x['number']=='1'])
# answer.sort(key=lambda x:int(x['number']))
# print(answer)
print(os.listdir(TEST_URL))
test_url = [x for x in os.listdir(TEST_URL) if x!='example' and x !='.DS_Store']
print(test_url)
evaluation_results = []
latex_cnt = 0
answer_cnt = 0

for u in  test_url:
    url = os.path.join(TEST_URL,u)
    test_imgs = os.listdir(url)

    for img in test_imgs:
        file_type = img.split('.')[-1]
        if file_type == 'jpg' or file_type == 'png':
            # 测试这张图片能否进行正确处理
            file_url = os.path.join(url,img)
            file_inf = img.split('.')[0]
            # print(file_inf)
            # print([x for x in answer if x['number'] == file_inf])
            file_inf = [x for x in answer if x['number'] == file_inf][0]
            # print(file_inf)
            img_number = file_inf['number']
            img_level = file_inf['level']
            img_latex = file_inf['latex']
            img_answer = file_inf['answer']
            # img_number,img_level,img_latex,img_answer = file_inf
            # print(img_number,img_level,img_latex,img_answer)
            is_error = false
            # evaluation_result = {'number':img_number,'level':img_level,'latex':img_latex,'answer':img_answer}
            # print(file_url)
            evaluation_result = file_inf
            err_msg = ''
            try:
                test_latex,test_result = solve(file_url,'test')
            except BaseException as e:
                # print(e)
                err_msg = repr(e)
                is_error = True
            finally:
                if is_error:
                    evaluation_result['is_error'] = True
                    evaluation_result['err_msg'] = err_msg
                else:
                    # print(latex,result)
                    evaluation_result['test_latex'] = test_latex
                    evaluation_result['test_answer'] = str(test_result).replace(' ','')

                    if test_latex == img_latex:
                        latex_cnt = latex_cnt + 1
                    if img_answer == evaluation_result['test_answer']:
                        answer_cnt = answer_cnt + 1
                    if test_latex != img_latex or img_answer != evaluation_result['test_answer']:
                        evaluation_result['is_wrong'] = 'yes'
                evaluation_results.append(evaluation_result)
for item in evaluation_results:
    print(item)
number_of_problems = len(evaluation_results)
print('一共测试了'+str(number_of_problems)+'道题')
latex_ratio = latex_cnt/float(number_of_problems)
answer_ratio = answer_cnt/float(number_of_problems)
print('做对题数',answer_cnt)
print('latex ratio:',latex_ratio,';answer_ratio:',answer_ratio)
