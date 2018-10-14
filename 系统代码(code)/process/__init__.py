from scan import get_token
import tensorflow as tf
import tools
import config
# from outlier_detector import *
# 识别非黏连的字符，比如i、=、除号
def detect_uncontinous_symbols(symbols,original_img):
    # 先对symbols垂直投影
    # 然后垂直投影
    for projection_type in range(1):
        projection = tools.get_projection(symbols,projection_type)
        # print('projection',projection)
        # 根据投影对symbols进行分割
        # 对于每一个分割，获得在这个分割里面的symbols
        locations = [x['location'] for x in symbols]
        end_index = 0
        for line_segment in projection:
            # 确定属于line_segment的symbols
            start_index = end_index
            for end_index in range(start_index, len(locations)):
                x11, x12 = locations[end_index][projection_type], locations[end_index][projection_type] + locations[end_index][projection_type + 2]
                x21, x22 = line_segment[0], line_segment[1]
                if (x11 >= x21 and x12 <= x22):
                    end_index += 1
                else:
                    break
            # 截取characters[start_index:end_index],如果长度大于1，继续递归调用sort_characters排序
            location_segment = locations[start_index:end_index]
            symbol_segment = symbols[start_index:end_index]
            sub_symbol = [x['src_img'] for x in symbol_segment]
            # print('切割后的location', location_segment)
            # print(symbol_segment)
            # 如果一个分割的长度大于1，小于3，就送到分类器进行识别
            if (len(location_segment) > 1 and len(location_segment)<4):

                location = tools.join_locations(location_segment)
                # 从原图提取待识别的图片
                extracted_img = tools.extract_img(location,original_img)
                # 识别字符 这里每次都需要calling model，可以进一步优化
                predict_input_fn = tf.estimator.inputs.numpy_input_fn(
                    x={"x":tools.normalize_matrix_value([extracted_img]+sub_symbol)},
                    shuffle=False)
                predictions = tools.cnn_symbol_classifier.predict(input_fn=predict_input_fn)
                characters = []
                for i, p in enumerate(predictions):
                    # print(p['classes'],FILELIST[p['classes']])
                    candidates = tools.get_candidates(p['probabilities'])
                    characters.append({'candidates': candidates})
                # print('detect uncontinuous symbols',characters)
                # 如果识别出候选的匹配字符中存在非连续字符，即作为一个整体
                for candidate in characters[0]['candidates']:
                    recognized_symbol = candidate['symbol']
                    probability = candidate['probability']

                    # 如果是非黏连字符,且有半成把握认为是正确的,则合并它们作为一个整体，返回合并后的symbols
                    if recognized_symbol in config.UNCONTINOUS_SYMBOLS and probability>0.5:
                        # print('yesssssss',characters[2]['candidates'][0]['symbol'],characters[1]['candidates'][0]['symbol'].isdigit(),characters[3]['candidates'][0]['symbol'].isdigit())
                        # 除号必须有三个字符构成，还要判断子字符包不包含数字，如果包含数字，则不能合并为整体
                        if recognized_symbol == 'div' and len(characters) == 4 and \
                                characters[2]['candidates'][0]['symbol'] in ['-',',','point'] and \
                                characters[1]['candidates'][0]['symbol'].isdigit() == False and \
                                characters[3]['candidates'][0]['symbol'].isdigit() == False:
                            joined_symbol = {'location': location, 'src_img': extracted_img}

                            for i in range(end_index - start_index):
                                symbols.remove(symbols[start_index])
                                locations.remove(locations[start_index])
                            symbols.insert(start_index, joined_symbol)
                            locations.insert(start_index, location)
                            end_index = start_index + 1
                            break
                        # 等于号的两个子字符必须是-
                        elif recognized_symbol == '=' and len(characters) == 3 and \
                                characters[2]['candidates'][0]['symbol'] in ['-',',','point'] and \
                                characters[1]['candidates'][0]['symbol'] in ['-',',','point']:
                            joined_symbol = {'location': location, 'src_img': extracted_img}
                            for i in range(end_index - start_index):
                                symbols.remove(symbols[start_index])
                                locations.remove(locations[start_index])
                            symbols.insert(start_index, joined_symbol)
                            locations.insert(start_index, location)
                            end_index = start_index + 1
                            break
                        # 等于号的两个子字符必须是-
                        elif recognized_symbol == 'rightarrow' and len(characters) == 3 and \
                             characters[2]['candidates'][0]['symbol'] in [')', '>'] and \
                             characters[1]['candidates'][0]['symbol'] in ['-', ',', 'point']:
                            joined_symbol = {'location': location, 'src_img': extracted_img}
                            for i in range(end_index - start_index):
                                symbols.remove(symbols[start_index])
                                locations.remove(locations[start_index])
                            symbols.insert(start_index, joined_symbol)
                            locations.insert(start_index, location)
                            end_index = start_index + 1
                            break
    return symbols

# 识别常见的数学函数名，目前默认所有数学函数名都是由三个分散的符号组成
# sin/cos/log
def detect_functions(symbols,original_img):
    sub_symbol_cnt = 3
    for j in range(2):
        stride = sub_symbol_cnt-j

        length = len(symbols)
        i = 0
        t_symbols = []
        locations = [x['location'] for x in symbols]
        while i<length-stride+1:
            location = tools.join_locations(locations[i:i+stride])
            segment_img = tools.extract_img(location,original_img)
            segment = {'src_img':segment_img,'start_index':i,'end_index':i+3,'location':location}
            t_symbols.append(segment)
            i = i+1
        # print([x['start_index'] for x in t_symbols])
        img_to_predict = [x['src_img'] for x in t_symbols]
        # 识别字符 这里每次都需要calling model，可以进一步优化
        predict_input_fn = tf.estimator.inputs.numpy_input_fn(
            x={"x": tools.normalize_matrix_value(img_to_predict)},
            shuffle=False)
        predictions = tools.cnn_symbol_classifier.predict(input_fn=predict_input_fn)
        characters = []
        for i, p in enumerate(predictions):
            candidates = tools.get_candidates(p['probabilities'])
            characters.append(candidates[0])
        # print(characters)
        length = len(t_symbols)
        i = 0
        shift = 0

        while i<length:
            # 如果识别结果是函数，则替换为一个整体
            if characters[i]['symbol'] in config.FUNCTION and characters[i]['probability'] >0.9:
                start_index = t_symbols[i]['start_index']
                end_index = t_symbols[i]['end_index']
                # print('detect function',i,start_index,end_index,shift)
                start_index = start_index - shift
                end_index = end_index - shift
                for j in range(end_index - start_index):
                    symbols.remove(symbols[start_index])
                symbols.insert(start_index, t_symbols[i])
                shift = shift + end_index-start_index-1
                if i+2 < length:
                    i = i+2
                elif i+1 < length:
                    i = i+1

            i = i+1
    return symbols


# 将一个个独立的字符识别成token序列，也是具备二维空间结构的数学公式转成一维token序列的具体实现
# 这是一个很重要的函数，它将上下标，积分的空间关系一维化
def group_into_tokens(characters):
    tokens = []
    next_index = 0

    while(next_index < len(characters)):

        token,next_index = get_token(characters,next_index)
        tokens.append(token)
    return tokens