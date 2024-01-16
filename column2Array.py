import clipboard
import json

# 获取剪贴板内容
clipboard_text = clipboard.paste()

# 将剪贴板文本分割成行，并去除前后空格
lines = [line.strip() for line in clipboard_text.splitlines()]

# 移除空行
lines = [line for line in lines if line]

# 判断每一行是否都是数字
if all(line.isnumeric() for line in lines):
    # 将每一行转换为 int 类型
    lines = [int(line) for line in lines]
else:
    # 给 lines 中每一个元素添加引号
    lines = ["{0}".format(line) for line in lines]

# 把 lines 转换为 json 字符串, 每一行前后的单引号替换为双引号
result = json.dumps(lines)
print(result)

# 将结果复制到剪贴板
clipboard.copy(result)
