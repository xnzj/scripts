# -*- coding: utf-8 -*-

import os
import subprocess
from config import config
import re
from collections import Counter

# 把路由地址转换成驼峰命名
def url_to_camel_case(url_path):
    # 分割URL路径
    parts = url_path.split('/')
    
    # 将每个部分的首字母大写
    camel_case_parts = [part.title() for part in parts]
    
    # 合并部分
    camel_case_url = ''.join(camel_case_parts)
    
    return camel_case_url

# 把 routePath 分割成数组，然后判断哪些路由文件名包含这些数组中的元素，忽略大小写，然后比较这些文件的大小，找出最大的那个文件
def guessRouteFile(routePath, route_files, routes_path):
    parts = routePath.split('/')
    # filter out empty string
    parts = list(filter(lambda part: part != '', parts))
    max_length = 0
    max_length_file = ''
    for file in route_files:
        for part in parts:
            if part.lower() in file.lower():
                file_path = os.path.join(routes_path, file)
                file_size = os.path.getsize(file_path)
                if file_size > max_length:
                    max_length = file_size
                    max_length_file = file
    return max_length_file

def guessServiceFile(routes_path, route_file):
    file_path = os.path.join(routes_path, route_file)
    word_freq = extract_word_frequency(file_path)
    # 找出词频最高并且包含 Service 的单词
    service_word = ''
    max_freq = 0
    for word, freq in word_freq.items():
        if 'Service' in word and freq > max_freq:
            service_word = word + '.js'
            max_freq = freq
            
    return service_word

def extract_word_frequency(file_path):
    # 打开文件并读取内容
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        text = file.read()
    # 使用正则表达式分词
    words = re.findall(r'\b\w+\b', text)  # 转换为小写并提取单词
    # 统计词频
    word_freq = Counter(words)

    return word_freq
    
