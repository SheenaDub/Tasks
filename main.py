from flask import Flask, render_template, request, redirect, url_for, abort, session, g
import os

from db import *

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    if 'user' in session:
        return render_template('index.html')
    else:
        return render_template('login.html', title="Please log in")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user', None)
        uname = str(request.form['username'].strip())
        upass = str(request.form['password'].strip())
        print(uname,upass)
        createConnection()
        result = checkUser(uname, upass)
        if result is None:
            return render_template('login.html', title="Log in failed. Please try again")
        else:
            session['user'] = request.form['username']
            return render_template('index.html', title="Log in successful", user=session['user'])
    return render_template('login.html', title="Please log in")

@app.route('/signup', methods=['POST','GET'])
def signup():
    return render_template('signup.html', title="Please log in after sign up")


@app.route('/signupprocess', methods=['POST','GET'])
def signupprocess():
    uname = str(request.form['username'].strip())
    upass = str(request.form['password'].strip())
    createConnection()
    createUser(uname, upass)
    return render_template('login.html', title="Please log in after sign up")

@app.before_request
def before_request():
    if request.endpoint != 'signup' and request.endpoint != 'signupprocess'and request.endpoint != 'index' and request.endpoint != 'login' and request.endpoint != 'loginB':
        g.user = None
        if 'user' in session:
            g.user = session['user']
        else:
            return render_template('401.html')


@app.route('/logout', methods=['POST','GET'])
def logout():
    session.pop('user', None)
    return render_template('login.html', title="Goodbye!")


@app.route('/createnew')
def create() -> 'html':
    return render_template('createnew.html', the_title='Create a new task', user=session['user'])


@app.route('/shownewtask', methods=['POST','GET'])
def showNew() -> 'html':
    name = request.form['taskname']
    detail = request.form['taskdetail']
    deadline = request.form['taskdeadline']
    createConnection()
    writeTask(name, detail, deadline, session['user'])
    createConnection()
    return render_template('shownewtask.html', taskname=name, taskdetail=detail, taskdeadline=deadline, uname=session['user'])

@app.route('/showall', methods=['POST','GET'])
def showAllTasks():
    createConnection()
    tasks = getUserTasksAsList(session['user'])
    return render_template('showall.html', tasks=tasks, uname=session['user'])

@app.route('/<string:taskname>', methods=['POST','GET'])
def showSelectedTask(taskname):
    createConnection()
    task = getOneTask(taskname)
    if not task:
        abort(404)
        print("list is empty")
    return render_template('showone.html', task=task)


@app.route('/editselected', methods=['POST','GET'])
def editSelected() -> 'html':
    task = request.form['editTask']
    task = task.strip()
    createConnection()
    thisTask = getOneTask(task)
    return render_template('editselected.html', the_title='Edit a task', thisTask=thisTask)


@app.route('/editThisTask', methods=['POST','GET'])
def editThisTask():
    name = request.form['taskname'].strip()
    detail = request.form['taskdetail'].strip()
    deadline = request.form['taskdeadline'].strip()
    oldname = request.form['oldName'].strip()
    createConnection()
    editTask(name, detail, deadline, oldname)
    return render_template('index.html', user=session['user'])


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.route("/delete", methods=['POST','GET'])
def delTask():
    if request.method == 'POST':
        task = request.form['deleteTask']
        createConnection()
        deleteATaskbyName(task)
        createConnection()
    return render_template('index.html', title='Task deleted', user=session['user'])

@app.route("/clearAll", methods=['POST'])
def clearAllTasks():
    createConnection()
    del_user_tasks(session['user'])
    createConnection()
    return render_template('index.html', the_title='Tasks cleared!', user=session['user'])



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)