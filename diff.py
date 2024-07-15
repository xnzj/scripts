import pyperclip
import keyboard
import time
import subprocess
import os

clipboard_history = []

def on_copied():
    copied_text = pyperclip.paste()
    clipboard_history.append(copied_text)

def compare_and_show_diff(file1_content, file2_content):
    # 保存内容到临时文件
    user_home = os.path.expanduser('~')
    file1_path = os.path.join(user_home, 'Downloads', 'diff1.txt')
    file2_path = os.path.join(user_home, 'Downloads', 'diff2.txt')
    with open(file1_path, 'w', encoding='utf-8') as file1:
        file1.write(file1_content)
    
    with open(file2_path, 'w', encoding='utf-8') as file2:
        file2.write(file2_content)

    # 使用 code 命令行工具打开 Diff
    subprocess.run(['code-insiders.cmd', '--diff', file1_path, file2_path])

print('复制两个需要比较的字符串，然后 ctrl + c，即可打开 Diff 工具比较两个字符串的差异')

keyboard.add_hotkey('ctrl+c', on_copied)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    keyboard.unhook_all()
    # 获取最后 2 个剪贴板内容
    last_two = clipboard_history[-2:]
    # 比较并显示差异
    compare_and_show_diff(last_two[0], last_two[1])
