from flask import Blueprint, request, abort, make_response, Response
from ..models.task import Task
from ..db import db

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.post("")
def create_task():
     
    request_body = request.get_json()
    task = validate_request(request_body)
    response = task.to_dict()

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
    db.session.add(task)
    db.session.commit()

    return task

@tasks_bp.get("")
def get_all_tasks():

    query = db.select(Task)

    tasks = db.session.scalars(query.order_by(Task.id))

    tasks_response = []
    for task in tasks:
        tasks_response.append(
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,   
                "is_complete": task.check_completion()
            }
        )
    return tasks_response


@tasks_bp.get("<task_id>")
def get_one_task(task_id):
    task = validate_task(task_id)

    return task.to_dict()

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
    



# noice, we made a get request for all tasks and now we need to test it!
# works on postman GET ! now we need to test it with pytest




    