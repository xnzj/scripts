'''
这个脚本接收两个参数，两个参数都是逗号分隔的字符串，转换成数组，返回第一个数组中有而第二个数组中没有的元素
'''
import sys

def arrayDiff(a, b):
    return [item for item in a if item not in b]

if len(sys.argv) < 3:
    print('Usage: python arrayDiff.py a b')
    exit()

a = sys.argv[1].split(',')
b = sys.argv[2].split(',')
result = arrayDiff(a, b)

print(result)
