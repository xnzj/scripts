import git
from functions import get_user_choice, get_user_input, get_key_by_value

repo_name_path_map = {
    'tms': 'C:/Me/Code/tms.freightapp.gofuze.io',
    'backend': 'C:/Me/Code/tms-backend'
}

repo_name_resolve_conflict_branch_map = {
    'tms': 'resolve-conflict-staging-jasper',
    'backend': 'RESOLVE-CONFLICT-STAGING',
}

repo_name = get_user_choice(repo_name_path_map, 'Choose git repo', 'backend')
if repo_name not in repo_name_path_map:
    print('Invalid repo name')
    exit(1)
repo_path = repo_name_path_map[repo_name]
repo = git.Repo(repo_path)
# print(repo)

target_branch = get_user_input('Target branch', 'staging')
feature_branch = get_user_input('Feature branch')
resolve_conflict_branch = repo_name_resolve_conflict_branch_map[repo_name]

# 切换到 target_branch
repo.git.checkout(target_branch)
print(f'Branch {target_branch} checked out')
# 拉取最新代码
repo.git.pull()
print(f'Branch {target_branch} pulled')
# 切换到 resolve_conflict_branch
repo.git.checkout(resolve_conflict_branch)
print(f'Branch {resolve_conflict_branch} checked out')
# 合并 target_branch 到 resolve_conflict_branch
repo.git.merge(target_branch)
print(f'Merged {target_branch} into {resolve_conflict_branch}')
# 合并 feature_branch 到 resolve_conflict_branch
repo.git.merge(feature_branch)
print(f'Merged {feature_branch} into {resolve_conflict_branch}')
