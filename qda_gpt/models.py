from django.db import models

# Model to handle uploaded files
class UploadedFile(models.Model):
    # Stores the uploaded file
    file = models.FileField(upload_to='uploads/')
    # Records the date and time when the file was uploaded automatically
    uploaded_at = models.DateTimeField(auto_now_add=True)

