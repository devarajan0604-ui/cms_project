from django.db import models

class APIRequestLog(models.Model):
    api_endpoint = models.CharField(max_length=255)
    http_method = models.CharField(max_length=10)
    request_payload = models.TextField(blank=True, null=True)
    response_payload = models.TextField(blank=True, null=True)
    status_code = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.http_method} {self.api_endpoint} - {self.status_code}"
