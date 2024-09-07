import os
import re
import subprocess
import zipfile
from getpass import getpass


class DjangoStarterGenerator():
    """Класс для создания и запуска проекта Django."""

    def __init__(self):
        self.project_name = 'core'
        self.superuser_email = 'admin@mysite.ru'
        self.superuser_password = ''

    def is_valid_password(password):
        """Проверяет, соответствует ли пароль заданным требованиям."""
        if len(password) < 8:
            print("Пароль должен содержать не менее 8 символов.")
            return False
        if not re.search(r'[A-Z]', password):
            print("Пароль должен содержать хотя бы одну заглавную букву.")
            return False
        if not re.search(r'[a-z]', password):
            print("Пароль должен содержать хотя бы одну строчную букву.")
            return False
        if not re.search(r'\d', password):
            print("Пароль должен содержать хотя бы одну цифру.")
            return False
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            print("Пароль должен содержать хотя бы один специальный символ.")
            return False
        if ' ' in password:
            print("Пароль не должен содержать пробелов.")
            return False
        return True

    def get_project_name(self):
        """
        Запрашивает у пользователя название проекта.

        Метод выводит сообщение с просьбой ввести название проекта. 
        Если пользователь оставляет поле пустым и нажимает Enter, 
        используется текущее значение атрибута self.project_name в качестве названия проекта.

        Примечание:
            В названии проекта не рекомендуется использовать пробелы - они будут удалены 
            перед присвоением значения атрибуту self.project_name.
        """
        project_name = input(
            f'Введите название проекта (нажмите Enter для использования "{self.project_name}"): ')

        if project_name.strip() != '':
            self.project_name = project_name.strip()

    def get_superuser_data(self):
        """
        Запрашивает у пользователя данные суперпользователя, включая email и пароль.

        Этот метод выполняет следующие действия:
        1. Запрашивает у пользователя ввод email суперпользователя. Если пользователь не вводит email и нажимает Enter, используется предустановленный email.
        2. Запрашивает у пользователя ввод пароля дважды для подтверждения. Если введенные пароли не совпадают, пользователь получает соответствующее сообщение об ошибке и может повторить попытку ввода.
        3. Проверяет, соответствует ли введенный пароль заданным требованиям с помощью метода is_valid_password. Если пароль не соответствует требованиям, выводится сообщение об ошибке, и пользователь может повторить попытку ввода.
        """
        # Запрос email пользователя.
        superuser_email = input(f'Введите email суперпользователя (нажмите Enter для использования "{
            self.superuser_email}"): ')
        if superuser_email.strip() != '':
            self.superuser_email = superuser_email.strip()
        while password == '':
            password1 = getpass("Введите пароль: ")
            password2 = getpass("Введите пароль еще раз: ")
            if password1 == password2:
                password = password1
            else:
                print('Пароли не совпадают. \n')
        # Запрос пароля.
        password = self.superuser_password
        while password == '':
            password1 = getpass("Введите пароль: ")
            password2 = getpass("Введите пароль еще раз: ")

            if password1 != password2:
                print('Пароли не совпадают. \n')
                continue

            if self.is_valid_password(password1):
                self.superuser_password = password1
            else:
                print(
                    'Пароль не соответствует требованиям. Пожалуйста, попробуйте снова.\n')

    def get_email_server_settings(self):
        pass

    def get_telegram_settings(self):
        pass

    def get_initial_data(self):
        self.get_project_name()
        self.get_superuser_data()
        self.get_email_server_settings()
        self.get_telegram_settings()


def get_initial_data(self):

    superuser = input('Введите имя суперпользователя (нажмите Enter для использования "admin"): ')\
        if superuser == '': \
        superuser = 'admin'\
        password = getpass('Введите пароль суперпользователя: ')\
        email = input('Введите email суперпользователя (нажмите Enter для использования "admin@admin.com"): ')\
        if email == '': \
        email = 'admin@admin.com'\
        return superuser, password, email


def initial_script_generator(self):
    project_name = input(
        'Введите название проекта (нажмите Enter для использования "core"): ')
    if project_name == '':
        self.project_name = 'core'
    else:
        self.project_name = project_name

    install_script = f"""
                        @echo off
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
                        django-admin startproject {project_name} .
                    """
    # Создание bat файла
    with open('install_script.bat', 'w') as file:
        file.write(install_script)
    # Запуск bat файла
    process = subprocess.Popen('install_script.bat')
    try:
        while True:
            if process.poll() is not None:
                break
    except KeyboardInterrupt:
        process.kill()
    # Удаление bat файла
    os.remove('install_script.bat')


def create_and_execute_install_bat_file(project_name='core'):
    """
    Функция создания bat-скрипта для создания проекта Django и его исполнения.

    :param project_name: имя проекта Django, по умолчанию 'core'
    :return: None
    """

    # Создание скрипта для bat файла
    install_script = f"""
                         @echo off
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
                         django-admin startproject {project_name} .
                      """

    # Создание bat файла
    with open('install_script.bat', 'w') as file:
        file.write(install_script)

    # Запуск bat файла
    process = subprocess.Popen('install_script.bat')
    try:
        while True:
            if process.poll() is not None:
                break
    except KeyboardInterrupt:
        process.kill()

    # Удаление bat файла
    os.remove('install_script.bat')


