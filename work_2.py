import math
import os
import jieba

def load_filter_chars(file_path):
    filter_chars = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()  # 去除行末尾的换行符
            if line:  # 确保不是空行
                filter_chars.append(line)
    return filter_chars

def calculate_entropy(text, unit='char', filter_chars=None):
    frequencies = {}
    total_count = 0

    # 根据 unit 参数决定以汉字、词语或字符为单位进行处理
    if unit == 'char':
        # 将文本拆分为单个字符，并过滤掉特定字符
        tokens = [char for char in text if char not in filter_chars]
    elif unit == 'word':
        # 中文分词，并过滤掉特定字符
        tokens = [word for word in jieba.lcut(text) if word not in filter_chars]
    else:
        raise ValueError("Invalid unit. Please choose 'char' or 'word'.")

    # 统计频率
    for token in tokens:
        frequencies[token] = frequencies.get(token, 0) + 1
        total_count += 1

    # 计算信息熵
    entropy = 0
    for count in frequencies.values():
        probability = count / total_count
        entropy -= probability * math.log2(probability)

    return entropy

def process_folder(folder_path, filter_file):
    filter_chars = load_filter_chars(filter_file)
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='gb18030') as f:
                    text = f.read()
                    char_entropy = calculate_entropy(text, unit='char', filter_chars=filter_chars)
                    word_entropy = calculate_entropy(text, unit='word', filter_chars=filter_chars)
                    print(f"文件: {file_path}")
                    print("以字符为单位的平均信息熵:", char_entropy)
                    print("以词为单位的平均信息熵:", word_entropy)
                    print()

# 指定文件夹路径和过滤文件路径
folder_path = './Chinese_data'
filter_file = './cn_stopwords.txt'

# 处理文件夹中的文本文件
process_folder(folder_path, filter_file)