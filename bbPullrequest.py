from atlassian.bitbucket import Cloud
from atlassian import Bitbucket
from dotenv import load_dotenv
import os
import sys
import time
import git
import requests
load_dotenv()

cloud = Cloud(
    username=os.getenv("BITBUCKET_USERNAME"),
    password=os.getenv("BITBUCKET_PASSWORD"),
    cloud=True)

repositories = {
    1: "tms-backend",
    2: "tms.freightapp.gofuze.io",
    3: "cp-middleware",
}

destination_branchs = {
    1: "staging",
    2: "master",
}

# 让用户选择一个仓库
print("请选择一个仓库：")
for key, value in repositories.items():
    print(f"{key}. {value}")
choice = input("请输入仓库号码(default 1): ")
if choice == "":
    choice = 1
choice = int(choice)
repository_name = repositories[choice]
print(f"你选择了 {repository_name}")

repo_path = f"C:/Me/Code/{repository_name}"
repo = git.Repo(repo_path)
active_branch = repo.active_branch
print(f"{repository_name} 的当前分支是 {active_branch}")

# 是否使用当前分支名
use_current_branch = input("是否使用当前分支名？(y/n, default y): ")
if use_current_branch.lower() != "n":
    branch_name = str(active_branch)
else:
    branch_name = input("请输入分支名：")

for key, value in destination_branchs.items():
    print(f"{key}. {value}")
choice = input("请输入目标分支号码(default 1): ")
if choice == "":
    choice = 1
choice = int(choice)
destination_branch = destination_branchs[choice]

def checkPipelineStatus(repository):
    running_pipelines = {}
    count = 0
    for pipline in repository.pipelines.each(sort="-created_on"):
        if (pipline.build_seconds_used == 0):
            print(f"pipline {pipline.build_number} is running")
            build_number = pipline.build_number
            running_pipelines[build_number] = pipline.uuid
        count += 1
        if count > 10:
            if (len(running_pipelines) == 0):
                print("all pipelines are completed")
            break
    # 检查正在运行的 pipeline 是否全部完成
    check_times = 0
    while len(running_pipelines) > 0:
        for build_number, uuid in running_pipelines.copy().items():
            pipeline = repository.pipelines.get(uuid)
            if pipeline.build_seconds_used > 0:
                print(f"pipline {build_number} is completed")
                running_pipelines.pop(build_number)
        check_times += 1
        if (len(running_pipelines) > 0):
            time.sleep(6)
            print(f"checking pipeline status {check_times} times")
        else:
            print("all pipelines are completed")
            break
        if (check_times > 20):
            print("pipeline not completed in 2 minutes, exit")
            break

try:
    workplace = cloud.workspaces.get("logisticsteam-dev")
    repository = workplace.repositories.get(repository_name)
    print(f"title: {branch_name}, sourceBranch: {branch_name}, destinationBranch: {destination_branch}")
    # 把本地代码推送到远程仓库
    origin = repo.remotes.origin
    origin.push()
    print("Successfully pushed to remote repository.")
    rst = repository.pullrequests.create(branch_name, branch_name, destination_branch)
    pull_request_id = rst.id
    print(f"Successfully created pull request {pull_request_id}.")
    # merge the pull request
    pull_request = repository.pullrequests.get(pull_request_id)
    pull_request.merge()
    print(f"Successfully merged pull request {pull_request_id}.")
    time.sleep(10)
    checkPipelineStatus(repository)
except requests.exceptions.HTTPError as e:
    print(f"Something wrong when pull request: {e}")
