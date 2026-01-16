from rest_framework.renderers import JSONRenderer

class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code
        
        # If data is already standardized (e.g. by exception handler), use it as is
        if isinstance(data, dict) and 'status' in data and 'message' in data:
             return super().render(data, accepted_media_type, renderer_context)

        response_data = {
            'status': 'success',
            'message': 'Operation successful',
            'data': data
        }

        if not str(status_code).startswith('2'):
            response_data['status'] = 'error'
            response_data['message'] = 'Operation failed'
            response_data['data'] = None
            if isinstance(data, dict) and 'detail' in data:
                 response_data['message'] = data['detail']
            elif isinstance(data, dict):
                 # Pass through validation errors or other info as data or errors
                 # But ideally structure should be consistent. 
                 # For now, let's put it in data key if it's not standard
                 response_data['data'] = data
            
        return super().render(response_data, accepted_media_type, renderer_context)
