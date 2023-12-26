import requests
from datetime import datetime, timedelta
import random

def getBeforeDate(n):
    today = datetime.now()
    before = today - timedelta(days=n)
    return before.strftime("%Y-%m-%d")

def clockInTime(n):
    before = getBeforeDate(n)
    randomMinute = random.randint(0, 10)
    randomMinute = str(randomMinute).zfill(2)
    randomSecond = random.randint(0, 59)
    randomSecond = str(randomSecond).zfill(2)
    return before + 'T09:' + randomMinute + ':' + randomSecond

def clockOutTime(n):
    before = getBeforeDate(n)
    randomMinute = random.randint(5, 30)
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

def timeRecord(authorization, startTime, endTime):
    url = 'https://timetracker.logisticsteam.com/timetracker/time-record'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'authorization': authorization,
        'content-type': 'application/json'
    }
    # 根据 startTime 和 endTime 计算 duration
    duration = getDuration(startTime, endTime)
    # 将 duration 转换为时分秒格式
    duration = str(duration).split('.')[0]
    data = {
        'userId': 63,
        'type': 'ManualEntry',
        'moduleName': 'LSO',
        'projectName': 'LSO',
        'taskName': 'Coding',
        'startTime': startTime,
        'duration': duration,
        'endTime': endTime
    }
    response = requests.post(url, headers=headers, json=data)
    json = response.json()
    return json

n = input('请输入要给前几天打卡：')
n = int(n)
authorization = getToken()
startTime = clockInTime(n)
endTime = clockOutTime(n)
json = timeRecord(authorization, startTime, endTime)
print(json)