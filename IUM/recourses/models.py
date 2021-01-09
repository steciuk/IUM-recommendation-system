from flask_restful import Resource


class Models(Resource):
    def get(self, user_id):
        return {"data": {"user_id": user_id}}