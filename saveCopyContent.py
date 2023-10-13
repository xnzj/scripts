import os
import datetime
import pyperclip

# 获取当前日期和时间
current_datetime = datetime.datetime.now()
ymdhis = current_datetime.strftime('%Y%m%d%H%M%S')

# 创建文件名
file_name = f'file_{ymdhis}.txt'

# 获取 Downloads 目录的路径
downloads_dir = os.path.expanduser('~/Downloads')

# 构建完整的文件路径
file_path = os.path.join(downloads_dir, file_name)

# 获取剪贴板内容
copied_content = pyperclip.paste()

# 将内容写入文件
with open(file_path, 'w') as file:
    file.write(copied_content)

print(f'剪贴板内容已成功写入到 {file_path}')
