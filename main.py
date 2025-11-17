from project_config import ProjectConfig
from dbconnection import DbConnection
from tables.country_table import CountriesTable
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
            print("\nn - следующая, p - предыдущая, a - добавить, e - изменить, d - удалить, 0 - назад")
            cmd = input("=> ").strip().lower()
            if cmd == "n":
                page += 1
            elif cmd == "p" and page > 0:
                page -= 1
            elif cmd == "a":
                name = input("Название страны: ").strip()
                if name:
                    self.countries.insert_one(name)
            elif cmd == "e":
                num = int(input("Номер страны для редактирования: "))
                if 1 <= num <= len(countries):
                    old_name = countries[num-1][0]
                    new_name = input(f"Новое название для '{old_name}': ").strip()
                    self.countries.update_one(old_name, new_name)
            elif cmd == "d":
                num = int(input("Номер страны для удаления: "))
                if 1 <= num <= len(countries):
                    self.countries.delete_one(countries[num-1][0])
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
            print("\nn - следующая, p - предыдущая, a - добавить, e - изменить, d - удалить, 0 - назад")
            cmd = input("=> ").strip().lower()
            if cmd == "n":
                page += 1
            elif cmd == "p" and page > 0:
                page -= 1
            elif cmd == "a":
                self.add_movie()
            elif cmd == "e":
                self.edit_movie(movies)
            elif cmd == "d":
                self.delete_movie(movies)
            elif cmd == "0":
                break

    def add_movie(self):
        title = input("Название: ").strip()
        genre = input("Жанр: ").strip()
        duration = int(input("Продолжительность (мин): "))
        age = int(input("Возрастное ограничение: "))
        countries = self.countries.all()
        for i, c in enumerate(countries, start=1):
            print(f"{i}. {c[0]}")
        cnum = int(input("Номер страны: "))
        country_name = countries[cnum-1][0] if 1 <= cnum <= len(countries) else None
        self.movies.insert_one(title, genre, duration, age, country_name)

    def edit_movie(self, movies):
        num = int(input("Номер фильма для редактирования: "))
        if 1 <= num <= len(movies):
            old_title, genre, duration, age, country = movies[num-1]
            title = input(f"Название [{old_title}]: ").strip() or old_title
            genre = input(f"Жанр [{genre}]: ").strip() or genre
            duration_input = input(f"Продолжительность [{duration}]: ").strip()
            duration = int(duration_input) if duration_input else duration
            age_input = input(f"Возрастное ограничение [{age}]: ").strip()
            age = int(age_input) if age_input else age
            countries = self.countries.all()
            for i, c in enumerate(countries, start=1):
                print(f"{i}. {c[0]}")
            cnum = int(input(f"Номер страны [{country}]: "))
            country_name = countries[cnum-1][0] if 1 <= cnum <= len(countries) else country
            self.movies.update_one(old_title, title, genre, duration, age, country_name)

    def delete_movie(self, movies):
        num = int(input("Номер фильма для удаления: "))
        if 1 <= num <= len(movies):
            self.movies.delete_one(movies[num-1][0])

if __name__ == "__main__":
    app = MainApp()
    app.main_menu()

