import re


def is_quoated(text, s, e, quotes=('"', "'", '`')):
    """
    指定された文字列の特定部分がクオート文字で囲まれているか調べる

    Ref: https://gist.github.com/lambdalisue/f2c9ab121883e48d3c2f

    Examples:
        >>> #         0123456789012345678901234
        >>> text = '''N'Y'N'Y'N"Y"N"Y'Y'Y"N"Y"N'''
        >>> # N
        >>> assert is_quoated(text, 0, 1) is False
        >>> # N'
        >>> assert is_quoated(text, 0, 2) is False
        >>> # N'Y
        >>> assert is_quoated(text, 0, 3) is False
        >>> # N'Y'
        >>> assert is_quoated(text, 0, 4) is False
        >>> # '
        >>> assert is_quoated(text, 1, 2) is False
        >>> # 'Y
        >>> assert is_quoated(text, 1, 3) is False
        >>> # 'Y'
        >>> assert is_quoated(text, 1, 4) is False
        >>> # 'Y'N
        >>> assert is_quoated(text, 1, 5) is False
        >>> # Y
        >>> assert is_quoated(text, 2, 3) is True
        >>> # Y'
        >>> assert is_quoated(text, 2, 4) is False
        >>> # Y'N
        >>> assert is_quoated(text, 2, 5) is False
        >>> # Y'N'
        >>> assert is_quoated(text, 2, 6) is True
        >>> # Y'N'Y
        >>> assert is_quoated(text, 2, 7) is True
        >>> # Y'N'Y'
        >>> assert is_quoated(text, 2, 8) is False
    """
    for quote in quotes:
        pattern = re.compile("[^{}]*".format(quote))
        p = pattern.sub('', text[:s])
        n = pattern.sub('', text[e:])
        if len(p) > 0 and len(n) > 0 and (len(p) * len(n)) % 2 != 0:
            return True
    return False


if __name__ == '__main__':
    import doctest;
    doctest.testmod()
