from app.tools import istring


class iObject():
    space = ''
    packages = []
    comment = ''
    class_decorators = []
    name = ''
    extends = ''
    attributes = {}
    comment_compress = False
    attr_decorators = {}
    show_methods = True

    def __init__(self, name=None):
        if name is not None:
            self.name = istring.ucwords(name)

    def set_name_extra(self, extra):
        self.name += extra

    def set_space(self, space):
        self.space = space

    def get_space(self):
        s = ''
        if self.space != '':
            s = 'package %s;\n' % (self.space)
        return s

    def set_packages(self, packages):
        if type(packages) is str:
            self.packages.append(packages)
        else:
            self.packages = packages

    def get_packages(self):
        s = ''
        if len(self.packages) > 0:
            s = '\n'
            for x in self.packages:
                s += 'import %s;\n' % (x)
            s += '\n'
        return s

    def set_comment(self, comment):
        self.comment = comment

    def get_comment(self):
        return '/**\n * %s\n */\n' % (self.comment)

    def set_class_decorators(self, decorators):
        self.class_decorators = decorators

    def get_class_decorators(self):
        if len(self.class_decorators) == 0:
            return ''

        s = ''
        for x in self.class_decorators:
            s += '%s\n' % (x)
        return s

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return 'public class %s' % (self.name)

    def set_extends(self, extends):
        self.extends = extends

    def get_extends(self):
        s = ''
        if self.extends != '':
            s = ' extends %s' % (self.extends)
        return s

    def add_attr(self, attr):
        self.attributes[attr.name] = attr

    def set_attr_decorator(self, attr_name, decorators):
        self.attr_decorators[attr_name] = decorators

    def get_attr_decorator(self, attr_name):
        decorators = self.attr_decorators[attr_name] if attr_name in self.attr_decorators else None
        if decorators is None:
            return ''

        s = ''
        for x in decorators:
            s += '\t%s\n' % (x)
        return s

    def gen_data_type(self, data_type):
        maps = {
            # 'TINYINT': 'Byte',
            'TINYINT': 'Short',
            'SMALLINT': 'Short',
            'MEDIUMINT': 'Integer',
            'INT': 'Integer',
            'INTEGER': 'Integer',
            'BIGINT': 'Long',
            'FLOAT': 'Float',
            'DOUBLE': 'Double',
            'DECIMAL': 'BigDecimal',
            'DATE': 'Date',
            'TIME': 'Date',
            'YEAR': 'Date',
            'DATETIME': 'Date',
            'TIMESTAMP': 'Date',
            'CHAR': 'String',
            'VARCHAR': 'String',
            'TINYBLOB': 'DataTypeWithBLOBs.byte[]',
            'TINYTEXT': 'String',
            'BLOB': 'DataTypeWithBLOBs.byte[]',
            # 'TEXT': 'DataTypeWithBLOBs.String',
            'TEXT': 'String',
            'MEDIUMBLOB': 'DataTypeWithBLOBs.byte[]',
            # 'MEDIUMTEXT': 'DataTypeWithBLOBs.String',
            'MEDIUMTEXT': 'String',
            'LONGBLOB': 'DataTypeWithBLOBs.byte[]',
            # 'LONGTEXT': 'DataTypeWithBLOBs.String   '
            'LONGTEXT': 'String   '
        }

        return maps[data_type] if data_type in maps else ''

    def get_attr(self, attr_name):
        attr = self.attributes[attr_name] if attr_name in self.attributes else None
        if attr is None:
            return ''

        s = ''
        if attr.comment is not None:
            if self.comment_compress is True:
                s = '\t/** %s **/\n' % (attr.comment)
            else:
                s = '\t/**\n\t * %s\n\t */\n' % (attr.comment)
        s += self.get_attr_decorator(attr_name)
        access = getattr(attr, 'access', 'private')
        data_type = self.gen_data_type(attr.data_type)
        if data_type != '':
            s += '\t%s %s %s;\n' % (access, data_type, istring.ucwords(attr.name, False, False))
        return s

    def get_method(self, attr_name):
        attr = self.attributes[attr_name] if attr_name in self.attributes else None
        if attr is None:
            return ''

        s = ''
        comment = ''
        if attr.comment is not None:
            if self.comment_compress is True:
                comment = '\t/** %s **/\n' % (attr.comment)
            else:
                comment = '\t/**\n\t * %s\n\t */\n' % (attr.comment)

        data_type = self.gen_data_type(attr.data_type)
        if data_type != '':
            name1 = istring.ucwords(attr.name)
            name2 = istring.ucwords(attr.name, False, False)

            s += comment
            s += '\tpublic %s get%s() {\n' % (data_type, name1)
            s += '\t\treturn %s;\n' % (name2)
            s += '\t}\n\n'

            s += comment
            s += '\tpublic void set%s(%s %s) {\n' % (name1, data_type, name2)
            s += '\t\tthis.%s = %s;\n' % (name2, name2)
            s += '\t}\n'

        return s

    def to_string(self):
        self.stype = 'java'

        s = ''
        s += self.get_space()
        s += self.get_packages()
        s += self.get_comment()
        s += self.get_class_decorators()
        s += self.get_name()
        s += self.get_extends()
        s += ' {\n'
        for x in self.attributes:
            s += self.get_attr(x)
            s += '\n'

        if self.show_methods is True:
            for x in self.attributes:
                s += self.get_method(x)
                s += '\n'

        s = s[0:-1] + '}\n'
        return s
