import neo4jTools
import argparse_settings

if __name__ == "__main__":
    # подключение к СУБД (по умолчанию она разворачивается на 7687 порту, пользователя надо создать в СУБД)
    # user - логин существующего пользователя в СУБД, password - его пароль
    conn = neo4jTools.Neo4jConnection(uri="bolt://localhost:7687", user="Anton_Korsunov", password="123456789")
    ARGS = argparse_settings.get_argparse_settings()  # Заполненное пространство имен из argparse

    dbs = ARGS.dbs

    if ARGS.export is not None:
        conn.export(dbs, ARGS.export)

    if ARGS.import_ is not None:
        conn.import_(dbs, ARGS.import_)

    if ARGS.command is not None:
        conn.query(ARGS.command, db=dbs)

    if ARGS.DBSprint:
        print(conn.query("MATCH (n) RETURN n", db=dbs))
