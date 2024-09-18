import requests
from datetime import datetime, timedelta
import random
import sys

def getBeforeDate(n):
    today = datetime.now()
    before = today - timedelta(days=n)
    return before.strftime("%Y-%m-%d")

def amClockInTime(n):
    before = getBeforeDate(n)
    randomMinute = random.randint(25, 30)
    randomMinute = str(randomMinute).zfill(2)
    randomSecond = random.randint(0, 59)
    randomSecond = str(randomSecond).zfill(2)
    return before + 'T09:' + randomMinute + ':' + randomSecond

def amClockOutTime(n):
    before = getBeforeDate(n)
    randomMinute = random.randint(0, 4)
    randomMinute = str(randomMinute).zfill(2)
    randomSecond = random.randint(0, 59)
    randomSecond = str(randomSecond).zfill(2)
    return before + 'T12:' + randomMinute + ':' + randomSecond

def pmClockInTime(n):
    before = getBeforeDate(n)
    randomMinute = random.randint(0, 2)
    randomMinute = str(randomMinute).zfill(2)
    randomSecond = random.randint(0, 59)
    randomSecond = str(randomSecond).zfill(2)
    return before + 'T13:' + randomMinute + ':' + randomSecond

def pmClockOutTime(n, amStartMinute):
    before = getBeforeDate(n)
    randomMinute = random.randint(amStartMinute - 5, amStartMinute + 5)
    randomMinute = str(randomMinute).zfill(2)
    randomSecond = random.randint(0, 59)
    randomSecond = str(randomSecond).zfill(2)
    return before + 'T18:' + randomMinute + ':' + randomSecond

def getToken():
    url = 'https://timetracker.logisticsteam.com/timetracker/employee/Login'
    headers = {}
    data = {
        'username': 'jasperw',
        'password': 'jasperw2019',
    }
    response = requests.post(url, headers=headers, json=data)
    json = response.json()
    return json['Authorization']

def getDuration(startTime, endTime):
    startTime = datetime.strptime(startTime, "%Y-%m-%dT%H:%M:%S")
    endTime = datetime.strptime(endTime, "%Y-%m-%dT%H:%M:%S")
    duration = endTime - startTime
    return duration

def timeRecord(authorization, n):
    url = 'https://timetracker.logisticsteam.com/timetracker/time-record'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'authorization': authorization,
        'content-type': 'application/json'
    }
    
    # 上午打卡
    amStartTime = amClockInTime(n)
    amStartMinute = int(amStartTime.split(':')[1])
    amEndTime = amClockOutTime(n)
    amDuration = getDuration(amStartTime, amEndTime)
    amDuration = str(amDuration).split('.')[0]
    
    amData = {
        'userId': 63,
        'type': 'ManualEntry',
        'moduleName': 'TMS',
        'projectName': 'Control Panel',
        'taskName': 'Coding',
        'startTime': amStartTime,
        'duration': amDuration,
        'endTime': amEndTime
    }
    amResponse = requests.post(url, headers=headers, json=amData)
    amJson = amResponse.json()
    
    # 下午打卡
    pmStartTime = pmClockInTime(n)
    pmEndTime = pmClockOutTime(n, amStartMinute)
    pmDuration = getDuration(pmStartTime, pmEndTime)
    pmDuration = str(pmDuration).split('.')[0]
    
    pmData = {
        'userId': 63,
        'type': 'ManualEntry',
        'moduleName': 'TMS',
        'projectName': 'Control Panel',
        'taskName': 'Coding',
        'startTime': pmStartTime,
        'duration': pmDuration,
        'endTime': pmEndTime
    }
    pmResponse = requests.post(url, headers=headers, json=pmData)
    pmJson = pmResponse.json()
    
    return [amJson, pmJson]

def get_start_end_of_week(week_number, exclude_weekend=True):
    # 获取当前年份
    current_year = datetime.now().year

    # 计算给定周数的第一天
    first_day_of_week = datetime.strptime(f'{current_year}-W{week_number}-1', "%Y-W%W-%w")

    # 如果排除周末
    if exclude_weekend:
        # 如果第一天是周六或周日，调整到下一周一
        if first_day_of_week.weekday() >= 5:
            first_day_of_week += timedelta(days=8 - first_day_of_week.weekday())

    # 计算结束日期
    end_of_week = first_day_of_week + timedelta(days=4)  # 这里假设一周工作日为 5 天

    return first_day_of_week, end_of_week

def get_current_week_number():
    today = datetime.now()
    week_number = today.strftime("%U")
    return int(week_number)

def get_week_days():
    current_week_number = get_current_week_number()
    week_number = input(f"Input week number(default current week {current_week_number}): ") or current_week_number
    # 获取某一周的开始和结束时间（排除周末）
    start_date, end_date = get_start_end_of_week(week_number, exclude_weekend=True)
    return start_date, end_date

def get_days_range(start_date, end_date):
    # 获取 start_date 和 end_date 距离今天的天数
    start_date_to_now = datetime.now() - start_date
    end_date_to_now = datetime.now() - end_date
    # 获取 start_date_to_now 和 end_date_to_now 之间的所有数字，包括本身
    week_days = range(end_date_to_now.days, start_date_to_now.days + 1)
    return week_days

if len(sys.argv) < 2:
    n = input('How many days prior to today do you want to check in: ')
    n = int(n)
    # 打印日期，再次让用户确认
    target_date = datetime.now() - timedelta(days=n)
    confirm = input(f"Are you sure to clock in/out for {target_date.strftime('%Y-%m-%d')}? (y/n): ")
    if confirm.lower() != 'y':
        exit()
    authorization = getToken()
    json = timeRecord(authorization, n)
    print(json)
    exit()

# 第一个参数的值
arg1 = sys.argv[1]
if (arg1 == 'd'):
    n = input('How many days prior to today do you want to check in: ')
    n = int(n)
    # 打印日期，再次让用户确认
    target_date = datetime.now() - timedelta(days=n)
    confirm = input(f"Are you sure to clock in/out for {target_date.strftime('%Y-%m-%d')}? (y/n): ")
    if confirm.lower() != 'y':
        exit()
    authorization = getToken()
    json = timeRecord(authorization, n)
    print(json)
elif (arg1 == 'w'):
    start_date, end_date = get_week_days()
    week_days = get_days_range(start_date, end_date)
    # confirm continue
    confirm = input(f"Are you sure to clock in/out for days between {start_date.strftime('%Y-%m-%d')} and {end_date.strftime('%Y-%m-%d')}? (y/n):")
    if confirm != 'y':
        exit()
    authorization = getToken()
    for day in week_days:
        json = timeRecord(authorization, day)
        print(json)
else:
    print('参数错误')