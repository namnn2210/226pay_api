from django.db import models

# Create your models here.
class APIResponse:
    def __init__(self, success, data, message):
        self.success = success
        self.data = data
        self.message = message

    def __dict__(self):
        return {
            'success': self.success,
            'data': self.data,
            'message': self.message
        }