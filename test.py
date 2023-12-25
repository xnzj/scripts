import git
from functions import get_user_choice

repo_name_path_map = {
    '1': 'C:/Me/Code/tms.freightapp.gofuze.io',
    '2': 'C:/Me/Code/tms-backend',
    '3': 'C:/Me/Code/cp-middleware',
}

repo_name = get_user_choice(repo_name_path_map, 'Choose git repo:')

# # 要求输入 git 仓库名
# repo_name = input('请输入 git 仓库名:')
# # 请输入需要被合并的分支名
# feature_branch = input('请输入需要被合并的分支名:')
# # 请输入输入接受合并的分支名
# target_branch = input('请输入输入接受合并的分支名:')


# # 获取仓库路径
# repo_path = repo_name_path_map[repo_name]
# # 获取仓库
# repo = git.Repo(repo_path)

