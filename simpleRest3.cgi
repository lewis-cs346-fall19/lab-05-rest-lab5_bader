#! /usr/bin/python3
# This is simpleRest3.cgi

import cgi
import cgitb
import sys
import os
import json
import MySQLdb
import re
import passwords
cgitb.enable()
form = cgi.FieldStorage()

if ('PATH_INFO' in os.environ) and os.environ['PATH_INFO'] == '/hello':
    print("Content-Type: application/json")
   # print("Content-Type: text/html")
    print("Status: 200 OK")
    print()

    x = {"foo": "bar", "hello": "32"}
    x_json = json.dumps(x)
    path = os.environ['PATH_INFO']
    print(x_json)
elif ('PATH_INFO' in os.environ and ((os.environ['PATH_INFO'] == '/courses') or os.environ['PATH_INFO'] == "/courses/")):
        print("Content-Type: application/json")
        print("Status: 200 OK")
        print()
        connection = MySQLdb.connect(host = passwords.SQL_HOST, user = passwords.SQL_USER, passwd = passwords.SQL_PASSWD, db="courses", charset = "utf8")
        cursor = connection.cursor();
        cursor.execute("SELECT * FROM courses");
        results = cursor.fetchall();
        results_json = json.dumps(results);
        print(results_json);



        cursor.close();
        connection.commit();
        connection.close();

elif ('PATH_INFO' in os.environ and re.search("/courses/\d+", os.environ['PATH_INFO']) and os.environ['REQUEST_METHOD'] == "GET"):
        print("Content-Type: application/json")
        print("Status: 200 OK")
        print()
        id = re.findall('\d+',os.environ['PATH_INFO'])[0]
        connection = MySQLdb.connect(host = passwords.SQL_HOST, user = passwords.SQL_USER, passwd = passwords.SQL_PASSWD, db="courses", charset = "utf8")
        cursor = connection.cursor();
        cursor.execute("SELECT * FROM courses WHERE id=%s;", (id))
        results = cursor.fetchall()
        results_json = json.dumps(results)
        print(results_json)



        cursor.close()
        connection.commit()
        connection.close()
elif ('PATH_INFO' in os.environ and re.search("/courses/\d+", os.environ['PATH_INFO']) and os.environ['REQUEST_METHOD'] == "POST"):
        id = re.findall('\d+',os.environ['PATH_INFO'])[0]
        connection = MySQLdb.connect(host = passwords.SQL_HOST, user = passwords.SQL_USER, passwd = passwords.SQL_PASSWD, db="courses", charset = "utf8")
        cursor = connection.cursor();
        cursor.execute("SELECT * FROM courses WHERE id=%s;", (id))
        results = cursor.fetchall()
        if(not (results is None)):
            print("Content-Type: text/html")
            print("Status: 200 OK")
            print()
            print("Sorry, the object already exists")
        elif ("units" in form and "dept" in form and "course" in form):
            units = str(form["units"].value)
            dept = str(form["dept"].value)
            course = str(form["course"].value)
            url = str(form["url"].value)
            cursor.execute("INSERT INTO courses (dept, course, units, url) VALUES(%s,%s,%s,%s)", (dept, course, units, url))
            newID = cursor.lastrowid
            print("Content-Type: text/html")
            print("Status: 302 Redirect")
            print("Location: /courses/", newID)
            print()
        cursor.close()
        connection.commit()
        connection.close()

else:
    print("Content-Type: text/html")
    print("Status: 302 Redirect")
    print("Location:https://www.google.com")
    print()
