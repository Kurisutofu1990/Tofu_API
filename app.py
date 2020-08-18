from flask import Flask, request, jsonify
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# Question: Does the name of the function matter and where is it being executed?
# TODOS:
# 1) Protect the API, make it private
# 2) Deploy
# 3) Write tests
# 4) Try making requests to this API from a supersimple seperate FE app.
# 5) Possible bridge - integrate graphQL with it?

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # def __repr__(self):
    #     return '<Task %r>' % self.id

    def __init__(self, id, content, date_created):
        self.id = id
        self.content = content
        self.date_created = date_created
        

    def serialize(self):
        return {
                    "id": self.id,
                    "content": self.content,
                    "date_created": self.date_created
                }

@app.route('/todos', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        data = request.get_json()
        task_content = data['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return data
        except:
            # TODO format this response as json
            return 'There was an issue adding your task'
    # TODO else a good idea?, what if it get a PATCH request
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return jsonify({'tasks': list(map(lambda task: task.serialize(), tasks))}), 404

@app.route('/todos/<int:id>', methods=['DELETE', 'GET', 'POST'])
def doesThisMethodNameMatter(id):
    if request.method == 'DELETE':
        task_to_delete = Todo.query.get_or_404(id)

        try:
            db.session.delete(task_to_delete)
            db.session.commit()
            return task_to_delete.serialize()
        except:
            # TODO format this response as json
            return 'There was an issue with deleting your task'

    if request.method == 'GET':
        task = Todo.query.get_or_404(id)
        return task.serialize()
    
    if request.method == 'POST':
        task = Todo.query.get_or_404(id)
        data = request.get_json() 
        task.content = data['content']  
        try:
            db.session.commit()
            return task.serialize()
        except:
            return 'There was an issue updating your task'

if __name__ == "__main__":
    app.run(debug=True)


