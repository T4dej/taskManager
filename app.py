from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Task.db"
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    data_created = db.Column(db.DateTime, default=datetime.utcnow)
    lists = db.relationship("List", backref="task", lazy="joined")

    def __repr__(self):
        return "<Task %r>" % self.id

class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    list_content = db.Column(db.String(200), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"), nullable=False)


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        task_content = request.form["content"]
        new_task = Task(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue adding your cost"
    else:
        tasks = Task.query.order_by(Task.data_created).all()
        return render_template("index.html", tasks=tasks)

@app.route("/add/<int:id>", methods=["GET", "POST"])
def add(id):
    if request.method == "POST":
        list_content = request.form["list"]
        new_list = List(list_content=list_content, task_id=id)
        try:
            db.session.add(new_list)
            db.session.commit()
            lists = db.session.query(List.list_content).filter(id==List.task_id).all()
            return render_template("add.html", site=id, lists=lists)
        except:
            return "There was an issue adding your list"
    else:
        #lists = List.query.order_by(List.id).all()
        #lists = db.session.query(Task, List).filter(Task.id == List.task_id).all()
        lists = db.session.query(List.list_content).filter(id==List.task_id).all()
        return render_template("add.html", site=id, lists=lists)



# Delete a task at index 
@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Task.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "There was a problem deleting that task!"

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    task = Task.query.get_or_404(id)

    if request.method == "POST":
        task.content = request.form["content"]

        try:
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue updating your task!"
    else:
        return render_template("update.html", task=task)

@app.route("/update/<int:id>", methods=["GET", "POST"])
def updateList(id):
    listQuery = List.query.get_or_404(id)

    if request.method == "POST":
        listQuery.list_content = request.form["list"]

        try:
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue updating your task!"
    else:
        return render_template("update.html", lists=listQuery)


#Update delete signle task button


""" Add delete a full list at specific task

@app.route("/deleteall/<int:id>")
def deleteall(id):
    try:
        #db.session.query(Task).delete()
        delete_List = List.query.get_or_404(id)
        db.session(delete_List).delete()
        db.session.commit()
        return redirect("/")
    except:
        return "There was an issue deleting all tasks!" """

if __name__ == "__main__":
    app.run(debug=True)