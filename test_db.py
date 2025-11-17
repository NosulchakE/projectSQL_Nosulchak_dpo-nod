from project_config import ProjectConfig
from dbconnection import DbConnection

cfg = ProjectConfig()
try:
    conn = DbConnection(cfg)
    print("Соединение с PostgreSQL успешно!")
except Exception as e:
    print("Ошибка соединения:", e)
