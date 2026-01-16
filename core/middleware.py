import json
import logging
import time
from django.utils.deprecation import MiddlewareMixin
from .models import APIRequestLog

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        if request.path.startswith('/api/'):
            try:
                # Attempt to parse body (only works if not consumed, or if DRF didn't consume it yet via stream)
                # DRF views access request.data, so request.body might differ or be unavailable if stream consumed.
                # Use a safe way.
                request_payload = ''
                if request.method in ['POST', 'PUT', 'PATCH']:
                    try:
                        if request.content_type == 'application/json':
                            request_payload = request.body.decode('utf-8')
                        else:
                            request_payload = str(request.POST.dict())
                    except Exception:
                        request_payload = '<Could not read payload>'
                
                response_payload = ''
                # Only log response if it's text/json
                if 'application/json' in response.get('Content-Type', ''):
                    try:
                        response_payload = response.content.decode('utf-8')
                    except Exception:
                        response_payload = '<Could not decode response>'
                
                APIRequestLog.objects.create(
                    api_endpoint=request.path,
                    method=request.method,
                    request_body=request_payload[:5000], # Trucate if too long
                    response_body=response_payload[:5000],
                    status_code=response.status_code
                )
            except Exception as e:
                logger.error(f"Error logging request: {e}")
        
        return response
