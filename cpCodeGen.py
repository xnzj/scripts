# 1. 列出 cp 这个项目的所有路由文件，以便确认路由要写到哪个文件中
# 2. 生成路由文件的代码
# 3. 列出 cp 的所有 service 文件，以便确认方法要写到哪个文件中
# 4. 生成 service 文件的代码
import os
import subprocess
from config import config

config = config['cp_code_gen']

project_path = config['project_path']
routes_path = project_path + config['route_path']
services_path = project_path + config['service_path']

# 输入 get/post 还有路由地址
method = input('请输入请求方法(默认 post): ')
if method == '':
    method = 'post'
# method 是否合法
method = method.lower()
if method not in ['get', 'post']:
    print('请求方法不合法')
    exit()

# 输入路由地址
routePath = input('请输入路由地址：')
if routePath == '':
    print('路由地址不能为空')
    exit()
# routePath 是否以 / 开头，如果没有，就加上
print(routePath[0])
if routePath[0] != '/':
    routePath = '/' + routePath

# 把路由地址转换成驼峰命名
def url_to_camel_case(url_path):
    # 分割URL路径
    parts = url_path.split('/')
    
    # 将每个部分的首字母大写
    camel_case_parts = [part.title() for part in parts]
    
    # 合并部分
    camel_case_url = ''.join(camel_case_parts)
    
    return camel_case_url

serviceMethod = url_to_camel_case(routePath)

print(method, routePath, serviceMethod)

# 1. 列出 cp 这个项目的所有路由文件，以便确认路由要写到哪个文件中,这是一个 js 项目
route_files = []
for root, dirs, files in os.walk(routes_path):
    for file in files:
        if file.endswith('.js'):
            route_files.append(file)

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
with open(os.path.join(routes_path, route_file), 'r') as f:
    print(f'路由文件 {route_file} 的内容：')
    lines = f.readlines()
    for i, line in enumerate(lines):
        print(f'{i}. {line}', end='')

# 用户输入路由代码的位置
line_number = int(input('请输入路由代码的位置：'))
# 读取路由模板文件
with open('./templates/cpMiddlewareRouteTemplate.txt', 'r') as f:
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
with open(os.path.join(routes_path, route_file), 'w') as f:
    f.writelines(lines)
# 使用 code-insiders 命令行工具打开路由文件
# subprocess.run(['code-insiders.cmd', os.path.join(routes_path, route_file)])

# 打印 service 文件内容，加上行号
with open(os.path.join(services_path, service_file), 'r') as f:
    print(f'service 文件 {service_file} 的内容：')
    lines = f.readlines()
    for i, line in enumerate(lines):
        print(f'{i}. {line}', end='')
# 用户输入 service 方法的位置
line_number = int(input('请输入 service 方法的位置：'))
line_number2 = int(input('请输入 service return 方法的位置：'))
# 读取 service 方法模板文件
with open('./templates/cpMiddlewareServiceMethodTemplate.txt', 'r') as f:
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
with open(os.path.join(services_path, service_file), 'w') as f:
    f.writelines(lines)
# 使用 code-insiders 命令行工具打开 service 文件
subprocess.run(['code-insiders.cmd', os.path.join(services_path, service_file)])