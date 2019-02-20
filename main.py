from flask import Flask, render_template, request, redirect, url_for, abort

from db import *

app = Flask(__name__)

@app.route('/')
def hello() -> 'html':
	return render_template('index.html')

@app.route('/createnew')
def create() -> 'html':
	return render_template('createnew.html', the_title='Create a new task')


@app.route('/shownewtask', methods=['POST','GET'])
def showNew() -> 'html':
	name = request.form['taskname']
	detail = request.form['taskdetail']
	deadline = request.form['taskdeadline']
	createConnection()
	writeTask(name,detail,deadline)
	return render_template('shownewtask.html', the_title='Your new task', taskname=name, taskdetail=detail, taskdeadline=deadline)

@app.route('/showall', methods=['POST','GET'])
def showAllTasks():
    createConnection()
    tasks = getTasksAsList()
    return render_template('showall.html', tasks=tasks, the_title='All your tasks')

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
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# @app.before_request
# def before_request():
#     # any code needed before request is made eg check authentication



@app.route("/delete", methods=['POST','GET'])
def delTask():
    if request.method == 'POST':
        task = request.form['deleteTask']
        print("delete in main called ", task)
        print("id type ", type(task))
        createConnection()
        deleteATaskbyName(task)
    return render_template('index.html', the_title='Welcome!')

@app.route("/clearAll", methods=['POST','GET'])
def clearAllTasks():
    createConnection()
    empty_table()
    print("clear all called ")
    return render_template('index.html')




#js method - prob going to delete this
@app.route("/display", methods=['POST','GET'])
def displayTasks():
    createConnection()
    tasks = getTasks()
    return tasks




if __name__ == '__main__':
	app.run(debug=True)