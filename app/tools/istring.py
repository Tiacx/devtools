import hashlib


def md5(s):
    if type(s) != str:
        s = str(s)

    o = hashlib.md5()
    o.update(s.encode('utf8'))
    return o.hexdigest()


def ucwords(s, underline=False):
    if s.find('_') == -1:
        return s.capitalize()

    _new = ''
    _list = s.split('_')
    for x in _list:
        _new += x.capitalize() + '_'

    _new = _new[:-1]

    if underline is False:
        _new = _new.replace('_', '')
    return _new
