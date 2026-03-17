from django.db import transaction
from django.db.models import Sum
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import User, File, UserFile
from .serializers import UserFileSerializer

MAX_STORAGE = 500 * 1024 * 1024

@api_view(['POST'])
def upload_file(request, user_id):
    file_name = request.data.get('file_name')
    file_size = int(request.data.get('file_size'))
    file_hash = request.data.get('file_hash')

    try:
        with transaction.atomic():
            user = User.objects.select_for_update().get(id=user_id)

            used = UserFile.objects.filter(
                user=user, is_deleted=False
            ).aggregate(total=Sum('file__file_size'))['total'] or 0

            if used + file_size > MAX_STORAGE:
                return Response({"error": "Storage limit exceeded"}, status=400)

            if UserFile.objects.filter(
                user=user, file_name=file_name, is_deleted=False
            ).exists():
                return Response({"error": "File name exists"}, status=400)

            file_obj, _ = File.objects.get_or_create(
                file_hash=file_hash,
                defaults={'file_size': file_size}
            )

            UserFile.objects.create(
                user=user,
                file=file_obj,
                file_name=file_name
            )

        return Response({"message": "Uploaded"})

    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
    
    
@api_view(['DELETE'])
def delete_file(request, user_id, file_id):
    try:
        file = UserFile.objects.get(id=file_id, user_id=user_id, is_deleted=False)
        file.is_deleted = True
        file.save()

        return Response({"message": "Deleted"})
    except UserFile.DoesNotExist:
        return Response({"error": "Not found"}, status=404)
    
    
@api_view(['GET'])
def storage_summary(request, user_id):

    used = UserFile.objects.filter(
        user_id=user_id, is_deleted=False
    ).aggregate(total=Sum('file__file_size'))['total'] or 0

    total_files = UserFile.objects.filter(
        user_id=user_id, is_deleted=False
    ).count()

    return Response({
        "used": used,
        "remaining": MAX_STORAGE - used,
        "total_files": total_files
    })
    
@api_view(['GET'])
def list_files(request, user_id):

    files = UserFile.objects.filter(user_id=user_id, is_deleted=False)
    serializer = UserFileSerializer(files, many=True)

    return Response(serializer.data)

