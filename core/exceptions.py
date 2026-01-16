from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    if response is not None:
        custom_response_data = {
            'status': 'error',
            'message': 'An error occurred',
            'errors': response.data
        }

        # Customize message based on error detail if available
        if isinstance(response.data, dict) and 'detail' in response.data:
            custom_response_data['message'] = response.data['detail']
            del custom_response_data['errors']['detail']
            if not custom_response_data['errors']:
                del custom_response_data['errors']
        elif isinstance(response.data, list):
             custom_response_data['message'] = 'Validation error'
             
        response.data = custom_response_data

    return response
