from flask import Flask, render_template, request

from db import *

app = Flask(__name__)

@app.route('/')
def hello() -> 'html':
	return render_template('index.html', the_title='Welcome!')

@app.route('/createnew')
def create() -> 'html':
	return render_template('createnew.html', the_title='Create a new task')


@app.route('/shownewtask', methods=['POST','GET'])
def showNew() -> 'html':
	name = request.form['taskname']
	detail = request.form['taskdetail']
	deadline = request.form['taskdeadline']
	print("name is ", name)
	createConnection()
	writeTask(name,detail,deadline)
	return render_template('shownewtask.html', the_title='Your new task', taskname=name, taskdetail=detail, taskdeadline=deadline,)



@app.route('/showall', methods=['POST'])
def showAllTasks():
	print("this shows all tasks")
	getTasks()
	return render_template('showall.html', the_title='Your saved tasks')


@app.route("/display", methods=['POST','GET'])
def displayTasks():
    createConnection()
    tasks = getTasks()
    return tasks





if __name__ == '__main__':
	app.run(debug=True)