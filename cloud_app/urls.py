from django.urls import path
from .views import upload_file, delete_file, storage_summary, list_files

urlpatterns = [
    path('users/<uuid:user_id>/files', upload_file),
    path('users/<uuid:user_id>/files/<uuid:file_id>', delete_file),
    path('users/<uuid:user_id>/storage-summary', storage_summary),
    path('users/<uuid:user_id>/files/list', list_files),
]