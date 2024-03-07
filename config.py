import yaml

def load_config(filename):
    with open(filename, 'r') as f:
        config = yaml.safe_load(f)
    return config

# 在模块级别加载配置并保存在变量中
config = load_config('config.yaml')
