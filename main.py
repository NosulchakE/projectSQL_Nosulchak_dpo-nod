from project_config import ProjectConfig
from dbconnection import DbConnection
from tables.countries_table import CountriesTable
from tables.movies_table import MoviesTable

PAGE_SIZE = 5

class MainApp:
    def __init__(self):
        self.config = ProjectConfig()
        self.conn = DbConnection(self.config)
        CountriesTable.dbconn = self.conn
        MoviesTable.dbconn = self.conn

        self.countries = CountriesTable()
        self.movies = MoviesTable()
        self.countries.create()
        self.movies.create()

    def main_menu(self):
        while True:
            print("\n=== Главное меню ===")
            print("1 - Управление странами")
            print("2 - Управление фильмами")
            print("9 - Выход")
            choice = input("=> ").strip()
            if choice == "1":
                self.countries_menu()
            elif choice == "2":
                self.movies_menu()
            elif choice == "9":
                break
            else:
                print("Неверный ввод!")

    # ----------------- Страны -----------------
    def countries_menu(self):
        page = 0
        while True:
            countries = self.countries.all(limit=PAGE_SIZE, offset=page*PAGE_SIZE)
            print("\n=== Страны ===")
            for idx, row in enumerate(countries, start=1):
                print(f"{idx}. {row[0]}")
            print("\nn - следующая, p - предыдущая, a - добавить, 0 - назад")
            cmd = input("=> ").strip().lower()
            if cmd == "n":
                page += 1
            elif cmd == "p" and page > 0:
                page -= 1
            elif cmd == "a":
                name = input("Название страны: ").strip()
                if name:
                    self.countries.insert_one(name)
            elif cmd == "0":
                break

    # ----------------- Фильмы -----------------
    def movies_menu(self):
        page = 0
        while True:
            movies = self.movies.all(limit=PAGE_SIZE, offset=page*PAGE_SIZE)
            print("\n=== Фильмы ===")
            for idx, row in enumerate(movies, start=1):
                title, genre, duration, age, country = row
                print(f"{idx}. {title} | {genre} | {duration} мин | {age}+ | {country}")
            print("\nn - следующая, p - предыдущая, a - добавить, 0 - назад")
            cmd = input("=> ").strip().lower()
            if cmd == "n":
                page += 1
            elif cmd == "p" and page > 0:
                page -= 1
            elif cmd == "a":
                title = input("Название: ").strip()
                genre = input("Жанр: ").strip()
                duration = int(input("Продолжительность (мин): "))
                age = int(input("Возрастное ограничение: "))
                # Выбор страны
                countries = self.countries.all()
                for i, c in enumerate(countries, start=1):
                    print(f"{i}. {c[0]}")
                cnum = int(input("Номер страны: "))
                country_name = countries[cnum-1][0] if 1 <= cnum <= len(countries) else None
                self.movies.insert_one(title, genre, duration, age, country_name)
            elif cmd == "0":
                break

if __name__ == "__main__":
    app = MainApp()
    app.main_menu()
