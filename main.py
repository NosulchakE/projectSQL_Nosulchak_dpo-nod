import sys
sys.path.append('tables')

from project_config import ProjectConfig
from dbconnection import DbConnection
from tables.country_table import CountriesTable
from tables.movies_table import MoviesTable

class Main:

    config = ProjectConfig()
    connection = DbConnection(config)

    def __init__(self):
        # Инициализируем соединение для таблиц
        CountriesTable.dbconn = self.connection
        MoviesTable.dbconn = self.connection
        return

    # Главное меню
    def show_main_menu(self):
        menu = """Добро пожаловать! 
Основное меню (выберите цифру в соответствии с необходимым действием): 
    1 - Управление странами;
    2 - Управление фильмами;
    9 - выход."""
        print(menu)

    # Считываем ввод
    def read_next_step(self):
        return input("=> ").strip()

    # После выбора в главном меню
    def after_main_menu(self, next_step):
        if next_step == "1":
            return "1"  # Меню стран
        elif next_step == "2":
            return "2"  # Меню фильмов
        elif next_step == "9":
            return "9"  # Выход
        else:
            print("Выбрано неверное число! Повторите ввод!")
            return "0"

    # --- Меню стран ---
    def show_countries(self):
        menu = """Управление странами:
    1 - добавить страну
    2 - редактировать страну
    3 - удалить страну
    n - следующая страница
    p - предыдущая страница
    0 - возврат в главное меню"""
        print(menu)

        # Показываем текущие страны
        lst = CountriesTable().all()
        print("\nСписок стран:")
        for idx, country in enumerate(lst, start=1):
            print(f"{idx}. {country[0]}")

    # --- Меню фильмов ---
    def show_movies(self):
        menu = """Управление фильмами:
    1 - добавить фильм
    2 - редактировать фильм
    3 - удалить фильм
    n - следующая страница
    p - предыдущая страница
    0 - возврат в главное меню"""
        print(menu)

        # Показываем текущие фильмы
        lst = MoviesTable().all()
        print("\nСписок фильмов:")
        for idx, movie in enumerate(lst, start=1):
            country = movie[5] if movie[5] else "не указана"
            print(f"{idx}. {movie[0]} | Жанр: {movie[1]} | Длительность: {movie[2]} мин | Возраст: {movie[3]} | Страна: {country}")

    # Основной цикл проекта
    def main_cycle(self):
        current_menu = "0"
        while current_menu != "9":
            if current_menu == "0":
                self.show_main_menu()
                next_step = self.read_next_step()
                current_menu = self.after_main_menu(next_step)
            elif current_menu == "1":
                self.show_countries()
                input("Нажмите Enter для возврата в главное меню...")
                current_menu = "0"
            elif current_menu == "2":
                self.show_movies()
                input("Нажмите Enter для возврата в главное меню...")
                current_menu = "0"

# ============================
# Запуск проекта
# ============================
if __name__ == "__main__":
    app = Main()
    app.main_cycle()
