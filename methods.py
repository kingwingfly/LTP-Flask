import torch
from ltp import LTP
import os
import shutil
from time import time, asctime
import asyncio


device = torch.device('cuda:0') if torch.cuda.is_available() else 'cpu'
workspace = os.path.dirname(__file__)

zh_tasks = {
    'cws': '分词',
    'pos': '词性',
    'ner': '命名实体',
    'srl': '语义角色',
    'dep': '依存句法',
    'sdp': '语义依存',
}


def generate_lst(path):
    lst = []
    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith('.txt'):
                file = os.path.join(dirpath, filename)
                with open(file, 'r', encoding='utf-8') as f:
                    print(f'Reading {file}')
                    lst.append(f.read())
    return lst


def save_results(output):
    asctime_now = asctime()
    # ['Sat', 'Nov', '19', '17:42:42', '2022']
    output_dir = os.path.join(workspace, 'output', asctime_now.replace(':', '-'))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for task, result in output.items():
        print('\n', task, '\n' , result, '-'*50)
        filename = os.path.join(output_dir, f'{task}_output.txt')
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(str(result))

def dnnMethod(dirpath, tasks, queue):
    ltp = LTP(os.path.join(workspace, 'data', 'base2'))  # 默认加载 Small 模型
    # 将模型移动到 GPU 上
    ltp.to(device)
    output = ltp.pipeline(generate_lst(dirpath), tasks=tasks)
    # 使用字典格式作为返回结果
    # print(output.cws)  # print(output[0]) / print(output['cws']) # 也可以使用下标访问
    # print(output.pos)
    # print(output.ner)
    save_results(output)
    queue.put(True)


def svmMethod(dirpath, tasks, queue):
    # 使用感知机算法实现的分词、词性和命名实体识别，速度比较快，但是精度略低
    ltp = LTP(os.path.join(workspace, 'data', 'legacy'))
    output = ltp.pipeline(generate_lst(dirpath), tasks=tasks)
    # cws, pos, ner = ltp.pipeline(['他叫汤姆去拿外衣。'], tasks=['cws', 'ner']).to_tuple() # error: NER 需要 词性标注任务的结果
    '''
    print(cws, pos, ner)
    cws, pos, ner = ltp.pipeline(
        generate_lst(dirpath), tasks=tasks
    ).to_tuple()  # to tuple 可以自动转换为元组格式
    # 使用元组格式作为返回结果
    print(cws, pos, ner)
    '''
    save_results(output)
    queue.put(True)


if __name__ == '__main__':
    path = './example'
    tasks = ['cws', 'pos', 'ner']
    svmMethod(path, tasks)
