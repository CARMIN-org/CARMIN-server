from flask_restful import Resource
from server.database import db
from server.resources.decorators import login_required
from server.database.queries.executions import get_execution_count_for_user


class ExecutionsCount(Resource):
    @login_required
    def get(self, user):
        return get_execution_count_for_user(user.username, db.session)
