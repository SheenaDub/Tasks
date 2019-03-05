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

def writeTask(name, detail, theDeadline, uname):
    _SQL = """insert into tasks (taskname, taskdetail, taskdeadline, username) values (%s, %s, %s, %s)"""
    print(name, detail, theDeadline, uname)
    try:
        cursor.execute(_SQL, (name, detail, theDeadline, uname))
        connection.commit()
        closeConnection()
        print("db success")
    except:
        print("db fail")
        connection.rollback()
        pass

def createUser(name, pword):
    _SQL = """insert into users (username, password) values (%s, %s)"""
    try:
        cursor.execute(_SQL, (name, pword))
        connection.commit()
        closeConnection()
        print("db success")
    except:
        connection.rollback()
        print("db fail")
        pass


def checkUser(name, pword):
    _SQL = "select username, userid from users WHERE password = '%s' AND username = '%s'" % (pword, name)
    try:
        cursor.execute(_SQL)
        r = cursor.fetchone()
        closeConnection()
        print(r)
        print("db success")
        return r
    except:
        connection.rollback()
        print("db fail")
        pass


# gets tasks of one specified user as list - user name as string
def getUserTasksAsList(name):
    _SQL = """select id, taskname, taskdetail, taskdeadline from tasks where username ='%s'""" %(name)
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
    newname = name.strip()
    _SQL = "DELETE FROM tasks WHERE taskname = '%s'" % (newname)
    try:
        # Execute the SQL command
        cursor.execute(_SQL)
        connection.commit()
        closeConnection()
    except:
        # Rollback in case there is any error
        connection.rollback()



def deleteATask(id):
    # Prepare SQL query to DELETE required records
    _SQL = "DELETE FROM tasks WHERE userID = '%d'" % (id)
    try:
        # Execute the SQL command
        cursor.execute(_SQL)
        connection.commit()
        closeConnection()
    except:
        # Rollback in case there is any error
        connection.rollback()


def editTask(name, detail, deadline, oldname):
    _SQL = """UPDATE tasks SET taskname=%s, taskdetail=%s, taskdeadline=%s WHERE taskname =%s"""
    try:
        cursor.execute(_SQL, (name, detail, deadline, oldname))
        connection.commit()
        closeConnection()
    except Exception as error:
        connection.rollback()
        print("Exception: ", error)
        pass


# FUNCTION TO del all tasks of one user
def del_user_tasks(name):
    _SQL = "DELETE FROM tasks WHERE username = '%s'" % (name)
    try:
        cursor.execute(_SQL)
        connection.commit()
        closeConnection()

    except Exception as error:
        connection.rollback()
        print("Exception: ", error)
        pass


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





