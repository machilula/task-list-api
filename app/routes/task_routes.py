from flask import Blueprint, request, abort, make_response, Response
from ..models.task import Task
from .route_utilities import create_model, validate_model, get_models_by_filters
from datetime import date
from ..db import db
import os
import requests

bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@bp.post("")
def create_task():
    request_body = request.get_json()
    return create_model(Task, request_body)


@bp.get("")
def get_all_tasks():
    return get_models_by_filters(Task, request.args)


@bp.get("<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    return {'task': task.to_dict()}

@bp.put("<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {'task': task.to_dict()}

@bp.delete("<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return {
        "details": f'Task {task.id} "{task.title}" successfully deleted'
        }


@bp.patch("<task_id>/mark_complete")
def mark_task_complete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = date.today()

    post_slack_message(task)

    db.session.commit()

    return {'task': task.to_dict()}

@bp.patch("<task_id>/mark_incomplete")
def mark_task_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None
    db.session.commit()

    return {'task': task.to_dict()}


# we might move the func below to route utilities

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





    