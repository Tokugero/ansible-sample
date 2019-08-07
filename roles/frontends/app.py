from flask import Flask
import threading
import os
import mysql.connector

app = Flask(__name__)
query = ("show variables like 'server_id';")

def callsql(result):
    cnx = mysql.connector.connect(user='haproxy_root', password='haproxy_root', host='165.22.131.188')
    cursor = cnx.cursor()
    cursor.execute(query)
    for (variable_name, value) in cursor:
        result.append("Queried mysql server "+value+" from server: "+os.uname()[1])
    cursor.close()
    cnx.close()

def unreasonablecalls(calls):
    threads = []
    output = []
    for i in range(calls):
        functionThread = threading.Thread(target=callsql, args=(output,))
        threads.append(functionThread)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return output

@app.route('/')
def get_rekt_sql():
    calls = 1000
    queryResult = unreasonablecalls(calls)
    response = ""
    for i in queryResult:
        response += i+"<br>"

    response = str(len(queryResult))+" calls were successfully made out of "+str(calls)+"<br>"+response
    return response
