import os
import re
import shutil
import subprocess
import textwrap
import time
import zipfile
from getpass import getpass


class Utils():
    """
    Класс Utils содержит общие утилитарные методы для работы Django Starter Generator.
    """

    def clear(self):
        # Для Windows
        if os.name == 'nt':
            os.system('cls')
        # Для Unix-подобных систем
        else:
            os.system('clear')


class Colors:
    """ Цвета сообщений """
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"


class Messages():

    def __init__(self, message=None, color=Colors.RESET):
        self.message = message
        self.color = color

    """ Класс сообщений """
    HERO = f"""{Colors.GREEN}
    ██████╗     ███████╗     ██████╗     Django Starter Generator -
    ██╔══██╗    ██╔════╝    ██╔════╝     приложение для автоматизации
    ██║  ██║    ███████╗    ██║  ███╗    создания, настройки и первого
    ██║  ██║    ╚════██║    ██║   ██║    запуска проектов на Django.
    ██████╔╝    ███████║    ╚██████╔╝
    ╚═════╝     ╚══════╝     ╚═════╝{Colors.RESET}     Copyright (c) 2024 Artem Fomin"""

    GREETING = f"""
    Добрый день!
    Начинаем создание вашего нового проекта Django.
    """

    PASSWORD_REQUIREMENTS = f"""
    Теперь нужно создать суперпользователя, задав его email и пароль.

    Требования к паролю:
    - Пароль должен содержать не менее 8 символов
    - Должны использоваться только латинские буквы
    - Пароль должен содержать хотя бы одну заглавную латинскую букву
    - Пароль должен содержать хотя бы одну строчную латинскую букву
    - Пароль не должен содержать пробелов
    - Желательно также использовать специальные символы
    """

    PASSWORD_ERRORS = [
        f"""    Пароль должен содержать не менее 8 символов.\n""",
        f"""    Пароль должен содержать хотя бы одну заглавную латинскую букву.\n""",
        f"""    Пароль должен содержать хотя бы одну строчную латинскую букву.\n""",
        f"""    Пароль должен содержать хотя бы одну цифру.\n""",
        f"""    Пароль должен содержать хотя бы один специальный символ.\n""",
        f"""    Пароль не должен содержать пробелов.\n""",
    ]

    EMAIL_SETUP_START = f"""
    Теперь можно настроить отправку электронной почты.
    """

    EMAIL_SETUP_LATER = f"""
    Настройки почтового сервера можно будут выполнить позже в файле ".env".
    """

    TELEGRAM_SETUP_START = f"""
    Теперь можно настроить Telegram для отправки уведомлений администратору.
    """

    TELEGRAM_SETUP_LATER = f"""
    Настройки Telegram можно будут выполнить позже в файле ".env".
    """

    START_DEPLOYMENT = f"""
    Отлично!
    Запускаем развертывание проекта...
    """

    SUCCESS = f"""
    Проект успешно создан и настроен.
    Удачной разработки!
    """

    reminds = []

    def print_message(self):
        """
        Вывод сообщения
        """
        # time.sleep(0.5)  # Задержка перед выводом всего сообщения
        lines = self.message.split('\n')
        # очистка каждой строки от пробелов в начале и в конце
        lines = [line.strip() for line in lines]
        # заменяем табуляции на 4 пробела
        lines = [line.replace('\t', '    ') for line in lines]
        max_len = max(len(line) for line in lines)
        print(f"\n{self.color}   ╭{'─' * (max_len + 4)}╮")
        for line in lines:
            print(f"   │  {line.ljust(max_len)}  │")
        print(f".oO╰{'─' * (max_len + 4)}╯{Colors.RESET}\n")


class Logger:
    def info(self, message):
        print(f"    {Colors.GREEN}[INFO]{Colors.RESET} {message}")

    def warning(self, message):
        print(f"    {Colors.YELLOW}[WARNING]{Colors.RESET} {message}")

    def error(self, message):
        print(f"    {Colors.RED}[ERROR]{Colors.RESET} {message}")


