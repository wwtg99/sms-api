from flask_restful import Resource


class Health(Resource):

    def get(self):
        return {'message': 'ok'}, 200
