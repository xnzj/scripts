# 显示当前目录下所有以 .bat 结尾的文件名称

import os

for file in os.listdir('.'):
    if file.endswith('.bat'):
        print(file)