import yaml


def get_ymal(filename):
    with open(filename,encoding='utf-8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data

def save_ymal(data,filename):
    with open(filename, 'w',encoding='utf-8') as f:
        yaml.dump(data, f)
