import logging
from flask_restful import Resource, reqparse
from app.sms import get_sms


parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('receivers', help='Comma separated receivers.', required=True)
parser.add_argument('template', help='Notification template name.', required=True)
parser.add_argument('params', help='Notification template params.', type=dict)


class Sms(Resource):

    def post(self):
        args = parser.parse_args()
        sms = get_sms()
        try:
            res = sms.send(**args)
        except Exception as e:
            logging.error(e)
            return {'message': 'failed'}, 500
        if res.status_code < 300:
            return {'message': 'send'}, 200
        else:
            logging.error('Send sms failed with {}'.format(res.text))
            return {'message': 'failed'}, 500
