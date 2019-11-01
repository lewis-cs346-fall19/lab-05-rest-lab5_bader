#! /usr/bin/python3
# This is simpleRest2.cgi

import cgi
import cgitb
import sys
import os
import json
cgitb.enable()


if 'PATH_INFO' in os.environ:
    print("Connnection-Type: text/html")
    print("Status: 200 OK")
    print()

    path = os.environ['PATH_INFO']
    print("""<html><body><p>Bader Jeragh. This is a sample with PATH_INFO {} </p> </body> </html> """.format(path))
else:
    print("Connection-Type: text/html")
    print("Status: 302 Redirect")
    print("Location:https://www.google.com")
    print()
