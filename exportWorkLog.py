import pymysql
import argparse
import pyperclip  # 用于复制到剪贴板
from config import config
from datetime import datetime


def fetch_tasks_by_tag(tag):
    # 从配置文件中获取数据库连接信息
    db_config = config['local_mysql']
    connection = pymysql.connect(
        host=db_config['host'],
        port=int(db_config['port']),
        user=db_config['username'],
        password=db_config['password'],
        db='automation',  # 数据库名称
    )
    
    grouped_tasks = {}  # 用于按 tag2 分组任务
    total_duration = 0  # 计算总耗时
    group_durations = {}  # 计算每个组的总耗时
    
    try:
        with connection.cursor() as cursor:
            # 根据输入的 tag 从 tasks 表中查询数据
            query = "SELECT * FROM tasks WHERE tag1 = %s"
            cursor.execute(query, (tag,))
            results = cursor.fetchall()

            # 按 tag2 分组
            for row in results:
                task_id, title, desc, tag1, tag2, tag3, created_at, updated_at, end_at = row
                
                # 如果 tag2 是 None 或空字符串，将其归为 "main"
                if not tag2:
                    tag2 = tag1 + " 主 ticket"
                
                # 如果 tag2 不在字典中，初始化为一个空列表
                if tag2 not in grouped_tasks:
                    grouped_tasks[tag2] = []
                
                # 将当前任务加入对应的 tag2 组
                grouped_tasks[tag2].append({
                    "id": task_id,
                    "title": title,
                    "desc": desc,
                    "created_at": created_at,
                    "end_at": end_at,
                    "duration": (end_at - created_at).total_seconds() / 3600 if end_at else None,
                })
                
                # 计算总耗时
                if end_at:
                    duration = (end_at - created_at).total_seconds() / 3600
                    total_duration += duration
                    
                    # 计算每个组的总耗时
                    if tag2 not in group_durations:
                        group_durations[tag2] = 0
                    group_durations[tag2] += duration

            # 构建输出内容
            output = []
            i = 0
            for tag, tasks in grouped_tasks.items():
                i += 1
                output.append("=" * 10)  # 每个组之间用十个等号隔开
                output.append(f"Group {i}: {tag}")
                group_total_duration = group_durations.get(tag, 0)  # 每个组的总耗时
                output.append(f"总耗时：{group_total_duration:.2f} 小时")
                output.append("")
                
                for index, task in enumerate(tasks, start=1):
                    start_time = task['created_at'].strftime('%Y-%m-%d %H:%M:%S')
                    end_time = task['end_at'].strftime('%Y-%m-%d %H:%M:%S') if task['end_at'] else "未定义"
                    duration = task['duration']
                    
                    output.append(f"{index}.")
                    output.append(f"开始：{start_time}")
                    output.append(f"*{task['title']}*")
                    
                    if task['desc']:
                        output.append("{code:java}")
                        output.append(f"{task['desc']}")
                        output.append("{code}")
                    
                    output.append(f"结束：{end_time}")
                    
                    if duration:
                        output.append(f"耗时：{duration:.2f} 小时")
                
                output.append("")  # 分隔不同的任务
            
            # 打印总耗时
            output.append(f"所有组总耗时：{total_duration:.2f} 小时")
            
            # 连接输出内容为一个字符串
            final_output = "\n".join(output)
            
            # 复制到剪贴板
            pyperclip.copy(final_output)
            
            # 输出到控制台
            print(final_output)
            
    finally:
        connection.close()  # 确保关闭数据库连接


def main():
    # 设置参数解析
    parser = argparse.ArgumentParser(description='根据 tag 查询 tasks 表')
    parser.add_argument('tag', type=str, help='查询用的 tag1')
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 根据提供的 tag 查询数据
    fetch_tasks_by_tag(args.tag)

# 运行脚本
if __name__ == '__main__':
    main()
