#!/usr/bin/python2.7

import MySQLdb
import entropy
import json
import csv
import sys

from datetime import datetime

db = MySQLdb.connect(db="enron")
c = MySQLdb.cursors.DictCursor(db) 

query="""SELECT m.sender "sender",
           r.rvalue AS "recipient", 
           m.date, m.subject, 
           m.body from message m,
           recipientinfo r 
         WHERE r.mid = m.mid 
         ORDER BY m.date"""

def datetime_to_iso(obj):
    return obj.isoformat() 

def gentropy(email, compare=None):
    particle = email.pop('body')

    try:
        ent = entropy.shannon_entropy(particle)
        email['entropy'] = ent

        email['date'] = email['date'].isoformat() #convert to str

    except:
        print "[ERROR] Failed to parse: %s " % (particle)

    return email

def write_json(emails, file_prefix):
    try:
        json_filename = file_prefix + ".json"
        json_fh = open(json_filename, 'w')
        json.dump(emails, json_fh)
        ret = True

    except:
        print "failed to write csv! Continuing.."
        print sys.exc_info()[0]
        ret = False

    json_fh.close()
    return ret

def write_csv(emails, file_prefix):
    #try:
    if 1 == 1:
        csv_filename = file_prefix + ".csv"
        csv_fh = open(csv_filename,'w')
        csv_header = emails[0].keys()
        csv_writer = csv.DictWriter(csv_fh, csv_header)
    
        csv_writer.writeheader()
        csv_writer.writerows(emails)
        ret = True

    #except:
    #    print "failed to write csv! Continuing.."
    #    print sys.exc_info()[0]
    #    ret = False

    csv_fh.close()
    return ret

def write_to_file(emails, file_prefix="tofrom_entropy", types=['csv','json']):
    if not types:
        return False

    for out_type in types:
        if out_type == 'csv':
            write_csv(emails, file_prefix)

        if out_type == 'json':
            write_json(emails, file_prefix)

c.execute(query)
all_emails = c.fetchall()

emails_ent = [ gentropy(email) for email in all_emails ]
write_to_file(emails_ent, types=['csv'])
