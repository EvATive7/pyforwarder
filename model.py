from util import *


class ConfigFilePath:
    root = './Data/Config'

    host_match = f'{root}/host_match.yaml'
    setting = f'{root}/setting.yaml'


class Config:
    def __init__(self, path) -> None:
        self.path = path

        self._data = None
        self._md5 = None

    @property
    def data(self) -> object:
        self._try_update()
        return self._data

    def _try_update(self):
        current_md5 = calculate_md5(self.path)
        if current_md5 != self._md5:
            self._data = read_yaml(self.path)
            self._md5 = current_md5


class HostMatch(Config):
    def __init__(self) -> None:
        super().__init__(ConfigFilePath.host_match)

    @property
    def list(self):
        result: list[tuple[str, str]] = []
        data = self.data

        for key in data:
            value = data[key]
            result.append((key, value))

        return result


class Setting(Config):
    def __init__(self) -> None:
        super().__init__(ConfigFilePath.setting)

    @property
    def proxy(self):
        data = self.data
        proxy_endpoint = data['proxy']
        proxy_url = 'http://' + proxy_endpoint

        return {
            'http': proxy_url,
            'https': proxy_url
        }

    @property
    def running_config(self):
        data = self.data
        _d = data['running_config']
        host = _d['host']
        port = _d['port']
        https = _d['https']

        return host, port, https
