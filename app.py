from datetime import datetime as dt
from pprint import pprint

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    dateTime = db.Column(db.DateTime, default=dt.now)

    def __repr__(self):
        return f"{self.title}- {self.desc} duration :- {self.dateTime}"


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        todo_Title = request.form['title']
        todo_Desc = request.form['desc']
        if todo_Title and todo_Desc:
            todo = Todo(title=todo_Title, desc=todo_Desc)
            db.session.add(todo)
            db.session.commit()
            return redirect(request.referrer)
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)


@app.route('/deleteDatabase')
def deleteDatabase():
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print(f'Clear table {table}')
        db.session.execute(table.delete())
    db.session.commit()
    return redirect("/")


@app.route('/delete/<int:srNo>')
def delete(srNo):
    todo = Todo.query.filter_by(sno=srNo).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


@app.route('/update/<int:srNo>', methods=['POST','GET'])
def update(srNo):
    if request.method == 'POST':
        todo_Title = request.form['title']
        todo_Desc = request.form['desc']
        if todo_Title and todo_Desc:
            todo = Todo.query.filter_by(sno=srNo).first()
            todo.title=todo_Title
            todo.desc=todo_Desc
            db.session.add(todo)
            db.session.commit()
            return redirect("/")
    todo = Todo.query.filter_by(sno=srNo).first()
    return render_template('update.html', todo=todo)


if __name__ == '__main__':
    app.run(debug=True)