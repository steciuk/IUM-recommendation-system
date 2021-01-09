from flask import Flask
from flask_restful import Api
from recourses.models import Models

app = Flask(__name__)
api = Api(app)

api.add_resource(Models, "/models", '/user/<string:user_id>')

if __name__ == "__main__":
    app.run(debug=True)
