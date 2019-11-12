import os


class Config:
    def __init__(self):
        self.config_data = {}

    def read_config(self):
        path = os.environ.get("PY_NGINX_CONFIG_PATH")
        config_path = path if path is not None else "httpd.conf"

        with open(config_path, "r") as config_file:
            data = config_file.read()
            self.config_data = dict(map(lambda x: x.split(" "), data.strip("\n\r\t ").split("\n")))

        host = os.environ.get("PY_NGINX_HOST")
        port = os.environ.get("PY_NGINX_PORT")
        self.config_data["host"] = host if host is not None else "0.0.0.0"
        self.config_data["port"] = int(port) if host is not None else 8008