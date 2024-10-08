from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from server.models import APIResponse
from django.contrib.auth import login as django_login
from .serializers import UserSerializer
from django.contrib.auth.models import User
import json

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    body = json.loads(request.body.decode('utf-8'))
    username = body['username']
    password = body['password']

    if not username or not password:
        return Response(APIResponse(success=False, data={}, message="Tên đăng nhập và mật khẩu là bắt buộc").__dict__(),
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response(APIResponse(success=False, data={}, message="Thông tin đăng nhập không chính xác").__dict__(),
                        status=status.HTTP_404_NOT_FOUND)

    if not user.check_password(password):
        return Response(APIResponse(success=False, data={}, message="Thông tin đăng nhập không chính xác").__dict__(),
                        status=status.HTTP_401_UNAUTHORIZED)
    if not user.is_active:
        return Response(APIResponse(success=False, data={},
                                    message="Tài khoản bị khóa. Vui lòng liên hệ để biết thêm chi tiết").__dict__(),
                        status=status.HTTP_401_UNAUTHORIZED)

    django_login(request, user)

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    # logged_account = UserSerializer(user).data
    user_serializer = UserSerializer(user).data

    return Response(APIResponse(success=True, data={'access_token': access_token, 'user': user_serializer},
                                message="").__dict__(), status=status.HTTP_200_OK)
