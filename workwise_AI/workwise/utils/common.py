import yaml

def return_ym_config(path_yml = r"D:\workwise_AI\workwise\utils\config.yml"):
    with open(path_yml, 'r') as file:
        config = yaml.safe_load(file)
    return config