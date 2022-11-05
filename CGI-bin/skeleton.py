# -*- coding: utf-8 -*-
import sqlite3
import cgi

db = sqlite3.connect('paintings.db')
cur = db.cursor()

print("Content-type: text/html\n\n");
form = cgi.FieldStorage()

full_name = form.getvalue("full_name", "Не задано")
genre = form.getvalue("genre", "Не задано")
birthday = form.getvalue("birthday", "Не задано")
technic_name = form.getvalue("technic_name", "Не задано")
name_pic = form.getvalue("name_pic", "Не задано")
date_of_creation = form.getvalue("date_of_creation", "Не задано")
id_painter = form.getvalue("id_painter", "Не задано")
id_picture = form.getvalue("id_picture", "Не задано")
db.commit()

cur.execute('INSERT INTO painters VALUES (Null, ?, ?, ?)', (full_name, genre, birthday))
db.commit()

cur.execute('INSERT INTO technic VALUES (Null, ?)', (technic_name,))
db.commit()

cur.execute('INSERT INTO paintings VALUES (Null, ?, ?, ?, ?)', (name_pic, date_of_creation, id_painter, id_picture))
db.commit()

# cur.execute('DELETE FROM painters WHERE full_name = "aaaa" ')
# db.commit()

# cur.execute('UPDATE painters SET genre = "aaaa" WHERE full_name = "OK" ')
# db.commit()

cur.execute('SELECT * FROM painters')
db.commit()
print(cur.fetchall())







