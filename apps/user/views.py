from django.contrib.auth import get_user_model
from django.contrib.auth import user_logged_out
# Register API
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, mixins
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from apps.user.models import APIUser
from apps.user.serializers import RegisterSerializer, LoginUserSerializer, UserSerializer, ChangePasswordSerializer, \
    UpdateUserSerializer, APIUserSerializer, AlterTokenValiditySerializer

# Create your views here.

User = get_user_model()


@method_decorator(name='post', decorator=swagger_auto_schema(tags=['user'],
                                                             operation_summary='Register user',
                                                             operation_description="Use this API to register user"
                                                             ))
class RegisterAPI(generics.CreateAPIView):
    """
        This api is used for registration of user
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class LoginAPI(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginUserSerializer

    @swagger_auto_schema(tags=['user'],
                         operation_summary='User login',
                         operation_description="Use this API to Login User")
    def post(self, request, *args, **kwargs):
        """
            This api used for login
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data
        user_serializer = UserSerializer(user, context=self.get_serializer_context()).data
        # login(request, user)
        return Response(
            user_serializer
        )
        # print(user)
        # return super(LoginAPI, self).post(request, format=None)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(tags=['user'],
                         operation_summary='User logout',
                         operation_description="Use this API to logout User")
    def post(self, request):
        """
            This API is used to log out authenticated user
        """
        user_logged_out.send(sender=request.user.__class__,
                             request=request, user=request.user)
        return Response({'status': True})


@method_decorator(name='post',
                  decorator=swagger_auto_schema(
                      tags=['user'],
                      operation_summary='Change user password',
                      operation_description="Use this API to change user password"
                  ))
class ChangePasswordView(generics.CreateAPIView):
    """
        User can change their password with this API
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'message': 'Password change successful'})


@method_decorator(name='post',
                  decorator=swagger_auto_schema(
                      tags=['user'],
                      operation_summary='Update user profile',
                      operation_description="Use this API to update user profile"
                  ))
class UpdateProfileView(generics.CreateAPIView):
    """
        This API is used to update profile detail of authenticated user.
    """
    serializer_class = UpdateUserSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj


class GetProfile(APIView):
    @swagger_auto_schema(tags=['user'],
                         auto_schema=None, operation_summary='Get user profile',
                         operation_description='Use this API to get user profile')
    def get(self, request, *args, **kwargs):
        return Response(UserSerializer(request.user, many=False).data)


class AlterTokenValidityView(APIView):
    serializer_class = AlterTokenValiditySerializer

    @swagger_auto_schema(
        tags=['API User'],
        operation_summary="Alter API user token validity",
        operation_description="""Alter API user token validity". 
    """
    )
    def post(self, request, *args, **kwargs):
        serialized = AlterTokenValiditySerializer(data=request.data)
        if serialized.is_valid(raise_exception=True):
            serialized.save()
        return Response({'message': 'Action performed successfully'})


@method_decorator(name='list', decorator=swagger_auto_schema(
    tags=['API User'],
    operation_summary="List of API users",
    operation_description="""List all API users. 
    """
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    tags=['API User'],
    operation_summary="Get API user item",
    operation_description="""Show full information for API user."""
))
@method_decorator(name='create', decorator=swagger_auto_schema(
    tags=['API User'],
    operation_summary="Create API user",
    operation_description="""Create a new API user"""
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    tags=['API User'],
    operation_summary="Delete API user"
))
class APIUserViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    queryset = APIUser.objects.all()
    serializer_class = APIUserSerializer
    permission_classes = [IsAuthenticated]
