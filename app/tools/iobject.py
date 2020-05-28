class iObject():
    comment = ''
    space = ''
    name = ''
    attributes = {}
    methods = {}

    def __init__(self, name=None):
        if name is not None:
            self.name = name

    def set_space(self, space):
        self.space = space

    def get_space(self):
        return 'use %s;' % (self.space)

    def set_comment(self, comment):
        self.comment = comment

    def get_comment(self):
        return '// %s' % (self.comment)

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return 'public class %s' % (self.name)

    def add_attr(self, attr):
        self.attributes[attr.name] = attr

    def gen_data_type(self, data_type):
        maps = {
            'TINYINT': 'Byte',
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
            'TEXT': 'DataTypeWithBLOBs.String',
            'MEDIUMBLOB': 'DataTypeWithBLOBs.byte[]',
            'MEDIUMTEXT': 'DataTypeWithBLOBs.String ',
            'LONGBLOB': 'DataTypeWithBLOBs.byte[]',
            'LONGTEXT': 'DataTypeWithBLOBs.String   '
        }

        return ' %s ' % (maps[data_type]) if data_type in maps else ' '

    def get_attr(self, attr_name):
        attr = self.attributes[attr_name] if attr_name in self.attributes else None
        if attr is None:
            return ''

        s = ''
        if attr.comment is not None:
            s = '\t/** %s **/\n' % (attr.comment)
        access = getattr(attr, 'access', 'public')
        s += '\t%s%s%s;\n' % (access, self.gen_data_type(attr.data_type), attr.name)
        return s

    def add_method(self, method):
        self.methods[method.name] = method

    def get_method(self, method_name):
        pass

    def to_string(self):
        self.stype = 'java'

        s = self.get_comment()
        s += '\n'
        s += self.get_name()
        s += ' {\n'
        for x in self.attributes:
            s += self.get_attr(x)
            s += '\n'
        s = s[0:-1] + '}\n'
        return s
