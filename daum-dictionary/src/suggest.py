#!/usr/bin/python2.7
# -*- coding: utf8 -*-

import sys
import json
from urllib import quote
from urllib2 import urlopen
from unicodedata import normalize

reload(sys)
sys.setdefaultencoding('utf-8')

def parse_item(item):
    word, meaning = item.split('|')[1:]
    if meaning == ' ':
        title = u'%s' % word
    else:
        title = u'%s: %s' % (word, meaning)
    subtitle = u"Search Daum Dictionary for '%s'" % word

    return u'<item arg="%s"><title>%s</title><subtitle>%s</subtitle></item>'\
        % (word, title, subtitle)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise ValueError
    query = normalize('NFC', unicode(sys.argv[1])).encode('utf-8')
    url = u'http://suggest.dic.daum.net/dic_all_ctsuggest?mod=json&cate=lan&q=%s'\
        % quote(query)
    data = json.loads(urlopen(url).read())

    print '<?xml version="1.0"?>'
    print '<items>'
    for item in data['items']:
        print parse_item(item)
    print '</items>'
