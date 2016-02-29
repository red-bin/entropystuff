#!/usr/bin/python2.7

import ijson
import codecs

"""Creates a json format of wikipedia's text. Used with multi_threader.sh,
   which is usually gzipped straight from stdout. Needs more disk space."""

ROOTDIR = '/opt/projects/wiki_project/'
json_file_loc = "%s/latest-all.json" % ROOTDIR

#json_reader = codecs.getreader('utf-8')
json_fh = open(json_file_loc)
json_file = codecs.EncodedFile(json_fh, 'utf8')
buf = ijson.parse(json_file, buf_size=1024)

while True:
    #key, val  = buf.next()
    print buf.next()

    #print type(val)
    if not buf:
        break

    #print key, val
