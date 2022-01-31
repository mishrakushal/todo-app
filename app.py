from datetime import datetime
from logging import debug
from flask import Flask, request
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ---- HOMEPAGE ----
@app.route("/", methods=['POST', 'GET'])
def home():
	if request.method == 'POST':
		taskContent = request.form['content']
		newTask = Todo(content = taskContent)

		try:
			db.session.add(newTask)
			db.session.commit()
			return redirect('/')
		except:
			return "An unexpected error occurred while adding your task"
	tasks = Todo.query.order_by(Todo.date_created).all()
	return render_template("index.html", tasks = tasks)

# ---- DELETE PAGE ----
@app.route('/delete/<int:id>')
def delete(id):
	taskToDelete = Todo.query.get_or_404(id)

	try:
		db.session.delete(taskToDelete)
		db.session.commit()
		return redirect('/')
	except:
		return "An unexpected error occurred while deleting your task"

# ---- UPDATE PAGE ----
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
	task = Todo.query.get_or_404(id)

	if request.method == 'POST':
		task.content = request.form['content']

		try:
			db.session.commit()
			return redirect("/")
		except:
			return "An unexpected error occurred while updating your task"

	return render_template('update.html', task = task)


class Todo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.String(200), nullable=False)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)

	def __repr__(self):
		return '<Task %r>' %self.id



if __name__ == "__main__":
	app.run(debug = True)
