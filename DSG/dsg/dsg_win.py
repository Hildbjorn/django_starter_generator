import os
import re
import subprocess
import textwrap
import zipfile
from getpass import getpass


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


class Messages:
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


class Logger:
    def info(self, message):
        print(f"{Colors.GREEN}[INFO]{Colors.RESET} {message}")

    def warning(self, message):
        print(f"{Colors.YELLOW}[WARNING]{Colors.RESET} {message}")

    def error(self, message):
        print(f"{Colors.RED}[ERROR]{Colors.RESET} {message}")


class Utils():
    """
    Класс Utils содержит общие утилитарные методы для работы Django Starter Generator.
    """

    def __init__(self, message=None):
        self.message = message

    def clear(self):
        # Для Windows
        if os.name == 'nt':
            os.system('cls')
        # Для Unix-подобных систем
        else:
            os.system('clear')

    def print_message(self):
        """
        Вывод сообщения
        """
        lines = self.message.split('\n')
        # очистка каждой строки от пробелов в начале и в конце
        lines = [line.strip() for line in lines]
        # заменяем табуляции на 4 пробела
        lines = [line.replace('\t', '    ') for line in lines]
        max_len = max(len(line) for line in lines)
        print(f"\n{Colors.YELLOW}   ╭{'─' * (max_len + 4)}╮")
        for line in lines:
            print(f"   │  {line.ljust(max_len)}  │")
        print(f".oO╰{'─' * (max_len + 4)}╯{Colors.RESET}\n")


class DjangoStarterGenerator():
    """Класс для создания и запуска проекта Django."""

    def __init__(self):
        self.project_name = 'core'
        self.superuser_email = 'admin@mysite.ru'
        self.superuser_password = ''
        self.email_host = None
        self.email_port = None
        self.email_host_user = None
        self.email_host_password = None
        self.default_from_email = None
        self.email_use_ssl = False
        self.email_use_tls = False
        self.telegram_token = None
        self.admin_telegram_id = None

    def is_valid_password(self, password):
        """Проверяет, соответствует ли пароль заданным требованиям."""
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
        Получает название проекта.
        """
        project_name = input(
            f'    Введите название проекта (нажмите Enter для использования "{Colors.CYAN}{self.project_name}{Colors.RESET}"): ')

        if project_name.strip() != '':
            self.project_name = project_name.strip()

    def get_superuser_data(self):
        """
        Получает данные суперпользователя (email и пароль).
        """
        logger = Logger()
        message = Messages.PASSWORD_REQUIREMENTS
        utils = Utils(message)
        utils.print_message()
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
                logger.error('    Пароли не совпадают. \n')
                continue
            if self.is_valid_password(password1):
                self.superuser_password = password1
                password = password1

    def get_email_server_settings(self):
        """
        Запрашивает у пользователя настройки почтового сервера.
        """
        logger = Logger()
        message = Messages.EMAIL_SETUP_START
        utils = Utils(message)
        utils.print_message()
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
                f"""\n    Введите имя и email, которыt будет использоваться в качестве отправителя (например, "{Colors.CYAN}Django Starter Generator <info@dsg.pro>{Colors.RESET}"): """).strip()
            # Сначала спрашиваем про SSL
            use_ssl = input(f"\n    Использовать SSL? {
                            Colors.CYAN}(y/n){Colors.RESET}: ").strip().lower()
            if use_ssl == 'y':
                self.email_use_ssl = True
                self.email_use_tls = False  # Устанавливаем TLS в False, если SSL True
            elif use_ssl == 'n':
                self.email_use_ssl = False
                # Если SSL False, спрашиваем про TLS
                use_tls = input(f"\n    Использовать TLS? {
                                Colors.CYAN}(y/n){Colors.RESET}: ").strip().lower()
                if use_tls == 'y':
                    self.email_use_tls = True
                elif use_tls == 'n':
                    self.email_use_tls = False
                else:
                    logger.error(
                        "Некорректный ввод. Установлено значение TLS=False.")
                    self.email_use_tls = False
            else:
                logger.error(
                    "Некорректный ввод. Установлены значения по умолчанию: SSL=False, TLS=False.")
        elif setup_now == 'n':
            message = Messages.EMAIL_SETUP_LATER
            utils = Utils(message)
            utils.print_message()
        else:
            logger.error("Некорректный ввод. Пожалуйста, введите 'y' или 'n'.")

    def get_telegram_settings(self):
        """
        Запрашивает у пользователя настройки Telegram.
        """
        logger = Logger()
        message = Messages.TELEGRAM_SETUP_START
        utils = Utils(message)
        utils.print_message()
        setup_now = input(
            f"    Хотите ли вы сразу настроить почтовый сервер? {Colors.CYAN}(y/n){Colors.RESET}: ").strip().lower()
        if setup_now == 'y':
            self.telegram_token = input(
                f"\n    Введите Telegram TOKEN, с которого будут отправляться уведомления: ").strip()
            self.admin_telegram_id = input(
                f"\n    Введите Telegram ID администратора: ").strip()
        elif setup_now == 'n':
            message = Messages.TELEGRAM_SETUP_LATER
            utils = Utils(message)
            utils.print_message()
        else:
            logger.error("Некорректный ввод. Пожалуйста, введите 'y' или 'n'.")

    def get_initial_data(self):
        self.get_project_name()
        self.get_superuser_data()
        self.get_email_server_settings()
        self.get_telegram_settings()

    def initial_script(self):
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
            message = f"""{Messages.START_DEPLOYMENT}"""
            utils = Utils(message)
            utils.print_message()
            process = subprocess.Popen(script_file_path)
            try:
                while True:
                    if process.poll() is not None:
                        break
            except KeyboardInterrupt:
                process.kill()
        else:
            logger.error('    Ошибка! Скрипт не обнаружен.')
        # Удаление bat файла
        os.remove(script_file_path)

    def start_script(self):
        """
        Функция создания скрипта для запуска проекта Django на Windows.
        """
        pass

    def unzip_sources(self):
        """
        Функция распаковки необходимых файлов для проекта.
        """
        pass

    def main(self):
        # Приветствие пользователя.
        message = Messages.GREETING
        utils = Utils(message)
        utils.clear()
        print(Messages.HERO)
        utils.print_message()
        # Создание, настройка и запуск проекта.
        self.get_initial_data()
        self.initial_script()
        self.unzip_sources()
        self.start_script()
        # Сообщение об успешном создании проекта.
        message = Messages.SUCCESS
        utils = Utils(message)
        utils.print_message()


# ========================= Основные алгоритмы =========================== #
if __name__ == '__main__':
    dsg = DjangoStarterGenerator()
    dsg.main()
# ======================================================================== #
