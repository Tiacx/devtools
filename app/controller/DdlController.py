from app.tools import imysql, istring
from app.tools.iobject import iObject
from ddlparse.ddlparse import DdlParse
from BaseController import BaseController


class DdlController(BaseController):

    def ddl2database(self):
        s = self.getValue('s')
        if s is None or s not in ('dev', 'test'):
            return ''

        imysql.conn(s)
        databases = imysql.list_databases()
        return self.asJson(databases)

    def ddl2table(self):
        database = self.getValue('s')
        if database is None:
            return ''

        tables = imysql.list_tables(database)
        return self.asJson(tables)

    def get_obj(self, database, table_name):
        environment = database[0:database.find('_')]
        imysql.conn(environment)
        table_ddl = imysql.table(table_name, database).get_ddl()
        if table_ddl is False:
            return self.error(500)
        else:
            # 处理英文逗号冲突
            table_ddl = table_ddl.replace(',\n', '-\n').replace(',', '，').replace('-\n', ',\n')
        table_comment = imysql.table(table_name, database).get_comment()
        result = DdlParse().parse(table_ddl)

        obj = iObject(table_name[table_name.find('_'):])
        obj.set_comment(table_comment)

        return (obj, result, table_ddl)

    def ddl2bean(self):
        title = 'Ddl2Bean!!'
        logo = 'ddl2bean'

        s = self.getValue('s')
        if s is not None:
            ajax = int(self.getValue('ajax', 0))
            s = s.split('.')
            tmp = self.get_obj(s[0], s[1])
            obj = tmp[0]
            result = tmp[1]

            obj.comment_compress = True
            obj.show_methods = False

            for col in result.columns.values():
                obj.add_attr(col)

            code = obj.to_string()
            if ajax == 1:
                return self.asJson(code)
            else:
                return self.render('code', code=code, title=title, logo=logo)

        uri = 'ddl2bean'
        return self.render('ddl2', title=title, logo=logo, uri=uri)

    def ddl2model(self):
        title = 'Ddl2Model!!'
        logo = 'ddl2model'

        s = self.getValue('s')
        if s is not None:
            ajax = int(self.getValue('ajax', 0))
            s = s.split('.')
            database = s[0]
            table_name = s[1]
            tmp = self.get_obj(database, table_name)
            obj = tmp[0]
            result = tmp[1]

            obj.set_name_extra('Model')
            obj.set_space('cn.wbiao.%s.rest.model' % (database[database.find('_')+1:]))
            obj.set_packages([
                'com.fasterxml.jackson.annotation.JsonFormat',
                'io.swagger.annotations.ApiModel',
                'io.swagger.annotations.ApiModelProperty',
                'org.hibernate.validator.constraints.Length',
                'org.hibernate.validator.constraints.NotEmpty',
                'org.hibernate.validator.constraints.Range',
                'java.util.Date'
            ])
            obj.set_class_decorators([
                '@ApiModel'
            ])
            for col in result.columns.values():
                if col.comment is None:
                    col.comment = col.name

                obj.add_attr(col)
                data_type = obj.gen_data_type(col.data_type)

                decorators = []
                decorators.append('@ApiModelProperty(value = "%s")' % (col.comment))
                if col.length:
                    if data_type in ('Short', 'Integer', 'Long'):
                        decorators.append('@Range(min = 0)')
                    else:
                        decorators.append('@Length(max = %s)' % (col.length))
                if col.not_null is True:
                    decorators.append('@NotEmpty')
                if data_type == 'Date':
                    decorators.append('@JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd HH:mm:ss", locale = "zh", timezone = "GMT+8")')
                obj.set_attr_decorator(col.name, decorators)

            code = obj.to_string()
            if ajax == 1:
                return self.asJson(code)
            else:
                return self.render('code', code=code, title=title, logo=logo)

        uri = 'ddl2model'
        return self.render('ddl2', title=title, logo=logo, uri=uri)

    def ddl2entity(self):
        title = 'Ddl2Entity!!'
        logo = 'ddl2entity'

        s = self.getValue('s')
        if s is not None:
            ajax = int(self.getValue('ajax', 0))
            s = s.split('.')
            database = s[0]
            table_name = s[1]
            tmp = self.get_obj(database, table_name)
            obj = tmp[0]
            result = tmp[1]

            database = database[database.find('_')+1:]
            obj.set_name_extra('Entity')
            obj.set_space('cn.wbiao.%s.dao.entities' % (database))
            obj.set_packages([
                'cn.wbiao.framework.core.data.AbstractEntity',
                'cn.wbiao.framework.core.data.ColumnName',
                'javax.persistence.*',
                'java.util.Date'
            ])
            obj.set_class_decorators([
                '@Entity(name = "%s.%s")' % (database, istring.ucwords(table_name[table_name.find('_'):])),
                '@Table(name = "%s")' % (table_name),
            ])
            obj.set_extends('AbstractEntity')
            for col in result.columns.values():
                comment = col.comment
                if comment is None:
                    comment = col.name

                # 不显示注释
                col.comment = None
                obj.add_attr(col)
                data_type = obj.gen_data_type(col.data_type)

                decorators = []
                if col.primary_key is True or comment.find('自增') > -1:
                    decorators.append('@Id')
                    decorators.append('@GeneratedValue(strategy = GenerationType.IDENTITY)')

                s = '@Column(name = "%s"' % (col.name)
                if col.not_null is True:
                    s += ', nullable = false'
                if col.length:
                    if data_type in ('String', 'DataTypeWithBLOBs.String'):
                        s += ', length = %s' % (col.length)
                s += ')'
                decorators.append(s)
                decorators.append('@ColumnName("%s")' % (comment))
                obj.set_attr_decorator(col.name, decorators)

            code = obj.to_string()
            if ajax == 1:
                return self.asJson(code)
            else:
                return self.render('code', code=code, title=title, logo=logo)

        uri = 'ddl2entity'
        return self.render('ddl2', title=title, logo=logo, uri=uri)

    def ddl2info(self):
        title = 'Ddl2Info!!'
        logo = 'ddl2info'

        s = self.getValue('s')
        if s is not None:
            ajax = int(self.getValue('ajax', 0))
            s = s.split('.')
            database = s[0]
            table_name = s[1]
            tmp = self.get_obj(database, table_name)
            obj = tmp[0]
            result = tmp[1]

            database = database[database.find('_')+1:]
            obj.set_name_extra('Info')
            obj.set_space('cn.wbiao.%s.api.info' % (database))
            obj.set_packages([
                'com.fasterxml.jackson.annotation.JsonFormat',
                'io.swagger.annotations.ApiModel',
                'io.swagger.annotations.ApiModelProperty',
                'java.util.Date'
            ])
            obj.set_class_decorators(['@ApiModel'])
            for col in result.columns.values():
                comment = col.comment
                if comment is None:
                    comment = col.name

                # 不显示注释
                col.comment = None
                obj.add_attr(col)
                data_type = obj.gen_data_type(col.data_type)

                decorators = []
                decorators.append('@ApiModelProperty(value = "%s")' % (comment))
                if data_type == 'Date':
                    decorators.append('@JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd HH:mm:ss", locale = "zh", timezone = "GMT+8")')
                obj.set_attr_decorator(col.name, decorators)

            code = obj.to_string()
            if ajax == 1:
                return self.asJson(code)
            else:
                return self.render('code', code=code, title=title, logo=logo)

        uri = 'ddl2info'
        return self.render('ddl2', title=title, logo=logo, uri=uri)
