import requests

url = 'https://timetracker.logisticsteam.com/timetracker/time-record/task-in-progress/63'

headers = {
    'accept': 'application/json',
    'authorization': 'f1de2078-e2e5-47f3-9cfb-db550d2bb0b0'
}

response = requests.get(url, headers=headers)

# Print the response content or handle it as needed
print(response.text)
# [ {
#   "id" : 439408,
#   "type" : "StopWatch",
#   "userId" : 63,
#   "moduleName" : "LSO",
#   "projectName" : "LSO",
#   "taskName" : "Coding",
#   "startTime" : "2023-11-20T17:27:17",
#   "updatedBy" : "jasperw",
#   "updatedWhen" : "2023-11-20T17:27:17"
# } ]
id = response.json()[0]['id']
print(id)
