# 时间都去哪了
import pymysql
import argparse
from config import config
from datetime import datetime, timedelta
import csv
import re


db_config = config['local_mysql']
connection = pymysql.connect(
    host=db_config['host'],
    port=int(db_config['port']),
    user=db_config['username'],
    password=db_config['password'],
    db='automation', 
)

exclude_tags = ['午休', '下班', '休息']

def get_working_hours_per_day(start_date, end_date):
    try:
        connection = pymysql.connect(
            host=db_config['host'],
            port=int(db_config['port']),
            user=db_config['username'],
            password=db_config['password'],
            db='automation', 
        )

        cursor = connection.cursor()

        query = f"""
            SELECT 
                DATE(created_at) AS work_date,
                ROUND(SUM(TIME_TO_SEC(TIMEDIFF(IFNULL(end_at, NOW()), created_at))) / 3600, 2) AS total_work_time,
                GROUP_CONCAT(CONCAT(tag1, ': ', ROUND((TIME_TO_SEC(TIMEDIFF(IFNULL(end_at, NOW()), created_at))) / 3600, 2)) SEPARATOR ', ') AS tag_details
            FROM 
                tasks
            WHERE 
                created_at BETWEEN '{start_date}' AND '{end_date}'
                AND tag1 NOT IN ('{"', '".join(exclude_tags)}')
            GROUP BY 
                DATE(created_at)
        """

        cursor.execute(query)
        working_hours_per_day = cursor.fetchall()

        return working_hours_per_day

    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()

def combine_tag_details(tag_details):
    issue_hours = 0
    support_hours = 0
    others_hours = 0
    tag_dict = {}

    for detail in tag_details.split(', '):
        tag, time = detail.split(': ')
        if tag in tag_dict:
            tag_dict[tag] += float(time)
        else:
            tag_dict[tag] = float(time)

        if re.match(r'[A-Z]+-\d+', tag):
            issue_hours += float(time)
        elif tag == '支持':
            support_hours += float(time)
        else:
            others_hours += float(time)
    # Round the time to 1 decimal place
    rounded_tag_details = {tag: round(time, 2) for tag, time in tag_dict.items()}
    tag_details = ', '.join([f"{tag}: {time}" for tag, time in rounded_tag_details.items()])

    return issue_hours, support_hours, others_hours, tag_details

def write_to_csv(filename, data):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['日期', '应工作小时数', '实际工作小时数', '做 ticket 小时数', '支持别人的小时数', '其它小时数', '详情'])
        for row in data:
            date = row[0]
            expected_work_time = 8  # Assuming expected work time is 8 hours
            actual_work_time = round(row[1], 1)
            issue_hours, support_hours, others_hours, tag_details = combine_tag_details(row[2]) if row[2] else ""
            writer.writerow([date, expected_work_time, actual_work_time, issue_hours, support_hours, others_hours, tag_details])

if __name__ == "__main__":
    today = datetime.now()
    first_day_of_month = today.replace(day=1)
    last_day_of_month = (first_day_of_month.replace(month=first_day_of_month.month % 12 + 1, day=1) - timedelta(days=1))
    
    parser = argparse.ArgumentParser(description="Script to analyze work hours per day and total hours per tag1")
    parser.add_argument("--month", help="Specify the month or range of months to analyze, e.g., '4', '4,5'", default=f"{today.month}")
    args = parser.parse_args()
    
    months = args.month.split(",")
    if len(months) == 1:
        start_date = datetime(today.year, int(months[0]), 1).strftime('%Y-%m-%d')
        end_date = (datetime(today.year, int(months[0]), 1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        end_date = end_date.strftime('%Y-%m-%d')
    elif len(months) == 2:
        start_date = datetime(today.year, int(months[0]), 1).strftime('%Y-%m-%d')
        end_date = (datetime(today.year, int(months[1]), 1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        end_date = end_date.strftime('%Y-%m-%d')
    else:
        print("Invalid month input. Please specify one month or a range of months separated by comma.")
        exit()

    working_hours_per_day = get_working_hours_per_day(start_date, end_date)

    print("Writing to CSV file...")

    csv_filename = f"C:\\Users\\wuzhu\\Downloads\\work_hours_{start_date}_{end_date}.csv"
    write_to_csv(csv_filename, working_hours_per_day)

    print(f"CSV file {csv_filename} generated successfully.")
