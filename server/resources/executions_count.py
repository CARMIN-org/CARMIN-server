from flask_restful import Resource
from server.resources.decorators import login_required, get_db_session
from server.database.queries.executions import get_execution_count_for_user


class ExecutionsCount(Resource):
    @login_required
    @get_db_session
    def get(self, user, db_session):
        return get_execution_count_for_user(user.username, db_session)
