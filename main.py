#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3
import os.path
from http.server import HTTPServer
from http.server import CGIHTTPRequestHandler
from lxml import etree, objectify


def parse_book_xml(xml_file):
    with open(xml_file) as fobj:
        xml = fobj.read()

    root = etree.fromstring(xml)

    books = []
    for book in root.getchildren():
        one_book = []
        for elem in book.getchildren():
            if not elem.text:
                one_book.append("None")
            else:
                one_book.append(elem.text)
        books.append(one_book)

    return [tuple(i) for i in books]


def create_appt(data):  # Создаем изначальную структуру XML

    appt = objectify.Element("painters")
    appt.id_painters = data["id_painters"]
    appt.full_name = data["full_name"]
    appt.genre = data["genre"]
    appt.birthday = data["birthday"]
    return appt


def create_xml():  # Создаем XML файл

    xml = '''<?xml version="1.0"?>
    <painters_table>
    </painters_table>
    '''

    root = objectify.fromstring(xml)

    appt = create_appt({"id_painters": "1",
                        "full_name": "Pablo Picasso",
                        "genre": "Portrait",
                        "birthday": "25.10.1881"}
                       )
    root.append(appt)

    appt = create_appt({"id_painters": "2",
                        "full_name": "Leonardo da Vinci",
                        "genre": "Portrait",
                        "birthday": "15.04.1452"}
                       )
    root.append(appt)

    appt = create_appt({"id_painters": "3",
                        "full_name": "Mary",
                        "genre": "Landscape",
                        "birthday": "23.02.1750"}
                       )
    root.append(appt)

    # удаляем все lxml аннотации.
    objectify.deannotate(root)
    etree.cleanup_namespaces(root)

    # конвертируем все в привычную нам xml структуру.
    obj_xml = etree.tostring(root, pretty_print=True, xml_declaration=True)

    try:
        with open("base_in.xml", "wb") as xml_writer:
            xml_writer.write(obj_xml)
        print("Конект прошел")
    except IOError:
        print("Упсссс!")
        pass

if not os.path.isfile('paintings.db'):
    db = sqlite3.connect('paintings.db')
    cur = db.cursor()

    cur.execute("DROP TABLE IF EXISTS painters")
    cur.execute("""CREATE TABLE IF NOT EXISTS painters (
                    id_painters INTEGER PRIMARY KEY AUTOINCREMENT ,
                    full_name TEXT NOT NULL, 
                    genre TEXT ,
                    birthday TEXT
                    ) """)
    db.commit()

    cur.execute("DROP TABLE IF EXISTS technic")
    cur.execute("""CREATE TABLE IF NOT EXISTS technic (
                    id_technic INTEGER PRIMARY KEY AUTOINCREMENT,
                    technic_name TEXT  
                    ) """)
    db.commit()

    cur.execute("DROP TABLE IF EXISTS paintings")
    cur.execute("""CREATE TABLE IF NOT EXISTS paintings (
                    id_picture INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL, 
                    date_of_creation TEXT,
                    id_painter INTEGER,
                    id_technic INTEGER,
                    FOREIGN KEY (id_painter) REFERENCES painters(id_painters),
                    FOREIGN KEY (id_technic) REFERENCES technic(id_technic)
                    ) """)
    db.commit()

    technic = [(1, 'Acrylic'), (2, 'Oil paints'), (3, 'Dry brush')]

    sql = '''INSERT INTO technic(id_technic, technic_name) VALUES(?, ?) '''
    db.executemany(sql, technic)
    db.commit()


    paintings = [(1, 'Girl on the Ball', '1905', '1', '1'),
                (2, 'Mona Lisa', '1503', '2', '2'),
                (3, 'Per aspera ad Astra', '19.12.1815', '3', '3')]

    sql = '''INSERT INTO paintings(id_picture, name, date_of_creation, id_painter, id_technic) VALUES(?, ?, ?, ?, ?) '''
    db.executemany(sql, paintings)
    db.commit()

    painters = [(1, 'Pablo Picasso', 'Portrait', '25.10.1881'),
                (2, 'Leonardo da Vinci', 'Portrait', '15.04.1452'),
                (3, 'Mary', 'Landscape', '23.02.1750')]

    sql = '''INSERT INTO painters(id_painters, full_name, genre, birthday) VALUES(?, ?, ?, ?) '''
    db.executemany(sql, painters)
    db.commit()

    xml_books = parse_book_xml("base_out.xml")  #
    db.executemany(sql, xml_books)

    db.commit()

create_xml()

server_address = ("", 8080)
httpd = HTTPServer(server_address, CGIHTTPRequestHandler)
httpd.serve_forever()