class DjangoStarterGenerator():
    """Класс для создания и запуска проекта Django."""

    def __init__(self):
        """ Метод инициации класса DjangoStarterGenerator """
        self.project_name = 'core'
        self.superuser_email = 'admin@mysite.ru'
        self.superuser_password = ''
        self.secret_key = ''
        self.email_host = ''
        self.email_port = ''
        self.email_host_user = ''
        self.email_host_password = ''
        self.default_from_email = ''
        self.email_use_ssl = False
        self.email_use_tls = False
        self.telegram_token = ''
        self.admin_telegram_id = ''
        # Пути к файлам и папкам
        self.archive_path = 'sources.zip'
        self.src_folder = '../src/'
        self.env_path = '../src/.env'
        self.archive_settings_file = 'settings.py'
        self.archive_views_file = 'views.py'
        self.archive_urls_file = 'urls.py'
        self.archive_gitignore_file = '.gitignore'

    def is_valid_password(self, password):
        """Метод проверки соответствия пароля заданным требованиям."""
        logger = Logger()
        if len(password) < 8:
            logger.error(Messages.PASSWORD_ERRORS[0])
            return False
        if not re.search(r'[A-Z]', password):
            logger.error(Messages.PASSWORD_ERRORS[1])
            return False
        if not re.search(r'[a-z]', password):
            logger.error(Messages.PASSWORD_ERRORS[2])
            return False
        if not re.search(r'\d', password):
            logger.error(Messages.PASSWORD_ERRORS[3])
            return False
        # if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        #     logger.error(Messages.PASSWORD_ERRORS[4])
        #     return False
        if ' ' in password:
            logger.error(Messages.PASSWORD_ERRORS[5])
            return False
        return True

    def get_project_name(self):
        """
        Метод получения названия проекта.
        """
        project_name = input(
            f'    Введите название проекта (нажмите Enter для использования "{Colors.CYAN}{self.project_name}{Colors.RESET}"): ')
        if project_name.strip() != '':
            self.project_name = project_name.strip()

    def get_superuser_data(self):
        """
        Метод получения данных суперпользователя (email и пароль).
        """
        logger = Logger()
        message = Messages.PASSWORD_REQUIREMENTS
        print_message = Messages(message=message, color=Colors.CYAN)
        print_message.print_message()
        # Запрос email пользователя.
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        while True:
            superuser_email = input(f'    Введите email суперпользователя (нажмите Enter для использования "{
                                    Colors.CYAN}{self.superuser_email}{Colors.RESET}"): ')
            if superuser_email.strip() == '':
                superuser_email = self.superuser_email
            if re.match(email_pattern, superuser_email):
                self.superuser_email = superuser_email.strip()
                break
            else:
                logger.error(f"""Некорректный email. Пожалуйста, введите действительный email в формате {
                             Colors.CYAN}user@mymail.ru{Colors.RESET} \n""")
        # Запрос пароля.
        password = self.superuser_password
        while password == '':
            password1 = getpass("    Введите пароль: ")
            password2 = getpass("    Введите пароль еще раз: ")
            if password1 != password2:
                logger.error('Пароли не совпадают. \n')
                continue
            if self.is_valid_password(password1):
                self.superuser_password = password1
                password = password1

    def get_email_server_settings(self):
        """

        """

    def get_email_server_settings(self):
        """
        Метод запроса настроек почтового сервера.
        """
        logger = Logger()
        message = Messages.EMAIL_SETUP_START
        print_message = Messages(message=message, color=Colors.CYAN)
        print_message.print_message()

        while True:
            setup_now = input(
                f"    Хотите ли вы сразу настроить почтовый сервер? {Colors.CYAN}(y/n){Colors.RESET}: ").strip().lower()

            if setup_now == 'y':
                self.email_host = input(
                    f"""\n    Введите адрес сервера для отправки почты (SMTP) (например, "{Colors.CYAN}smtp.dsg.pro{Colors.RESET}"): """).strip().lower()
                self.email_port = input(
                    f"""\n    Введите порт (например, с SSL - "{Colors.CYAN}465{Colors.RESET}", без шифрования - "{Colors.CYAN}25{Colors.RESET}" или "{Colors.CYAN}2525{Colors.RESET}"): """).strip()
                self.email_host_user = input(
                    f"""\n    Введите логин (имя пользователя) (например, "{Colors.CYAN}info@dsg.pro{Colors.RESET}"): """).strip()
                self.email_host_password = getpass(
                    f"""\n    Введите пароль: """).strip()
                self.default_from_email = input(
                    f"""\n    Введите имя и email, которые будут использоваться в качестве отправителя
        (например, "{Colors.CYAN}Django Starter Generator <info@dsg.pro>{Colors.RESET}"): """).strip()

                # Сначала спрашиваем про SSL
                while True:
                    use_ssl = input(f"\n    Использовать SSL? {
                                    Colors.CYAN}(y/n){Colors.RESET}: ").strip().lower()
                    if use_ssl == 'y':
                        self.email_use_ssl = True
                        self.email_use_tls = False  # Устанавливаем TLS в False, если SSL True
                        break
                    elif use_ssl == 'n':
                        self.email_use_ssl = False
                        # Если SSL False, спрашиваем про TLS
                        while True:
                            use_tls = input(f"\n    Использовать TLS? {
                                            Colors.CYAN}(y/n){Colors.RESET}: ").strip().lower()
                            if use_tls == 'y':
                                self.email_use_tls = True
                                break
                            elif use_tls == 'n':
                                self.email_use_tls = False
                                break
                            else:
                                logger.error(
                                    "Некорректный ввод. Пожалуйста, введите 'y' или 'n'.")
                        break
                    else:
                        logger.error(
                            "Некорректный ввод. Пожалуйста, введите 'y' или 'n'.")

                break  # Выход из цикла после успешного ввода

            elif setup_now == 'n':
                message = Messages.EMAIL_SETUP_LATER
                Messages.reminds.append(
                    f'''Указать настройки почтового сервера в файле ".env",
                    чтобы приложение могло отправлять письма (нужно для подтверждения email новых пользователей)
                    ''')
                print_message = Messages(message=message, color=Colors.YELLOW)
                print_message.print_message()
                break  # Выход из цикла после выбора 'n'

            else:
                logger.error(
                    "Некорректный ввод. Пожалуйста, введите 'y' или 'n'.")

    def get_telegram_settings(self):
        """
        Метод запроса настроек Telegram.
        """
        logger = Logger()
        message = Messages.TELEGRAM_SETUP_START
        print_message = Messages(message=message, color=Colors.CYAN)
        print_message.print_message()
        while True:
            setup_now = input(
                f"    Хотите ли вы сразу настроить Telegram? {Colors.CYAN}(y/n){Colors.RESET}: ").strip().lower()
            if setup_now == 'y':
                self.telegram_token = input(
                    f"\n    Введите Telegram TOKEN, с которого будут отправляться уведомления: ").strip()
                self.admin_telegram_id = input(
                    f"\n    Введите Telegram ID администратора: ").strip()
                break  # Выход из цикла после успешного ввода
            elif setup_now == 'n':
                message = Messages.TELEGRAM_SETUP_LATER
                Messages.reminds.append(
                    f'''Указать настройки Telegram в файле ".env",
                    чтобы приложение могло отправлять администратору уведомления о регистрации новых пользователей
                    ''')
                print_message = Messages(message=message, color=Colors.YELLOW)
                print_message.print_message()
                break  # Выход из цикла после выбора 'n'
            else:
                logger.error(
                    "Некорректный ввод. Пожалуйста, введите 'y' или 'n'.")

    def get_initial_data(self):
        """ Метод формирования исходных данных """
        self.get_project_name()
        self.get_superuser_data()
        self.get_email_server_settings()
        self.get_telegram_settings()

    def initial_script(self):
        """ Метод создания нового проекта Django """
        logger = Logger()
        install_script = textwrap.dedent(f"""
                                                @echo off
                                                cd ..
                                                python -m venv env
                                                call env\\Scripts\\activate
                                                call python.exe -m pip install --upgrade pip
                                                pip install Django
                                                pip install python-dotenv
                                                pip install telepot
                                                pip install django-utils-six
                                                pip install typus
                                                pip install django-widget-tweaks
                                                pip freeze > requirements.txt
                                                mkdir src
                                                cd src
                                                mkdir static
                                                django-admin startproject {self.project_name} .
                                                """)
        # Создание bat файла
        script_file_path = '..\install_script.bat'
        with open(script_file_path, 'w') as file:
            file.write(install_script)
        # Запуск bat файла
        if os.path.exists(script_file_path):
            message = Messages.START_DEPLOYMENT
            print_message = Messages(message=message, color=Colors.GREEN)
            print_message.print_message()
            process = subprocess.Popen(script_file_path)
            try:
                while True:
                    if process.poll() is not None:
                        break
            except KeyboardInterrupt:
                process.kill()
        else:
            logger.error('Ошибка! Скрипт не обнаружен.')
        # Удаление bat файла
        os.remove(script_file_path)

    def start_script(self):
        """
        Метод создания скрипта для запуска проекта Django на Windows.
        """
        # Создание скрипта страта нового проекта Django
        start_script = textwrap.dedent(f"""
                            @echo off
                            cd ..
                            call env\\Scripts\\activate
                            cd src
                            python manage.py makemigrations
                            python manage.py migrate
                            set DJANGO_SUPERUSER_EMAIL={self.superuser_email}
                            set DJANGO_SUPERUSER_PASSWORD={self.superuser_password}
                            python manage.py createsuperuser --no-input
                            REM call env\\Scripts\\activate
                            REM cd src
                            python manage.py makemigrations
                            python manage.py migrate
                            start python manage.py runserver
                            start "" http://localhost:8000
                            """)
        # Создание bat файла
        start_script_path = '..\start_script.bat'
        with open(start_script_path, 'w') as file:
            file.write(start_script)
        # Запуск bat файла
        process = subprocess.Popen(start_script_path)
        try:
            while True:
                if process.poll() is not None:
                    break
        except KeyboardInterrupt:
            process.kill()
        # Удаление bat файла
        os.remove(start_script_path)
        utils = Utils()
        utils.clear()
        message = Messages.SUCCESS
        print_message = Messages(message=message, color=Colors.GREEN)
        print_message.print_message()

    def get_secret_key(self):
        """ Метод записи SECRET_KEY в файл .env """
        # находим SECRET_KEY в файле settings.py
        with open(f"{self.src_folder}{self.project_name}/{self.archive_settings_file}", "r") as file:
            for line in file:
                if line.startswith("SECRET_KEY"):
                    self.secret_key = line.strip()

    def unzip_sources(self):
        """
        Метод распаковки необходимых файлов для проекта.
        """
        # извлечение settings.py в папку src/project_name
        with zipfile.ZipFile(self.archive_path, 'r') as zip_file:
            zip_file.extract(self.archive_settings_file,
                             path=f"{self.src_folder}{self.project_name}")
        # извлечение views.py в папку src/project_name
        with zipfile.ZipFile(self.archive_path, 'r') as zip_file:
            zip_file.extract(self.archive_views_file,
                             path=f"{self.src_folder}{self.project_name}")
        # извлечение urls.py в папку src/project_name
        with zipfile.ZipFile(self.archive_path, 'r') as zip_file:
            zip_file.extract(self.archive_urls_file,
                             path=f"{self.src_folder}{self.project_name}")
        # извлечение gitignore и src в текущую папку
        with zipfile.ZipFile(self.archive_path, 'r') as zip_file:
            zip_file.extract(self.archive_gitignore_file, path='../')
        # Извлечение остальных файлов из архива
        with zipfile.ZipFile(self.archive_path, 'r') as zip_file:
            zip_file.extractall(path='../', members=[
                f for f in zip_file.namelist() if f.startswith('src/')])

    def set_all_env_variables(self):
        """ Метод создания и сохранения файла .env с параметрами конфигурации проекта. """
        env_content = textwrap.dedent(f"""
        # Секретный ключ
        {self.secret_key}

        # Разрешенные хосты
        ALLOWED_HOSTS = *

        # Режим отладки
        DEBUG = True

        # Имя базы данных
        DATABASE_NAME = 'db.sqlite3'

        # Настройки электронной почты
        EMAIL_HOST = '{self.email_host}'
        EMAIL_PORT = '{self.email_port}'
        EMAIL_HOST_USER = '{self.email_host_user}'
        EMAIL_HOST_PASSWORD = '{self.email_host_password}'
        DEFAULT_FROM_EMAIL = '{self.default_from_email}'
        EMAIL_USE_TLS = {self.email_use_tls}
        EMAIL_USE_SSL = {self.email_use_ssl}

        # Настройки Telegram с которого будут приходить уведомления
        TELEGRAM_TOKEN = '{self.telegram_token}'

        # Telegram администратора
        ADMIN_TELEGRAM_ID = '{self.admin_telegram_id}'
        """).strip()

        with open(self.env_path, mode="w", encoding="utf-8") as file:
            file.write(env_content)

    def set_project_name(self):
        """ Метод внесения имени проекта в необходимых местах для корректной работы проекта. """
        # В файле settings.py
        with open(f"{self.src_folder}{self.project_name}/settings.py", mode="r", encoding="utf-8") as file:
            lines = file.readlines()

        for i in range(len(lines)):
            lines[i] = lines[i].replace("<project_name>", self.project_name)

        with open(f"{self.src_folder}{self.project_name}/settings.py", mode="w", encoding="utf-8") as file:
            file.writelines(lines)

        # В файле urls.py
        with open(f"{self.src_folder}{self.project_name}/urls.py", mode="r", encoding="utf-8") as file:
            lines = file.readlines()

        for i in range(len(lines)):
            lines[i] = lines[i].replace("<project_name>", self.project_name)

        with open(f"{self.src_folder}{self.project_name}/urls.py", mode="w", encoding="utf-8") as file:
            file.writelines(lines)

        # В файле communications/views.py
        with open(f"{self.src_folder}communications/views.py", mode="r", encoding="utf-8") as file:
            lines = file.readlines()

        for i in range(len(lines)):
            lines[i] = lines[i].replace("<project_name>", self.project_name)

        with open(f"{self.src_folder}communications/views.py", mode="w", encoding="utf-8") as file:
            file.writelines(lines)

    def final_reminds(self):
        """
        Метод, который выводит напоминания о необходимых действиях после создания проекта.
        """
        if Messages.reminds:  # Проверяем, не пустой ли список
            message = f"""
            Внимание! Вы отложили некоторые настройки на потом.

            Не забудьте:\n
            """
            for remind in Messages.reminds:
                # Добавляем напоминания в нужном формате
                message += f'- {remind}\n'

            print_message = Messages(message=message, color=Colors.YELLOW)
            print_message.print_message()
        else:
            pass  # Если список пустой, ничего не делаем

    def delete_dsg_folder(self):
        """Метод удаления папки dsg, чтобы остался только чистый проект"""
        # Получаем путь к директории dsg.
        dsg_folder = os.getcwd()
        for attempt in range(5):  # Попытка удалить 5 раз
            try:
                shutil.rmtree(dsg_folder)
                # print(f"Директория '{dsg_folder}' успешно удалена.")
                return
            except Exception as e:
                # print(f"Ошибка при удалении директории: {e}")
                time.sleep(1)  # Задержка перед повторной попыткой

    def main(self):
        # Приветствие пользователя.
        message = Messages.GREETING
        utils = Utils()
        utils.clear()
        print(Messages.HERO)
        print_message = Messages(message=message, color=Colors.GREEN)
        print_message.print_message()
        # Создание, настройка и запуск проекта.
        self.get_initial_data()
        self.initial_script()
        self.get_secret_key()
        self.unzip_sources()
        self.set_all_env_variables()
        self.set_project_name()
        self.start_script()
        # Напоминания.
        self.final_reminds()
        # Запрос окончания работы.
        print("\n", Messages.HERO)
        input(
            f"\n    Нажмите {Colors.CYAN}Enter{Colors.RESET} для завершения программы...")
        # Удаляем исходники, оставляя чистый проект.
        self.delete_dsg_folder()


# ========================= Основные алгоритмы =========================== #
if __name__ == '__main__':
    dsg = DjangoStarterGenerator()
    dsg.main()
# ======================================================================== #
