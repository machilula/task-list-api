from flask import Blueprint, request, abort, make_response, Response
from ..models.task import Task
from datetime import date
from ..db import db
import os
import requests

bp = Blueprint("bp", __name__, url_prefix="/tasks")

@bp.post("")
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

@bp.get("")
def get_all_tasks():

    query = db.select(Task)

    # this function needs some tidying up

    title_param = request.args.get("title")
    if title_param:
        query = query.where(Task.title.ilike(f"%{title_param}"))
    
    description_param = request.args.get("description")
    if description_param:
        query = query.where(Task.description.ilike(f"%{description_param}%"))

    # the code commented below works, but interferes with the logic of asc and desc
    # elif sort_param:
    #     query = query.order_by(getattr(Task, sort_param))

    # maybe we can do a try except helper function for this to include the code above
    # going back to this, the filters helper in flasky wouldnt work for the code below
    # the task model has no attribute "asc" or "desc"

    sort_param = request.args.get("sort")
    if sort_param == "asc":
        query = query.order_by(Task.title)
    if sort_param == "desc":
        query = query.order_by(Task.title.desc())

    tasks = db.session.scalars(query.order_by(Task.id))

    tasks_response = [task.to_dict() for task in tasks]

    return tasks_response


@bp.get("<task_id>")
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
@bp.put("<task_id>")
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {'task': task.to_dict()}

@bp.delete("<task_id>")
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return {
        "details": f'Task {task.id} "{task.title}" successfully deleted'
        }

# heyyy stay with me, we are doing patch for wave 3 with a custom endpoint
# lets create patch first, then worry about refactoring into route utilities


@bp.patch("<task_id>/mark_complete")
def mark_task_complete(task_id):
    task = validate_task(task_id)

    task.completed_at = date.today()

    slack_message = post_slack_message(task)

    db.session.commit()

    return {'task': task.to_dict()}

@bp.patch("<task_id>/mark_incomplete")
def mark_task_incomplete(task_id):
    task = validate_task(task_id)

    task.completed_at = None
    db.session.commit()

    return {'task': task.to_dict()}

def post_slack_message(task):

    path = "https://slack.com/api/chat.postMessage"

    token = os.environ.get('SLACK_API_KEY')
    headers = {
        "Authorization": f'Bearer {token}'
        }
    post_message = {
        "channel": "api-test-channel",
        "text": f"Someone just completed the task {task.title}"
        }
    
    response = requests.post(path, headers=headers, json=post_message)

    return response





    