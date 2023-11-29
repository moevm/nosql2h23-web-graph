import argparse


# Задание параметров запуска через консоль через argpasrse
def get_argparse_settings():
    parser = argparse.ArgumentParser(description='Тестовый пример работы Neo4j + Python')
    parser.add_argument('--dbs', default='test', type=str, help='Название выбранной бд')
    parser.add_argument('--export', default=None, type=str, help='Путь для экспорта БД')
    parser.add_argument('--import_', default=None, type=str, help='Путь для импорта БД')
    parser.add_argument('--command', default=None, type=str, help='Команда в формате Cypher Query')
    parser.add_argument('--DBSprint', default=False, type=bool, help='Надо ли выводить текущее состояние БД в консоль')

    return parser.parse_args()
