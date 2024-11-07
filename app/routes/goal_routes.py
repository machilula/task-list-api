from flask import Blueprint, request
from .route_utilities import create_model, validate_model
from ..models.goal import Goal
from .route_utilities import create_model, validate_model, get_models_by_filters
from ..db import db

bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json()
    return create_model(Goal, request_body)

@bp.get("")
def get_all_goals():
    return get_models_by_filters(Goal, request.args)

@bp.get("<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return {"goal": goal.to_dict()}

@bp.put("<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    db.session.commit()

    return {'goal': goal.to_dict()}

@bp.delete("<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return {
        "details": f'Goal {goal.id} "{goal.title}" successfully deleted'
        }



