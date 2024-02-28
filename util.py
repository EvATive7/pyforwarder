import hashlib
import yaml
import json


def calculate_md5(file_path):
    # 创建一个 MD5 对象
    md5_hash = hashlib.md5()

    # 打开文件并逐块读取内容
    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b''):
            md5_hash.update(chunk)

    # 计算 MD5 值
    md5_value = md5_hash.hexdigest()

    return md5_value


def mimetype_is_text(mime_type: str) -> bool:
    try:
        return mime_type.startswith('text/')
    except Exception as e:
        pass


def prase_query_args(d) -> str:
    pass


def try_pop_ignore_cap(d: dict, key: str):
    lower_key = key.lower()

    for k in d.copy():
        k: str
        if k.lower() == lower_key:
            d.pop(k)


def read_file(path):
    with open(str(path), 'r', encoding='utf8') as file:
        return file.read()


def read_json(path):
    return json.loads(read_file(path))


def read_yaml(path):
    return yaml.safe_load(read_file(path))


def write_file(path, content):
    with open(str(path), 'w', encoding='utf8') as file:
        file.write(content)


def write_json(path, content):
    write_file(path, json.dumps(content, ensure_ascii=False))


def write_yaml(path, content):
    write_file(path, yaml.safe_dump(content))
