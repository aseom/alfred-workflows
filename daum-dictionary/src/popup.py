#!/usr/bin/python2.7
# -*- coding: utf8 -*-

import cocoa
import sys
from urllib import quote
from unicodedata import normalize

reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise ValueError
    query = normalize('NFC', unicode(sys.argv[1])).encode('utf-8')
    url = u'http://small.dic.daum.net/search.do?q=%s' % quote(query)
    view = cocoa.BrowserView('Daum Dictionary', url, width=400, height=700)
    view.show()
    sys.exit(0)
