from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # our stuff
        data = request.get_json()
        task_content = data['content']
        new_task = Todo(content=task_content)
        print(data)
        try:
            db.session.add(new_task)
            db.session.commit()
            return jsonify({'response': 'success yay!', 'content': content})
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        # find out how
        print('It is not a post request')


if __name__ == "__main__":
    app.run(debug=True)


