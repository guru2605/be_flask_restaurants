from flask import jsonify


class FailedException(Exception):
    @staticmethod
    def handle_failed_exception(error):
        return jsonify({'status_id': 0, 'reason': str(error)}), 400
