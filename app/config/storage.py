from django.core.files.storage import FileSystemStorage

OVERWRITE_STORAGE = FileSystemStorage(allow_overwrite=True)
