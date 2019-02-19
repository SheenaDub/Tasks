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
    print("in getTasks. datatype of r: ", type(r))
    return jsonTasks

def getTasksAsList():
    _SQL = """select id, taskname, taskdetail, taskdeadline from tasks"""
    cursor.execute(_SQL)
    r = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]
    closeConnection()
    return r

def getOneTask(name):
    _SQL = "select id, taskname, taskdetail, taskdeadline from tasks WHERE taskname = '%s'" % (name)
    cursor.execute(_SQL)
    r = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]
    closeConnection()
    return r

def deleteATaskbyName(name):
    # Prepare SQL query to DELETE required records
    #_SQL = """DELETE FROM tasks WHERE taskname = '%s'""" % (name)
    print("delete a task by name function in db.py called")
    print("task to be deleted is ", name)
    newname = name.strip()
    print("task name after strip function ", newname)
    _SQL = "DELETE FROM tasks WHERE taskname = '%s'" % (newname)
    try:
        # Execute the SQL command
        cursor.execute(_SQL)
        connection.commit()
        closeConnection()
        print("delete success. allegedly")
    except:
        print("delete error")
        # Rollback in case there is any error
        connection.rollback()




def deleteATask(id):
    # Prepare SQL query to DELETE required records
    _SQL = "DELETE FROM tasks WHERE id = '%d'" % (id)
    print("delete a task function in db.py called")
    try:
        # Execute the SQL command
        cursor.execute(_SQL)
        connection.commit()
        closeConnection()
    except:
        # Rollback in case there is any error
        connection.rollback()


# FUNCTION TO CLEAN ALL TASKS!!!!
def empty_table():
    try:
        print("empty table in db.py called: ")
        cursor.execute('TRUNCATE TABLE tasks')
        connection.commit()
        closeConnection()

    except Exception as error:
        connection.rollback()
        print("Exception: ", error)
        pass





