import pymysql
from os import environ

mysql_conn = pymysql.connect(
    host=environ.get('MYSQL_HOST'),
    user=environ.get('MYSQL_USER'),
    password=environ.get('MYSQL_PASS'),
    database=environ.get('MYSQL_DB'),
    charset="utf8"
)

mysql_cursor = mysql_conn.cursor(cursor=pymysql.cursors.DictCursor)


class table():
    conn = None
    cursor = None
    table = None
    database = None

    def __init__(self, table_name, database=None):
        self.conn = mysql_conn
        self.cursor = mysql_cursor
        self.table = table_name
        if database is not None:
            self.database = database
            self.conn.select_db(database)

    def genSetter(self, data):
        s = ''
        for x in data:
            s += "`{}`='{}',".format(x, data[x])

        s = s[0:-1]
        return s

    def genFieldsAndPlaceHolder(self, data):
        if type(data) is dict:
            data = [data]

        fields = '('
        placeholder = '('
        for x in data[0]:
            fields += "`{}`,".format(x)
            placeholder += "%s,"

        fields = fields[0:-1] + ')'
        placeholder = placeholder[0:-1] + ')'
        return (fields, placeholder)

    def genValues(self, data):
        if type(data) is dict:
            data = [data]

        values = []
        for row in data:
            item = []
            for x in row:
                item.append(row[x])
            values.append(item)

        return tuple(values)

    def genWhere(self, condition, withWhere=False):
        s = ''
        for key in condition:
            value = condition[key]
            if type(value) is not list:
                operate = '='
                value = "'{}'".format(value)
            else:
                operate = " {} ".format(value[0])
                value = value[1]
                if operate == ' in ':
                    value = "('{}')".format("','".join(value))
                elif operate == ' between ':
                    value = "{} and {}".format(value[0], value[1])
                else:
                    value = "'{}'".format(value)

            s += " AND `{}`{}{}".format(key, operate, value)

        s = s[5:]
        return s if withWhere is False else ' WHERE ' + s

    def find(self, condition={}, orders='', limit=''):
        sql = "SELECT * FROM {table}{where}{orders}{limit}".format(
            table=self.table,
            where=self.genWhere(condition, True) if len(condition) > 0 else '',
            orders=" ORDER BY " + orders if orders != '' else '',
            limit=" LIMIT " + limit if limit != '' else ''
        )
        self.cursor.execute(sql)
        return self.cursor

    def find_one(self, condition):
        result = self.find(condition, '', '0,1').fetchone()
        return result

    def update_many(self, condition, data, limit=0):
        sql = "UPDATE {table} SET {setter} WHERE {where}{limit}".format(
            table=self.table,
            setter=self.genSetter(data),
            where=self.genWhere(condition),
            limit=" LIMIT " + str(limit) if limit == 0 else ''
        )
        try:
            effect = self.cursor.execute(sql)
            self.conn.commit()
            return effect
        except Exception as e:
            self.conn.rollback()
            print('imysql 批量更新错误')
            print(sql)
            print(e)
            return False

    def update_one(self, condition, data):
        return self.update_many(condition, data, 1)

    def insert_many(self, data):
        tmp = self.genFieldsAndPlaceHolder(data)
        sql = "INSERT INTO {table} {fields} VALUES {placeholder}".format(
            table=self.table,
            fields=tmp[0],
            placeholder=tmp[1]
        )
        values = self.genValues(data)
        try:
            effect = self.cursor.executemany(sql, values)
            self.conn.commit()
            return effect
        except Exception as e:
            self.conn.rollback()
            print('imysql 批量写入失败')
            print(e)
            return False

    def get_ddl(self):
        sql = 'SHOW CREATE TABLE {}'.format(self.table)
        try:
            self.cursor.execute(sql)
        except Exception as e:
            print(e)
            return False
        result = self.cursor.fetchone()
        return result['Create Table'] if result else ''

    def get_comment(self):
        sql = """
            SELECT
                table_name,
                table_comment
            FROM
                information_schema.TABLES
            WHERE
                table_schema = '%s'
            AND table_name = '%s';
        """
        sql = sql % (self.database, self.table)
        try:
            self.cursor.execute(sql)
        except Exception as e:
            print(e)
            return False
        result = self.cursor.fetchone()
        return result['table_comment'] if result else ''


def list_databases():
    sql = 'SHOW DATABASES'
    try:
        mysql_cursor.execute(sql)
    except Exception as e:
        print(e)
        return False
    result = []
    for x in mysql_cursor:
        if x['Database'] in ('information_schema', 'mysql', 'performance_schema'):
            continue
        result.append(x['Database'])
    return result if result else ''


def list_tables(database):
    if database in ('information_schema', 'mysql', 'performance_schema'):
        return False

    sql = 'SHOW TABLES'
    try:
        mysql_conn.select_db(database)
        mysql_cursor.execute(sql)
    except Exception as e:
        print(e)
        return False

    field = 'Tables_in_' + database
    result = []
    for x in mysql_cursor:
        result.append(x[field])
    return result if result else ''
