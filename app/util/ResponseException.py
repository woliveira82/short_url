from flask import jsonify


class ResponseException(Exception):


    def __init__(self, status_code, message='', data=None):
        self.status_code = status_code
        self.message = message
        self.data = data


    def response(self):
        response = jsonify({
            'status_code': self.status_code,
            'message': self.message,
            'data': self.data,
        })
        response.status_code = self.status_code
        return response
