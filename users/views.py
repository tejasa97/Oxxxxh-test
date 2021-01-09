from rest_framework import generics, permissions, mixins
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from .serializers import UserSerializer, RegisterSerializer
import logging

access_log = logging.getLogger("access")


class Register(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args,  **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        access_log.info(f"User {user} successfully signed up")

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "registered",
        })


class TokenObtainPairViewCustom(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        access_log.info(f"User {serializer._kwargs['data']['username']} successfully logged in")
        return Response(serializer.validated_data, status=200)
