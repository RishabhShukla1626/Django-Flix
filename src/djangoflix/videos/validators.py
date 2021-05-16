from django.core.exceptions import ValidationError
import os

def file_validator(file):
    ext = os.path.splitext(file.name)[1]
    valid_extensions = ['.MP4', '.MOV', '.WMV', '.FLV', '.AVI', '.AVCHD', '.WebM', '.MKV']
    if not ext.upper() in valid_extensions:
        raise ValidationError('Unsupported file Type.')

