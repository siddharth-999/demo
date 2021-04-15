from django.contrib.auth import authenticate, login
from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import User, FamilyRelation, RELATION_CHOICE
from .permissions import UserPermission, LoginSignupPermission, \
    FamilyRelativePermission, FamilyMemberPermission
from .serializers import (UserUpdateSerializer,
    UserDetailSerializer, LoginAuthSerializer,
    FamilyRelativeDetailSerializer,
    FamilyRelativeUpdateSerializer, 
    FamilyRelativeCreateSerializer, UserListSerializer)


class LoginAPIView(ObtainAuthToken, GenericAPIView):
    permission_classes = (AllowAny, LoginSignupPermission)
    serializer_class = LoginAuthSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                user_check = User.objects.get(
                    email__iexact=serializer.validated_data['username'].lower().strip(),
                    is_delete=False, is_active=True)
            except User.DoesNotExist:
                response = \
                    {
                        "detail": "We can't find that email address, please try again!",
                    }
                return Response(response, status.HTTP_401_UNAUTHORIZED)
            password = serializer.validated_data['password']
            user = authenticate(username=user_check.email, password=password)
            if user and user.is_authenticated:
                login(request, user)
                token_obj, created = Token.objects.get_or_create(user=user)
                return Response({"token": str(token_obj.key),
                                 "user": user.id},
                                status=status.HTTP_200_OK)
            return Response({"detail": "The password you entered does not "
                                       "match our records, please try again"},
                            status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.error_messages,
                            status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, UserPermission,)
    http_method_names = ["get", "patch"]

    def get_queryset(self):
        username = self.request.user.username
        return User.objects.filter(username=username,
                                   is_delete=False)

    def get_serializer_class(self):
        if self.action == "partial_update":
            return UserUpdateSerializer
        else:
            return UserDetailSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class FamilyMemberViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, FamilyMemberPermission,)
    queryset = User.objects.exclude(is_superuser=True).order_by('id')
    http_method_names = ["get"]
    serializer_class = UserListSerializer

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class FamilyRelativeViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, FamilyRelativePermission,)
    queryset = FamilyRelation.objects.all()
    http_method_names = ["get", "patch", "delete", "post"]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('relation', 'relative')

    def get_serializer_class(self):
        if self.action == "create":
            return FamilyRelativeCreateSerializer
        elif self.action == "partial_update":
            return FamilyRelativeUpdateSerializer
        return FamilyRelativeDetailSerializer

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def relations(self, request):
        data = []
        for relation in RELATION_CHOICE:
            data.append(
                {
                    'id': relation[0],
                    'relation': relation[1]
                }
            )
        return Response(data, status=status.HTTP_200_OK)
