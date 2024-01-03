import os

# 获取当前文件所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))

for file in os.listdir(current_dir):
    if file.endswith('.bat'):
        # 去掉文件名中的 .bat 后缀
        file_name = file[:-4]
        print(file_name)