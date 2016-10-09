from flask import Flask, jsonify, abort, make_response, request
import uuid

app = Flask(__name__)

# Define the tasks here
tasks = [
    {
        'id': str(uuid.uuid4()),
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': str(uuid.uuid4()),
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]


@app.route("/")
def home():
    return "Hello! World"


@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})


@app.route("/tasks/<task_id>", methods=['GET'])
def get_task(task_id):
    requested_task = None
    for task in tasks:
        if task['id'] == task_id:
            requested_task = task
    if not requested_task:
        abort(404)
    else:
        return make_response(jsonify({'task': requested_task}), 200)


@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(403)
    else:
        task = {
                    'id' : str(uuid.uuid4()),
                    'title': request.json['title'],
                    'description': request.json['description'],
                    'done': request.json['done']
        }
        tasks.append(task)
        return make_response(jsonify({'tasks': tasks}), 201)


@app.route("/tasks/<task_id>", methods=['PUT', 'POST'])
def update_task(task_id):
    if not request.json or not 'title' in request.json:
        abort(403)
    else:
        requested_task = None
        for task in tasks:
            if task["id"] == task_id:
                requested_task = task
        requested_task['title'] = request.json.get('title', requested_task['title'])
        requested_task['description'] = request.json.get('description', requested_task['description'])
        requested_task['done'] = request.json.get('done', requested_task['done'])
        return make_response(jsonify({'task': requested_task}), 201)


@app.route("/tasks/<task_id>", methods=['DELETE'])
def delete_task(task_id):
    requested_task = None
    for task in tasks:
        if task["id"] == task_id:
            requested_task = task
    if not requested_task:
        abort(404)
    else:
        tasks.remove(requested_task)
        return jsonify({'Result': True})



@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True, port=5053)