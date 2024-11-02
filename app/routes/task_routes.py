from flask import Blueprint, request, abort, make_response, Response
from ..models.task import Task
from ..db import db

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.post("")
def create_task():
     
    request_body = request.get_json()
    task = validate_request(request_body)

    db.session.add(task)
    db.session.commit()

    response = {
        'task': task.to_dict()
    }
    return response, 201

def validate_request(request_body):
    try:
        title = request_body["title"]
        description = request_body["description"]
        # completed_at = request_body["completed_at"]
    except:
        response = {"details": "Invalid data"}
        abort(make_response(response , 400))

    task = Task(title=title, description=description)
    return task

@tasks_bp.get("")
def get_all_tasks():

    query = db.select(Task)
    tasks = db.session.scalars(query.order_by(Task.id))

    tasks_response = []
    for task in tasks:
        tasks_response.append(
            task.to_dict()
        )
    return tasks_response


@tasks_bp.get("<task_id>")
def get_one_task(task_id):
    task = validate_task(task_id)

    return {'task': task.to_dict()}

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        response = {"details": f"task {task_id} invalid"}
        abort(make_response(response , 400))

    query = db.select(Task).where(Task.id == task_id)
    task = db.session.scalar(query)

    if not task:
        response = {"details": f"task {task_id} not found"}
        abort(make_response(response, 404))

    return task
    
    # we need to make requests for put and delete to finish wave 1! lets do this!
@tasks_bp.put("<task_id>")
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {'task': task.to_dict()}

@tasks_bp.delete("<task_id>")
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return {
        "details": f'Task {task.id} "{task.title}" successfully deleted'
        }






    