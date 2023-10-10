import pyperclip

# 获取剪贴板内容
clipboard_text = pyperclip.paste()

# 转换为大写
uppercase_text = clipboard_text.lower()

# 将大写文本放回剪贴板
pyperclip.copy(uppercase_text)
