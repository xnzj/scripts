import clipboard

# 获取剪贴板内容
clipboard_text = clipboard.paste()

# 将剪贴板文本分割成行，并去除前后空格
lines = [line.strip() for line in clipboard_text.splitlines()]

# 在每一行前后添加双引号和逗号
formatted_lines = ['"{0}",'.format(line) for line in lines]

# 将格式化后的行合并成一个字符串，一行一项
result = '\n'.join(formatted_lines)

# 去除最后一行的逗号
result = result.rstrip(',')

# 将结果复制到剪贴板
clipboard.copy(result)
