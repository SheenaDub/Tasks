from flask import Flask, render_template, request, redirect, url_for, abort


from db import *

app = Flask(__name__)

loggedIn = False
userID=0

@app.route('/')
def index():
    if loggedIn:
        id=getUserID()
        createConnection()
        username = getUserName(id)
        uname = username[0]['username']
        return render_template('index.html', id=id, user=uname)
    else:
        return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    uname = str(request.form['username'].strip())
    upass = str(request.form['password'].strip())
    createConnection()
    createUser(uname, upass)
    return render_template('login.html', title="Please log in")

@app.route('/loginB')
def loginByButton():
    return render_template('login.html', title="Please log in")

def getUserID():
    global userID
    return userID

@app.route('/login', methods=['POST'])
def login():
    uname = str(request.form['username'].strip())
    upass = str(request.form['password'].strip())
    createConnection()
    result = checkUser(uname,upass)
    if result is None:
        return render_template('login.html', title="Log in failed. Please try again")
    elif len(result) is 2:
        id = result[1]
        global loggedIn
        loggedIn=True
        global userID
        userID=id
        return render_template('index.html', user=uname, id=id, log=loggedIn)
    else:
        return render_template('login.html', title="Log in failed. Please try again")

@app.route('/logout', methods=['POST','GET'])
def logout():
    global userID
    userID=0
    global loggedIn
    loggedIn = False
    print("log out called ", loggedIn)
    return render_template('login.html', title="Goodbye!", log=loggedIn)


@app.route('/createnew')
def create() -> 'html':
    id = getUserID()
    createConnection()
    username = getUserName(id)
    uname = username[0]['username']
    return render_template('createnew.html', the_title='Create a new task', log=loggedIn, id=id, user=uname)


@app.route('/shownewtask', methods=['POST','GET'])
def showNew() -> 'html':
    name = request.form['taskname']
    detail = request.form['taskdetail']
    deadline = request.form['taskdeadline']
    id=getUserID()
    createConnection()
    writeTask(id, name, detail, deadline)
    createConnection()
    username= getUserName(id)
    uname=username[0]['username']
    return render_template('shownewtask.html', taskname=name, taskdetail=detail, taskdeadline=deadline, id=id, uname=uname, log=loggedIn)

@app.route('/showall', methods=['POST','GET'])
def showAllTasks():
    id=request.form['userId'].strip()
    id_as_int=int(id)
    createConnection()
    tasks = getUserTasksAsList(id_as_int)
    createConnection()
    username = getUserName(id_as_int)
    uname = username[0]['username']
    return render_template('showall.html', tasks=tasks, uname=uname, id=id, log=loggedIn)

@app.route('/<string:taskname>', methods=['POST','GET'])
def showSelectedTask(taskname):
    global userID
    userID = getUserID()
    createConnection()
    task = getOneTask(taskname)
    if not task:
        abort(404)
        print("list is empty")
    return render_template('showone.html', task=task, id=userID, log=loggedIn)


@app.route('/editselected', methods=['POST','GET'])
def editSelected() -> 'html':
    task = request.form['editTask']
    task = task.strip()
    id = request.form['userID'].strip()
    id_as_int = int(id)
    createConnection()
    thisTask = getOneTask(task)
    return render_template('editselected.html', the_title='Edit a task', thisTask=thisTask, id=id_as_int, log=loggedIn)


@app.route('/editThisTask', methods=['POST','GET'])
def editThisTask():
    name = request.form['taskname'].strip()
    detail = request.form['taskdetail'].strip()
    deadline = request.form['taskdeadline'].strip()
    oldname = request.form['oldName'].strip()
    id = request.form['userID'].strip()
    id_as_int = int(id)
    createConnection()
    editTask(name, detail, deadline, oldname)
    return render_template('index.html', id=id_as_int, log=loggedIn)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.route("/delete", methods=['POST','GET'])
def delTask():
    if request.method == 'POST':
        task = request.form['deleteTask']
        createConnection()
        deleteATaskbyName(task)
        id = request.form['userID'].strip()
        id_as_int = int(id)
        createConnection()
        username = getUserName(id_as_int)
        uname = username[0]['username']
    return render_template('index.html', id=id_as_int, log=loggedIn, user=uname)

@app.route("/clearAll", methods=['POST'])
def clearAllTasks():
    id = request.form['userId'].strip()
    id_as_int = int(id)
    createConnection()
    del_user_tasks(id_as_int)
    print("clear all called ", loggedIn)
    createConnection()
    username = getUserName(id_as_int)
    uname = username[0]['username']
    return render_template('index.html', the_title='Tasks cleared!', id=id_as_int, log=loggedIn, user=uname)




if __name__ == '__main__':
    app.run(debug=True)