# -*- coding: utf-8 -*-
import ConfigParser, MySQLdb
import sys
config = ConfigParser.ConfigParser()
config.read(sys.argv[1])

hostname =  config.get ('mysql', 'host')
dbname =  config.get ('mysql', 'dbname')
username =  config.get ('mysql', 'user')
password =  config.get ('mysql', 'passwd')

db = MySQLdb.connect(hostname, username, password, dbname, use_unicode=True)

cursor = db.cursor()
cursor.execute('SET NAMES utf8')
cursor.execute("""DELETE FROM tag_errors WHERE error_type = 4""")
cursor.execute("""DELETE FROM tag_errors WHERE error_type = 6""")
cursor.execute("""SELECT book_id, tag_name FROM book_tags WHERE
			(book_id in (select book_id from books where parent_id = 8 or parent_id = 56)) and  (tag_name LIKE 'url:%') and (tag_name NOT LIKE '%oldid=%')""") 
data = cursor.fetchall();
for i in data:
    query = """INSERT INTO tag_errors VALUES(%d, '%s', %d)""" % (i[0], i[1], 4)
    cursor.execute(query)

cursor.execute("""SELECT distinct book_id FROM books WHERE book_id NOT IN (SELECT book_id FROM book_tags WHERE tag_name LIKE 'url:%')""")
data1 = cursor.fetchall();
#for i in data:
#    query = """INSERT INTO tag_errors VALUES(%d, '%s', %d)""" % (i[0], i[1], 4)
#    cursor.execute(query)
for j in data1:
    query1 = """INSERT INTO tag_errors VALUES(%d, '%s', %d)""" % (j[0], '', 6)
    cursor.execute(query1)
db.commit()
db.close


