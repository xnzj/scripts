import os
import sys

# 获取当前脚本文件的绝对路径
current_script = os.path.abspath(sys.argv[0])

# 获取当前脚本文件所在的目录
script_directory = os.path.dirname(current_script)

# 指定要检查的目录路径
directory_path = script_directory

# 使用os.listdir()获取目录中的所有文件
files = os.listdir(directory_path)

# 使用os.path.getctime()函数获取文件的创建时间，然后根据创建时间排序文件
files.sort(key=lambda x: os.path.getctime(os.path.join(directory_path, x)), reverse=True)

# 获取最新创建的文件名
if files:
    newest_file_name = files[0]
    # 获取文件名后缀
    file_extension = os.path.splitext(newest_file_name)[1]
    # 如果文件后缀名不是 .py 则退出程序
    if file_extension != '.py':
        print('目录中最新的文件不是 .py 文件')
        sys.exit()
    # 把文件后缀名替换为 .bat
    bat_file_name = newest_file_name.replace(file_extension, '.bat')
    # 读取模板文件
    with open(os.path.join(directory_path, 'bat.template'), 'r') as template_file:
        template_content = template_file.read()
        # 替换模板文件中的占位符 {file_name} 为最新创建的文件名
        content = template_content.replace('{filename}', newest_file_name)
        # 将替换后的内容写入到新文件中
        with open(os.path.join(directory_path, bat_file_name), 'w') as new_file:
            new_file.write(content)
            print(f'已成功创建 {bat_file_name} 文件')
            print(f'文件内容为：\n{content}')
else:
    print("目录中没有文件")