def create_and_execute_start_bat_file(project_name, superuser, password):
    """
    Функция создания скрипта для запуска проекта Django на Windows.

    :param project_name: имя проекта Django
    :param superuser: имя суперпользователя
    :param password: пароль суперпользователя
    :return: None
    """

    # Создание скрипта для bat файла
    start_script = f"""
                       @echo off
                       del start_django_win.py
                       del install_sources.zip
                       del create_project_conifrm_email.bat
                       call env\\Scripts\\activate
                       cd src
                       python manage.py makemigrations
                       python manage.py migrate
                       cls
                       python manage.py createsuperuser --username {superuser} --password {password}
                       cd src
                       start python manage.py runserver
                       start "" http://localhost:8000
                    """

    # Создание bat файла
    with open('start_script.bat', 'w') as file:
        file.write(start_script)

    # Запуск bat файла
    process = subprocess.Popen('start_script.bat')
    try:
        while True:
            if process.poll() is not None:
                break
    except KeyboardInterrupt:
        process.kill()

    # Удаление bat файла
    os.remove('start_script.bat')


def unzip_install_sources():
    """
    Функция распаковки необходимых файлов для проекта.
    """

    archive_path = 'install_sources.zip'
    src_folder = 'src/'
    settings_file = 'settings.py'
    views_file = 'views.py'
    urls_file = 'urls.py'
    gitignore_file = '.gitignore'

    # извлечение settings.py в папку src/project_name
    with zipfile.ZipFile(archive_path, 'r') as zip_file:
        zip_file.extract(settings_file, path=f"src/{project_name}")

    # извлечение views.py в папку src/project_name
    with zipfile.ZipFile(archive_path, 'r') as zip_file:
        zip_file.extract(views_file, path=f"src/{project_name}")

    # извлечение urls.py в папку src/project_name
    with zipfile.ZipFile(archive_path, 'r') as zip_file:
        zip_file.extract(urls_file, path=f"src/{project_name}")

    # извлечение gitignore и src в текущую папку
    with zipfile.ZipFile(archive_path, 'r') as zip_file:
        zip_file.extract(gitignore_file, path='.')
        # zip_file.extract(src_folder, path='.')
        zip_file.extractall(path='.', members=[
                            f for f in zip_file.namelist() if f.startswith(src_folder)])


def find_secret_key():
    """
    Функция поиска ключа безопасности в файле настроек проекта settings.py.
    """

    secret_key = ''
    with open(f"src/{project_name}/settings.py", "r") as file:
        for line in file:
            if line.startswith("SECRET_KEY"):
                secret_key = line.strip()
                return secret_key
    return secret_key


def set_secret_key(secret_key):
    """
    Функция изменения значения переменной SECRET_KEY в файле .env проекта.
    """

    with open("src/.env", mode="r", encoding="utf-8") as file:
        lines = file.readlines()

    for i in range(len(lines)):
        if lines[i].startswith("SECRET_KEY ="):
            lines[i] = f"{secret_key}\n"
            break

    with open("src/.env", mode="w", encoding="utf-8") as file:
        file.writelines(lines)


def set_project_name(project_name):
    """
    Функция прописывания имени проекта в необходимых местах.
    """

    # В файле settings.py
    with open(f"src/{project_name}/settings.py", mode="r", encoding="utf-8") as file:
        lines = file.readlines()

    for i in range(len(lines)):
        lines[i] = lines[i].replace("<project_name>", project_name)

    with open(f"src/{project_name}/settings.py", mode="w", encoding="utf-8") as file:
        file.writelines(lines)

    # В файле urls.py
    with open(f"src/{project_name}/urls.py", mode="r", encoding="utf-8") as file:
        lines = file.readlines()

    for i in range(len(lines)):
        lines[i] = lines[i].replace("<project_name>", project_name)

    with open(f"src/{project_name}/urls.py", mode="w", encoding="utf-8") as file:
        file.writelines(lines)

    # В файле communications/views.py
    with open(f"src/communications/views.py", mode="r", encoding="utf-8") as file:
        lines = file.readlines()

    for i in range(len(lines)):
        lines[i] = lines[i].replace("<project_name>", project_name)

    with open(f"src/communications/views.py", mode="w", encoding="utf-8") as file:
        file.writelines(lines)


# ========================= Основные алгоритмы =========================== #
if __name__ == '__main__':
    # Обновление pip
    subprocess.run(['python', '-m', 'pip', 'install', '--upgrade', 'pip'])
    os.system('cls')

    # Запрос имени проекта
    # project_name = input('Введите наименование проекта: ')
    project_name = 'core'

    # # Запрос e-mail суперпользователя
    superuser = ''
    # superuser = input('Введите e-mail суперпользователя: ')

    # # Запрос пароля суперпользователя 1
    password = ''
    # while password == '':
    #     password1 = getpass("Введите пароль: ")
    #     password2 = getpass("Введите пароль еще раз: ")
    #     if password1 == password2:
    #         password = password1
    #     else:
    #         print('Пароли не совпадают. \n')

    # Создание проекта
    create_and_execute_install_bat_file(project_name)

    # Настройка проекта
    secret_key = find_secret_key()
    unzip_install_sources()
    set_secret_key(secret_key)
    set_project_name(project_name)

    # Запуск проекта
    create_and_execute_start_bat_file(project_name, superuser, password)
# ======================================================================== #
