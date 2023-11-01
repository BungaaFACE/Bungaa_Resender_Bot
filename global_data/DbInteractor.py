import sqlite3
from os.path import abspath, dirname, join
from CONFIGURATION import SQLITE3_FILENAME

DB_FILEPATH = join(dirname(abspath(__file__)), SQLITE3_FILENAME)


class DbInteractor:
    def __init__(self) -> None:
        self.connect = sqlite3.connect(DB_FILEPATH)
        with open(join(dirname(abspath(__file__)), 'create_tables.sql'), encoding='utf-8') as generate_tables_file:
            generate_tables_sql = generate_tables_file.read()
        cursor = self.connect.cursor()
        cursor.executescript(generate_tables_sql)
        self.connect.commit()
        del cursor

    def get_items(self, table, columns='*', filter1='', value1='', filter2='', value2='', to_dict=False, to_list=False):
        cursor = self.connect.cursor()
        if to_list:
            cursor.row_factory = lambda cursor, row: row[0]
        sql_exec = f"SELECT {columns} FROM {table}"
        if filter1 and value1:
            sql_exec += f' WHERE {filter1}={value1}'
            if filter2 and value2:
                sql_exec += f' AND {filter2}={value2}'
        print(sql_exec)
        cursor.execute(sql_exec)
        results = list(cursor.fetchall())
        if to_dict:
            table_columns = [d[0] for d in cursor.description]
            results = [dict(zip(table_columns, result)) for result in results]
        cursor.close()
        return results

    def custom_command(self, sql_exec, to_dict=False, to_list=False):
        print(sql_exec)
        cursor = self.connect.cursor()
        if to_list:
            cursor.row_factory = lambda cursor, row: row[0]
        cursor.execute(sql_exec)
        results = list(cursor.fetchall())
        self.connect.commit()
        if to_dict and results:
            table_columns = [d[0] for d in cursor.description]
            results = [dict(zip(table_columns, result)) for result in results]
        cursor.close()
        return results


if __name__ == "__main__":
    db = DbInteractor()
