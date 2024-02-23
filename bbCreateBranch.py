from atlassian.bitbucket import Cloud
from atlassian import Bitbucket
from dotenv import load_dotenv
import os
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

# 让用户输入分支名 
branch_name = input("请输入分支名：")

workplace = cloud.workspaces.get("logisticsteam-dev")
repository = workplace.repositories.get(repository_name)

def checkout_or_stash(repository_name, branch_name):
    # 创建 Git 仓库对象
    repo_path = f"C:/Me/Code/{repository_name}"
    repo = git.Repo(repo_path)
    repo.git.fetch()
    # 尝试切换分支
    try:
        repo.git.checkout(branch_name)
        print(f"Successfully checked out branch {branch_name}.")
    except git.GitCommandError:
        # 如果切换分支失败，则将未提交的更改暂存起来
        print("Failed to checkout branch. Stashing changes...")
        repo.git.stash()

        # 再次尝试切换分支
        try:
            repo.git.checkout(branch_name)
            print(f"Successfully checked out branch {branch_name}.")
        except git.GitCommandError as e:
            print(f"Failed to checkout branch {branch_name}: {e}")

try:
    repository.branches.create(branch_name, "master")
    checkout_or_stash(repository_name, branch_name)
except requests.exceptions.HTTPError as e:
    json = e.response.json()
    error_code = json['error']['code']
    if (error_code == "BRANCH_ALREADY_EXISTS"):
        print(f"分支 {branch_name} 已经存在")
        checkout_or_stash(repository_name, branch_name)
    else:
        print(f"Failed to create branch: {e}")
