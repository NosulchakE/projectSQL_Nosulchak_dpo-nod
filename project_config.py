# Загрузка настроек проекта (в данном случае только настроек соединения с БД)
# из файла config.yaml.
import yaml

class ProjectConfig:
    def __init__(self):
        with open("config.yaml", "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
        self.dbname = cfg.get("dbname", "postgres")
        self.user = cfg.get("user", "postgres")
        self.password = cfg.get("password", "")
        self.host = cfg.get("host", "localhost")
        self.dbtableprefix = cfg.get("dbtableprefix", "public.")

