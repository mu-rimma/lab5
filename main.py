import PySimpleGUI as sg
import sys


class Logger:
    __instance = None

    @staticmethod
    def get_instance():
        if Logger.__instance is None:
            Logger.__instance = Logger()
        return Logger.__instance

    def log_info(self, message):
        print(f'[INFO]: {message}')

    def log_warning(self, message):
        print(f'[WARNING]: {message}')

    def log_error(self, message):
        print(f'[ERROR]: {message}', file=sys.stderr)


class Decorator:
    def __init__(self, logger):
        self.__logger = logger

    def log_info_to_file(self, filename, message):
        with open(filename, 'a') as file:
            file.write(f'[INFO]: {message}\n')
        self.__logger.log_info(message)

    def log_warning_to_file(self, filename, message):
        with open(filename, 'a') as file:
            file.write(f'[WARNING]: {message}\n')
        self.__logger.log_warning(message)

    def log_error_to_file(self, filename, message):
        with open(filename, 'a') as file:
            file.write(f'[ERROR]: {message}\n')
        self.__logger.log_error(message)

    def log_error_to_stderr(self, message):
        self.__logger.log_error(message)


# Создаем список элементов для первой вкладки
tab1_layout = [
    [sg.Text('Введите значение веса:')],
    [sg.Input(key='-INPUT-')],
    [sg.Button('Конвертировать')],
    [sg.Button('Сбросить')]
]

# Создаем список элементов для второй вкладки
tab2_layout = [
    [sg.Text('Выберите единицу измерения:')],
    [sg.Combo(['Килограммы в фунты', 'Фунты в килограммы', 'Килограммы в граммы'], key='-OPTION-')],
    [sg.Button('Выбрать')],
    [sg.Button('Сбросить вариант конвертации')]
]

# Создаем список элементов для третьей вкладки
tab3_layout = [
    [sg.Text('Результат:', size=(15, 1), justification='center')],
    [sg.Text(size=(40, 1), key='-RESULT-')]
]

# Создаем вкладки
tab_group_layout = [
    [sg.Tab('Вес', tab1_layout), sg.Tab('Единица измерения', tab2_layout), sg.Tab('Результат', tab3_layout)]
]

# Создаем окно приложения
layout = [[sg.TabGroup(tab_group_layout)]]
window = sg.Window('Конвертер веса', layout)

# Создаем экземпляр класса Logger
logger = Logger.get_instance()

# Создаем экземпляр класса Decorator
decorator = Decorator(logger)

# Обработка событий
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break

    elif event == 'Сбросить':
        window['-INPUT-'].update('')
        window['-RESULT-'].update('')

    elif event == 'Сбросить вариант конвертации':
        window['-OPTION-'].update('')
        window['-RESULT-'].update('')

    elif event == 'Выбрать':
        try:
            if values['-OPTION-'] == 'Килограммы в фунты':
                result = float(values['-INPUT-']) * 2.20462
            elif values['-OPTION-'] == 'Фунты в килограммы':

                result = float(values['-INPUT-']) * 2.20462

            elif values['-OPTION-'] == 'Килограммы в граммы':

                result = float(values['-INPUT-']) * 1000
            window['-RESULT-'].update(f'Вес: {result}')
            decorator.log_info_to_file('log.txt', f'Конвертация {values["-OPTION-"]}:{result}')
        except Exception as e:
            decorator.log_error_to_file('log.txt', str(e))
            decorator.log_error_to_stderr(str(e))

window.close()
