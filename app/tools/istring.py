import hashlib


def md5(s):
    if type(s) != str:
        s = str(s)

    o = hashlib.md5()
    o.update(s.encode('utf8'))
    return o.hexdigest()


def ucwords(s, underline=False, cap=True):
    if s.find('_') == -1:
        return s.capitalize() if cap is True else s

    _new = ''
    _list = s.split('_')
    for i in range(len(_list)):
        if i == 0 and cap is False:
            _new += _list[i] + '_'
        else:
            _new += _list[i].capitalize() + '_'

    _new = _new[:-1]

    if underline is False:
        _new = _new.replace('_', '')
    return _new
