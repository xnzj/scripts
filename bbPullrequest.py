from atlassian.bitbucket import Cloud
from atlassian import Bitbucket
from dotenv import load_dotenv
import os
import time
import git
import requests
load_dotenv()

cloud = Cloud(
    username=os.getenv("BITBUCKET_USERNAME"),
    password=os.getenv("BITBUCKET_PASSWORD"),
    cloud=True)

repositories = {
    1: "tms.freightapp.gofuze.io",
    2: "tms-backend",
    3: "cp-middleware",
}

destination_branchs = {
    1: "master",
    2: "staging",
}

# 让用户选择一个仓库
print("请选择一个仓库：")
for key, value in repositories.items():
    print(f"{key}. {value}")
choice = int(input("请输入仓库号码："))
repository_name = repositories[choice]
print(f"你选择了 {repository_name}")

repo_path = f"C:/Me/Code/{repository_name}"
repo = git.Repo(repo_path)
active_branch = repo.active_branch
print(f"{repository_name} 的当前分支是 {active_branch}")

# 是否使用当前分支名
use_current_branch = input("是否使用当前分支名？(y/n): ")
if use_current_branch.lower() == "y":
    branch_name = active_branch
else:
    branch_name = input("请输入分支名：")

for key, value in destination_branchs.items():
    print(f"{key}. {value}")
choice = int(input("请输入目标分支号码："))
destination_branch = destination_branchs[choice]

try:
    workplace = cloud.workspaces.get("logisticsteam-dev")
    repository = workplace.repositories.get(repository_name)
    rst = repository.pullrequests.create(branch_name, branch_name, destination_branch)
    pull_request_id = rst['id']
    print(f"Successfully created pull request {pull_request_id}.")
    # merge the pull request
    pull_request = repository.pullrequests.get(pull_request_id)
    pull_request.merge()
    print(f"Successfully merged pull request {pull_request_id}.")
    # check if the pull request is merged. If not, check again after 5 seconds
    # 超过 5 分钟还没合并则退出
    while not pull_request.is_merged:
        time.sleep(5)
        print(".")
        if time.time() - pull_request.created_on > 300:
            print(f"Failed to merge pull request {pull_request_id} after 5 minutes.")
            break


except requests.exceptions.HTTPError as e:
    print(f"Something wrong when pull request: {e}")