def main(config=config):
        
    config = config['cp_code_gen']

    project_path = config['project_path']
    routes_path = project_path + config['route_path']
    services_path = project_path + config['service_path']

    # 输入路由：GET /api/v1/user
    route = input('请输入路由：')
    # 把路由按空格分割成两部分
    method, routePath = route.split(' ')
    method = method.lower()
    # 判断 method 是否合法
    if method not in ['get', 'post']:
        print('method 不合法')
        exit()

    # 判断 routePath 是否为空
    if routePath == '':
        print('routePath 不能为空')
        exit()
    # 判断 routePath 是否以 / 开头
    if routePath[0] != '/':
        routePath = '/' + routePath



    serviceMethod = url_to_camel_case(routePath)

    print(method, routePath, serviceMethod)

    route_files = []
    for root, dirs, files in os.walk(routes_path):
        for file in files:
            if file.endswith('.js'):
                route_files.append(file)


    route_file = guessRouteFile(routePath, route_files, routes_path)
    if (route_file != ''):
        print('猜测的路由文件：', route_file)
        confirm = input('是否正确？(y/n, default y): ')
        if confirm.lower() == 'n':
            route_file = ''
    if route_file == '':    
        # 把所有的路由文件列出来，加上编号，让用户选择
        print('路由文件列表：')
        for i, file in enumerate(route_files):
            print(f'{i+1}. {file}')

        # 用户选择一个路由文件
        route_file = input('请选择一个文件(默认 common.js): ')
        # 如果没有输入，就默认 common.js
        if route_file == '':
            route_file = 'common.js'
        else:
            route_file_index = int(route_file) - 1
            route_file = route_files[route_file_index]

    service_file = guessServiceFile(routes_path, route_file)
    
    if (service_file != ''):
        print('猜测的 service 文件：', service_file)
        confirm = input('是否正确？(y/n, default y): ')
        if confirm.lower() == 'n':
            service_file = ''
    # 检查 service 文件是否存在
    service_file_path = os.path.join(services_path, service_file)
    if not os.path.exists(service_file_path):
        print('service 文件不存在')
        exit()
    
    if service_file == '':
        # 列出 cp 的所有 service 文件，以便确认方法要写到哪个文件中
        service_files = []
        for root, dirs, files in os.walk(services_path):
            for file in files:
                if file.endswith('.js'):
                    service_files.append(file)

        # 把所有的 service 文件列出来，加上编号，让用户选择
        print('service 文件列表：')
        for i, file in enumerate(service_files):
            print(f'{i+1}. {file}')

        # 用户选择一个 service 文件
        service_file = input('请选择一个文件(默认 CommonService.js): ')
        # 如果没有输入，就默认 CommonService.js
        if service_file == '':
            service_file = 'CommonService.js'
        else:
            service_file_index = int(service_file) - 1
            service_file = service_files[service_file_index]

    # 2. 生成路由文件的代码
    # 打印文件内容，加上行号
    with open(os.path.join(routes_path, route_file), 'r', encoding='utf-8', errors='ignore') as f:
        print(f'路由文件 {route_file} 的内容：')
        lines = f.readlines()
        for i, line in enumerate(lines):
            # 判断 Line 的内容是否包含 router，如果包含，就打印出来
            if 'router.' in line:
                print(f'{i}. {line}', end='')
    print('\n')
    # 用户输入路由代码的位置
    line_number = int(input('请输入路由代码的位置：'))
    # 读取路由模板文件
    with open('./templates/cpMiddlewareRouteTemplate.txt', 'r', encoding='utf-8') as f:
        route_template = f.read()
    # 把模板文件中的变量替换成用户输入的内容，变量有 {{method}} {{routePath}} {{service}} {{serviceMethod}}，然后写入文件
    route_code = route_template.replace('{{method}}', method).replace('{{routePath}}', routePath).replace('{{serviceName}}', service_file.split('.')[0]).replace('{{serviceMethod}}', serviceMethod)
    # 判断用户输入的行号是否合法
    if line_number < 0 or line_number > len(lines):
        print('行号不合法')
        exit()
    # 判断用户输入的行号的上一行是否是空行，如果不是，就在模板内容上面插入一个空行
    if lines[line_number-1].strip() != '':
        route_code = '\n' + route_code
        print("开头添加了一个空行")
    # 判断用户输入的行号的下一行是否是空行，如果不是，就在模板内容下面插入一个空行
    if lines[line_number+1].strip() != '':
        route_code = route_code + '\n'
        print("末尾添加了一个空行")
    # 把模板内容插入到文件中
    lines.insert(line_number, route_code)
    # 写入文件
    with open(os.path.join(routes_path, route_file), 'w', encoding='utf-8') as f:
        f.writelines(lines)
    # 使用 code-insiders 命令行工具打开路由文件
    # subprocess.run(['code-insiders.cmd', os.path.join(routes_path, route_file)])

    # 打印 service 文件内容，加上行号
    with open(os.path.join(services_path, service_file), 'r', encoding='utf-8') as f:
        print(f'service 文件 {service_file} 的内容：')
        lines = f.readlines()
        for i, line in enumerate(lines):
            if 'async' in line and 'function' in line:
                print(f'{i}. {line}', end='')
            # 如果 line 只包含方法名和逗号, 使用正则表达式匹配
            if re.match(r'\s+\w+,\n', line):
                print(f'{i}. {line}', end='')
            
    # 用户输入 service 方法的位置
    line_number2 = int(input('请输入 service return 方法的位置：'))
    line_number = int(input('请输入 service 方法的位置：'))
    # 读取 service 方法模板文件
    with open('./templates/cpMiddlewareServiceMethodTemplate.txt', 'r', encoding='utf-8') as f:
        service_method_template = f.read()
    # 把模板文件中的变量替换成用户输入的内容，变量有 {{method}} {{routePath}} {{serviceMethod}}，然后写入文件
    service_method_code = service_method_template.replace('{{method}}', method).replace('{{routePath}}', routePath).replace('{{serviceMethod}}', serviceMethod)
    # 判断用户输入的行号是否合法
    if line_number < 0 or line_number > len(lines):
        print('行号不合法')
        exit()
    # 判断用户输入的行号的上一行是否是空行，如果不是，就在模板内容上面插入一个空行
    if lines[line_number-1].strip() != '':
        service_method_code = '\n' + service_method_code
        print("开头添加了一个空行")
    # 判断用户输入的行号的下一行是否是空行，如果不是，就在模板内容下面插入一个空行
    if lines[line_number+1].strip() != '':
        service_method_code = service_method_code + '\n'
        print("末尾添加了一个空行")
    # 把模板内容插入到文件中
    lines.insert(line_number2, '        ' + serviceMethod + ',\n')
    lines.insert(line_number, service_method_code)
    # 写入文件
    with open(os.path.join(services_path, service_file), 'w', encoding='utf-8') as f:
        f.writelines(lines)
    # 使用 code-insiders 命令行工具打开 service 文件
    subprocess.run(['code-insiders.cmd', os.path.join(services_path, service_file)])

if __name__ == '__main__':
    main()