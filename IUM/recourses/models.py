from flask_restful import Resource
from services.recommendations.get_user_model import get_user_model
from services.models.models_controller import get_recommendations


class Models(Resource):
    def get(self, user_id):
        model = get_user_model(user_id)
        recommendations = get_recommendations(user_id, model)

        return recommendations
