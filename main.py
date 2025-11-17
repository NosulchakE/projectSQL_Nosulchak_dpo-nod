import sys
sys.path.append('tables')

from project_config import ProjectConfig
from dbconnection import DbConnection
from tables.country_table import CountriesTable
from tables.movies_table import MoviesTable

PAGE_SIZE = 5  # количество записей на странице

class Main:

    config = ProjectConfig()
    connection = DbConnection(config)

    def __init__(self):
        CountriesTable.dbconn = self.connection
        MoviesTable.dbconn = self.connection
        return

    # Главное меню
    def show_main_menu(self):
        print("""Добро пожаловать! 
Основное меню (выберите цифру в соответствии с необходимым действием): 
    1 - Управление странами;
    2 - Управление фильмами;
    9 - выход.""")

    def read_next_step(self):
        return input("=> ").strip()

    def after_main_menu(self, next_step):
        if next_step == "1":
            return "1"
        elif next_step == "2":
            return "2"
        elif next_step == "9":
            return "9"
        else:
            print("Выбрано неверное число! Повторите ввод!")
            return "0"

    # -------------------
    # Работа со странами
    # -------------------
    def show_countries(self, page=0):
        table = CountriesTable()
        all_countries = table.all()
        start = page * PAGE_SIZE
        end = start + PAGE_SIZE
        subset = all_countries[start:end]

        print("\nСписок стран:")
        for idx, country in enumerate(subset, start=1+start):
            print(f"{idx}. {country[0]}")

        print(f"""
Управление странами:
    a - добавить
    e - редактировать
    d - удалить
    n - следующая страница
    p - предыдущая страница
    0 - главное меню""")

        choice = input("=> ").strip()
        if choice == "a":
            self.add_country()
        elif choice == "e":
            self.edit_country()
        elif choice == "d":
            self.delete_country()
        elif choice == "n":
            if end < len(all_countries):
                return self.show_countries(page + 1)
        elif choice == "p":
            if page > 0:
                return self.show_countries(page - 1)
        elif choice == "0":
            return "0"
        else:
            print("Неверный выбор!")

        return self.show_countries(page)

    def add_country(self):
        name = input("Введите название страны: ").strip()
        if not name:
            print("Название не может быть пустым.")
            return
        CountriesTable().insert_one(name)
        print(f"Страна '{name}' добавлена!")

    def edit_country(self):
        table = CountriesTable()
        all_countries = table.all()
        num = input("Введите номер страны для редактирования: ").strip()
        if not num.isdigit() or int(num) < 1 or int(num) > len(all_countries):
            print("Некорректный номер")
            return
        old_name = all_countries[int(num)-1][0]
        new_name = input(f"Новое название для '{old_name}': ").strip()
        if not new_name:
            print("Название не может быть пустым")
            return
        cur = table.dbconn.conn.cursor()
        cur.execute("UPDATE countries SET country_name=%s WHERE country_name=%s", (new_name, old_name))
        table.dbconn.conn.commit()
        print("Страна обновлена!")

    def delete_country(self):
        table = CountriesTable()
        all_countries = table.all()
        num = input("Введите номер страны для удаления: ").strip()
        if not num.isdigit() or int(num) < 1 or int(num) > len(all_countries):
            print("Некорректный номер")
            return
        name = all_countries[int(num)-1][0]
        cur = table.dbconn.conn.cursor()
        cur.execute("DELETE FROM countries WHERE country_name=%s", (name,))
        table.dbconn.conn.commit()
        print(f"Страна '{name}' удалена!")

    # -------------------
    # Работа с фильмами
    # -------------------
    def show_movies(self, page=0):
        table = MoviesTable()
        all_movies = table.all()
        start = page * PAGE_SIZE
        end = start + PAGE_SIZE
        subset = all_movies[start:end]

        print("\nСписок фильмов:")
        for idx, movie in enumerate(subset, start=1+start):
            country = movie[5] if movie[5] else "не указана"
            print(f"{idx}. {movie[0]} | Жанр: {movie[1]} | Длительность: {movie[2]} мин | Возраст: {movie[3]} | Страна: {country}")

        print(f"""
Управление фильмами:
    a - добавить
    e - редактировать
    d - удалить
    n - следующая страница
    p - предыдущая страница
    0 - главное меню""")

        choice = input("=> ").strip()
        if choice == "a":
            self.add_movie()
        elif choice == "e":
            self.edit_movie()
        elif choice == "d":
            self.delete_movie()
        elif choice == "n":
            if end < len(all_movies):
                return self.show_movies(page + 1)
        elif choice == "p":
            if page > 0:
                return self.show_movies(page - 1)
        elif choice == "0":
            return "0"
        else:
            print("Неверный выбор!")
        return self.show_movies(page)

    def add_movie(self):
        title = input("Название фильма: ").strip()
        genre = input("Жанр: ").strip()
        duration = input("Продолжительность (мин): ").strip()
        min_age = input("Минимальный возраст: ").strip()

        countries = CountriesTable().all()
        print("Выберите страну производства:")
        for idx, c in enumerate(countries, start=1):
            print(f"{idx}. {c[0]}")

        country_choice = input("Номер страны (или Enter для пустого): ").strip()
        country_name = None
        if country_choice.isdigit():
            num = int(country_choice)
            if 1 <= num <= len(countries):
                country_name = countries[num-1][0]

        try:
            duration = int(duration)
            min_age = int(min_age)
        except:
            print("Длительность и возраст должны быть числами!")
            return

        MoviesTable().insert_one(title, genre, duration, min_age, country_name)
        print(f"Фильм '{title}' добавлен!")
    def edit_movie(self):
        table = MoviesTable()
        all_movies = table.all()
        num = input("Введите номер фильма для редактирования: ").strip()
        if not num.isdigit() or int(num) < 1 or int(num) > len(all_movies):
            print("Некорректный номер")
            return
        old = all_movies[int(num)-1]
        new_title = input(f"Новое название (Enter чтобы оставить '{old[0]}'): ").strip() or old[0]
        new_genre = input(f"Жанр (Enter чтобы оставить '{old[1]}'): ").strip() or old[1]
        new_duration = input(f"Длительность (Enter чтобы оставить '{old[2]}'): ").strip() or old[2]
        new_min_age = input(f"Мин. возраст (Enter чтобы оставить '{old[3]}'): ").strip() or old[3]

        # Страна
        countries = CountriesTable().all()
        print("Выберите страну производства:")
        for idx, c in enumerate(countries, start=1):
            print(f"{idx}. {c[0]}")
        country_choice = input("Номер страны (или Enter оставить текущую): ").strip()
        country_name = old[4]
        if country_choice.isdigit():
            numc = int(country_choice)
            if 1 <= numc <= len(countries):
                country_name = countries[numc-1][0]

        cur = table.dbconn.conn.cursor()
        cur.execute("""UPDATE movies SET title=%s, genre=%s, duration_minutes=%s, minimum_age=%s, country_name=%s
                       WHERE title=%s""",
                    (new_title, new_genre, int(new_duration), int(new_min_age), country_name, old[0]))
        table.dbconn.conn.commit()
        print("Фильм обновлен!")

    def delete_movie(self):
        table = MoviesTable()
        all_movies = table.all()
        num = input("Введите номер фильма для удаления: ").strip()
        if not num.isdigit() or int(num) < 1 or int(num) > len(all_movies):
            print("Некорректный номер")
            return
        title = all_movies[int(num)-1][0]
        cur = table.dbconn.conn.cursor()
        cur.execute("DELETE FROM movies WHERE title=%s", (title,))
        table.dbconn.conn.commit()
        print(f"Фильм '{title}' удален!")

    # -------------------
    # Основной цикл
    # -------------------
    def main_cycle(self):
        current_menu = "0"
        while current_menu != "9":
            if current_menu == "0":
                self.show_main_menu()
                next_step = self.read_next_step()
                current_menu = self.after_main_menu(next_step)

            elif current_menu == "1":
                result = self.show_countries()
                if result == "0":
                    current_menu = "0"

            elif current_menu == "2":
                result = self.show_movies()
                if result == "0":
                    current_menu = "0"


# ============================
if __name__ == "__main__":
    app = Main()
    app.main_cycle()



