#! -*- coding: utf-8 -*-
#
# created by giginet on 2014/4/15
#
__author__ = 'giginet'
__version__ = (0, 1, 0)
VERSION = ".".join(map(str, __version__))

try:
    import pymysql
    pymysql.install_as_MySQLdb()
except:
    pass
