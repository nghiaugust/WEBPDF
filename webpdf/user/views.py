from rest_framework import viewsets, generics, permissions, status
from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
import requests
from django.shortcuts import get_object_or_404

# Create your views here.
# user
class IsSelf(permissions.BasePermission):
    #Custom permission to only allow users to access their own data.
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return obj == request.user  # Chỉ cho phép truy cập nếu obj là chính user đang đăng nhập
    
class UserViewSet(viewsets.ViewSet,
                  generics.CreateAPIView,
                  generics.RetrieveAPIView):
    queryset = User.objects.filter(is_active= True)
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            # Sử dụng quyền kiểm tra nếu đây là tài khoản của chính người dùng
            return [permissions.IsAuthenticated(), IsSelf()]
        return [permissions.AllowAny()]

    def retrieve(self, request, *args, **kwargs):
        # Lấy thông tin user từ URL (thông qua pk)
        user = get_object_or_404(User, pk=kwargs.get('pk'))

        # Kiểm tra quyền truy cập
        self.check_object_permissions(request, user)

        # Nếu hợp lệ, trả về thông tin user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LoginUser(generics.GenericAPIView):
    """
    API for user login. Accepts username and password,
    automatically adds client_id and client_secret.
    """
    def post(self, request, *args, **kwargs):
        # Lấy dữ liệu username và password từ request
        username = request.data.get('username')
        password = request.data.get('password')

        # Kiểm tra xem username và password có đủ không
        if not username or not password:
            return Response(
                {"error": "Missing username or password."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Lấy client_id và client_secret từ settings
        client_id = 'q7DRZB1xBqrvXmthNZ9AzjVaJPJaSPd4cNgqniaT'
        client_secret = 'mLh5YgszpJjTtyLzLSwlkzjrUuCNIrpFphOjh0T2VI7kyZA2GVjeZXY2bpyZF76ug95A9Un6MI5NJRmAiVc908vBh7GrQJIc5jmlQLOFAu0BKZaePit7GKV5SrqVEqhf'

        if not client_id or not client_secret:
            return Response(
                {"error": "OAuth2 client_id or client_secret is not configured."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Endpoint của OAuth2 để lấy token
        token_url = 'http://127.0.0.1:8000/o/token/'

        # Payload gửi tới endpoint OAuth2
        payload = {
            'grant_type': 'password',
            'username': username,
            'password': password,
            'client_id': client_id,
            'client_secret': client_secret,
        }

        # Gửi yêu cầu tới /o/token/
        try:
            response = requests.post(token_url, data=payload)
            if response.status_code == 200:
                # Trả về token nếu thành công
                return Response(response.json(), status=status.HTTP_200_OK)
            else:
                # Trả về lỗi nếu thông tin đăng nhập không đúng
                return Response(
                    {
                        "error": "Invalid credentials or unauthorized.",
                        "details": response.json(),
                    },
                    status=response.status_code
                )
        except requests.exceptions.RequestException as e:
            # Xử lý lỗi khi không kết nối được tới OAuth2 server
            return Response(
                {"error": "Failed to connect to the token endpoint.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )