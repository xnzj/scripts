import csv
import json
import os
import datetime
import clipboard

# JSON 数据
json_data = json.loads(clipboard.paste())

# json_data 是否为字典
if isinstance(json_data, dict):
    json_data = [json_data]

# CSV 文件路径
downloads_dir = os.path.expanduser('~/Downloads')
current_datetime = datetime.datetime.now()
ymdhis = current_datetime.strftime('%Y%m%d%H%M%S')
filename = f'json2csv_{ymdhis}.csv'
csv_file_path = os.path.join(downloads_dir, filename)

# 写入 CSV 文件
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    # 创建 CSV writer 对象
    csv_writer = csv.writer(csv_file)

    # 写入 CSV 头部
    header = json_data[0].keys()
    csv_writer.writerow(header)

    # 写入 JSON 数据
    for row in json_data:
        csv_writer.writerow(row.values())

print(f'CSV 文件已保存到 {csv_file_path}')

