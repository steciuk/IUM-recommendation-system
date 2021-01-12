import json
from datetime import datetime
from uuid import uuid4
from flask_restful import Resource
from services.recommendations.get_user_model import get_user_model
from services.recommendations.write_logs import write_logs
from services.models.models_controller import get_recommendations


class Models(Resource):
    def get(self, user_id):
        model = get_user_model(user_id)

        id = str(uuid4())
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        products = get_recommendations(user_id, model)

        recommendation = {"id": id, "date": date, "user_id": user_id, "products": products}

        write_logs(recommendation)

        return recommendation
