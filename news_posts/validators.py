import os
from django.core.exceptions import ValidationError


def validate_file_extensions(file):
    """
    File Extension Validation
    """
    extension = os.path.splitext(file.name)[1]
    valid_extensions = ['.txt', '.docx', '.doc', '.odt', '.md', '.pdf']
    if not extension.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Supported ones are ' + ', '.join(valid_extensions))
