#! /usr/bin/python3
# This is restTurnin.cgi

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


if ((not ('PATH_INFO' in os.environ)) or ('PATH_INFO' in os.environ and os.environ['PATH_INFO'] == '/')):
  print("Connnection-Type: text/html")
  print("Status: 200 OK")
  print()
  print("""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Form to post Course into SQL Database</title></head>
    <body><h1>Courses (REST) website. Main links</h1><br><div>
    <a href="/cgi-bin/restTurnin.cgi/courses" method="get">courses/</a><br>
    <a href="/cgi-bin/restTurnin.cgi/form">new course form</a></div><br><div>
    <a href="/cgi-bin/restTurnin.cgi">Back to root of this site</a></div></body></html> """)

elif ('PATH_INFO' in os.environ and os.environ['REQUEST_METHOD'] == "GET" and ((os.environ['PATH_INFO'] == '/courses') or os.environ['PATH_INFO'] == "/courses/")):
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
elif ('PATH_INFO' in os.environ and re.search("/courses/\d+", os.environ['PATH_INFO'])):
  print("Content-Type: application/json")
  print("Status: 200 OK")
  print()
  id = str(int(re.findall('\d+',os.environ['PATH_INFO'])[0]))
  connection = MySQLdb.connect(host = passwords.SQL_HOST, user = passwords.SQL_USER, passwd = passwords.SQL_PASSWD, db="courses", charset = "utf8")
  cursor = connection.cursor();
  command = "SELECT * FROM courses WHERE id=%s;"%id
  #cursor.execute("SELECT * FROM courses WHERE id={};".format(id)) # works but is dirty
  #cursor.execute("SELECT * FROM courses WHERE id=%s", (id)) # does not work, but it uses one less line
  #cursor.execute(command)
  cursor.execute("SELECT * FROM courses WHERE id=%s;"%id)
  results = cursor.fetchall()
  results_json = json.dumps(results)
  print(results_json)
  cursor.close()
  connection.commit()
  connection.close()
elif('PATH_INFO' in os.environ and os.environ['PATH_INFO'] == '/form'):
  print("Content-Type: text/html")
  print("Status: 200 OK")
  print()
  print("""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<title>Form to post Course into SQL Database</title></head><body>
<h1>Form to post Course into SQL Database:</h1><br><br>
<form method="post" action="/cgi-bin/restTurnin.cgi/courses">
        <div><label for="dept">Department:</label><input id="dept" name="dept" type="text" ></div>
        <div><label for="course">Course Number:</label><input id="course" name="course" type="text" ></div>
        <div><label for="units">Units:</label><input id="units" name="units" type="number" step="1"></div>
        <div><input type="submit" id="submit" name="submit" value="Register"></div>
    </form></body></html> """)

elif ('PATH_INFO' in os.environ and os.environ['REQUEST_METHOD'] == "POST" and ((os.environ['PATH_INFO'] == '/courses') or (os.environ['PATH_INFO'] == "/courses/")) and ("units" in form and "dept" in form and "course" in form)):
  units = str(form["units"].value)
  dept = str(form["dept"].value)
  course = str(form["course"].value)
  connection = MySQLdb.connect(host = passwords.SQL_HOST, user = passwords.SQL_USER, passwd = passwords.SQL_PASSWD, db="courses", charset = "utf8")
  cursor = connection.cursor()
  cursor.execute("INSERT INTO courses (dept, course, units) VALUES(%s,%s,%s);", (dept, course, units))
  newID = cursor.lastrowid
  url = str("/courses/" + str(newID))
  cursor.execute("UPDATE courses SET url=%s WHERE id=%s;", (url, newID))
  cursor.close()
  connection.commit()
  connection.close()
  print("Content-Type: text/html")
  print("Status: 302 Redirect")
  print("Location: /cgi-bin/restTurnin.cgi" + url)
  print()


elif ('PATH_INFO' in os.environ and os.environ['REQUEST_METHOD'] == "POST" and ((os.environ['PATH_INFO'] == '/courses') or (os.environ['PATH_INFO'] == "/courses/"))):
  print("Content-Type: text/html")
  print("Status: 200 OK")
  print()
  print("You are in /courses with method = post")
  if "units" in form:
    print("units in form")
  if "course" in form:
    print("course in form")
  if "dept" in form:
    print("dept in form")
else:
    print("Content-Type: text/html")
    print("Status: 200 OK")
    print()
    print("""<html><head><meta charset="UTF-8"><title>Bad url</title></head><body>
      <p>This is not a valid url, please go <a href="/cgi-bin/restTurnin.cgi">Back to the root page</a>
      </p><br></body></html>""")
