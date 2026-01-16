from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        abstract = True

class APIRequestLog(BaseModel):
    api_endpoint = models.CharField(max_length=255)
    METHOD_CHOICES = [
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('DELETE', 'DELETE'),
        ('PATCH', 'PATCH'), # Added PATCH just in case, though spec list didn't explicitly say it, it's common. Spec said "Select: GET, POST, PUT, DELETE". I will stick to spec for now but might need PATCH later. 
    ]
    method = models.CharField(max_length=10, choices=[('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT'), ('DELETE', 'DELETE')])
    request_body = models.TextField(blank=True, null=True) # Renamed from request_payload to match spec
    response_body = models.TextField(blank=True, null=True) # Renamed from response_payload to match spec
    status_code = models.IntegerField()
    # timestamp field is redundant with created_at from BaseModel, but I will keep created_at as the source of truth or keep generic timestamp.
    # User spec says "API Log ... fields ... timestamps". 
    # BaseModel has created_at. I'll use that.
    
    def __str__(self):
        return f"{self.method} {self.api_endpoint} - {self.status_code}"
