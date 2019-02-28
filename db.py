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

def writeTask(id, name, detail, theDeadline):
    _SQL = """insert into tasks (userID, taskname, taskdetail, taskdeadline) values (%s, %s, %s, %s)"""
    print(name, detail, theDeadline, id)
    print("type of id in write task ", type(id))
    try:
        cursor.execute(_SQL, (id, name, detail, theDeadline))
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
    except:
        connection.rollback()
        pass


def checkUser(name, pword):
    _SQL = "select username, userid from users WHERE password = '%s' AND username = '%s'" % (pword,name)
    try:
        cursor.execute(_SQL)
        r = cursor.fetchone()
        closeConnection()
        print(r)
        return r
    except:
        connection.rollback()
        pass



# gets all tasks in task table as json object
def getTasks():
    _SQL = """select id, taskname, taskdetail, taskdeadline from tasks"""
    cursor.execute(_SQL)
    r = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]
    closeConnection()
    jsonTasks = json.dumps(r)
    print("in getTasks. datatype of r: ", type(r))
    return jsonTasks

# gets all tasks in task table as list
def getTasksAsList():
    _SQL = """select id, taskname, taskdetail, taskdeadline from tasks"""
    cursor.execute(_SQL)
    r = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]
    closeConnection()
    return r

# gets tasks of one specified user as list
def getUserTasksAsList(userID):
    _SQL = """select id, taskname, taskdetail, taskdeadline from tasks where userID ='%d'""" %(userID)
    cursor.execute(_SQL)
    r = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]
    closeConnection()
    return r

def getUserName(userID):
    _SQL = """select username from users where userid ='%d'""" %(userID)
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
        print("delete success. allegedly")
    except:
        print("delete error")
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
def del_user_tasks(id):
    _SQL = "DELETE FROM tasks WHERE userID = '%s'" % (id)
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





