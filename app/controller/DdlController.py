from app.tools import imysql, istring
from app.tools.iobject import iObject
from ddlparse.ddlparse import DdlParse
from BaseController import BaseController


class DdlController(BaseController):

    def ddl2database(self):
        s = self.getValue('s')
        if s is None or s != 'test':
            return ''

        databases = imysql.list_databases()
        return self.asJson(databases)

    def ddl2table(self):
        database = self.getValue('s')
        if database is None:
            return ''

        tables = imysql.list_tables(database)
        return self.asJson(tables)

    def show(self, cla_type, database, table_name, title='DevTools!!', logo='logo'):
        ajax = int(self.getValue('ajax', 0))

        table_ddl = imysql.table(table_name, database).get_ddl()
        if table_ddl is False:
            return 'Something Wrong!!'
        table_comment = imysql.table(table_name, database).get_comment()
        result = DdlParse().parse(table_ddl)

        obj = iObject(istring.ucwords(table_name))
        obj.set_comment(table_comment)
        for col in result.columns.values():
            obj.add_attr(col)

        code = obj.to_string('java')
        if ajax == 1:
            return self.asJson(code)
        else:
            return self.render('code', code=code, title=title, logo='ddl2bean')

    def ddl2bean(self):
        title = 'Ddl2Bean!!'
        logo = 'ddl2bean'

        s = self.getValue('s')
        if s is not None:
            s = s.split('.')
            return self.show('bean', s[0], s[1], title, logo)

        uri = 'ddl2bean'
        return self.render('ddl2', title=title, logo=logo, uri=uri)

    def ddl2model(self):
        title = 'Ddl2Model!!'
        logo = 'ddl2model'

        s = self.getValue('s')
        if s is not None:
            s = s.split('.')
            return self.show('model', s[0], s[1], title, logo)

        uri = 'ddl2model'
        return self.render('ddl2', title=title, logo=logo, uri=uri)

    def ddl2entity(self):
        title = 'Ddl2Entity!!'
        logo = 'ddl2entity'

        s = self.getValue('s')
        if s is not None:
            s = s.split('.')
            return self.show('entity', s[0], s[1], title, logo)

        uri = 'ddl2entity'
        return self.render('ddl2', title=title, logo=logo, uri=uri)

    def ddl2info(self):
        title = 'Ddl2Info!!'
        logo = 'ddl2info'

        s = self.getValue('s')
        if s is not None:
            s = s.split('.')
            return self.show('info', s[0], s[1], title, logo)

        uri = 'ddl2info'
        return self.render('ddl2', title=title, logo=logo, uri=uri)
