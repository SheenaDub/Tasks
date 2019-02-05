import mysql.connector
from time import sleep
import json


dbconfig = {
   'host':'127.0.0.1',
    'user': 'root',
    'password':'root',
    'database':'tasks',
}

def createConnection():
    global connection
    while True:
        try:
            connection = mysql.connector.connect(**dbconfig)
            print("connection established")
            global cursor
            cursor = connection.cursor()
            break

        except Exception as error:
            print(error)
            sleep(10)
            pass

def closeConnection():
    cursor.close()
    connection.close()

def writeTask(name, detail, theDeadline):
    _SQL = """insert into tasks (taskname, taskdetail, taskdeadline) values (%s, %s, %s)"""
    try:
        cursor.execute(_SQL, (name, detail, theDeadline))
        connection.commit()
        closeConnection()
    except:
        connection.rollback()
        pass

def getTasks():
    _SQL = """select id, taskname, taskdetail, taskdeadline from tasks"""
    cursor.execute(_SQL)
    r = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]
    closeConnection()
    jsonTasks = json.dumps(r)
    return jsonTasks



def getOneTask(name):
    _SQL = "select id, taskname, taskdetail, taskdeadline from tasks WHERE taskname = '%s'" % (name)
    cursor.execute(_SQL)
    r = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]
    closeConnection()
    return r


# FUNCTION TO CLEAN ALL TASKS!!!!
def empty_table():
    try:
        cursor.execute('TRUNCATE TABLE tasks')
        connection.commit()
        closeConnection()

    except Exception as error:
        connection.rollback()
        print("Exception: ", error)
        pass





