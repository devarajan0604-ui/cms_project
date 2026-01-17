from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError

def custom_exception_handler(exc, context):
    # Handle Django ValidationError by converting it to DRF ValidationError
    if isinstance(exc, DjangoValidationError):
        if hasattr(exc, 'message_dict'):
            exc = DRFValidationError(detail=exc.message_dict)
        elif hasattr(exc, 'messages'):
            exc = DRFValidationError(detail=exc.messages)
        else:
            exc = DRFValidationError(detail=str(exc))

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
