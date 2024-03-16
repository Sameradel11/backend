from django.shortcuts import render
from .models import CustomUser, Company, Notes
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializer import UserSerializer, CompanySerializer, NoteSerializer
from rest_framework import generics, status
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
import jwt
import datetime
# @api_view(['POST'])
# def CompanyView(request):
#     serializer = CompanySerializer(data=request.data)
#     if serializer.is_valid(raise_exception=True):
#         response=serializer.save()
#         return Response(response.data)
#     else:
#         return Response(serializer.errors)


class CompanyView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            response = serializer.save()
            return Response(response)
        else:
            return Response(serializer.errors)

    def put(self, request, *args, **kwargs):
        email = request.data.get('user').get('email', None)
        if email is None:
            return Response({'error': 'Email is required in the request data.'},
                            status=status.HTTP_400_BAD_REQUEST)
        instance = Company.objects.filter(user__email=email).first()
        serializer = CompanySerializer(instance=instance, data=request.data)
        print('serializer is valid')
        serializer.update(instance, request.data)
        return Response(CompanySerializer(instance).data)



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        # ...

        return token

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getNotes(request):
    user=request.user
    notes = Notes.objects.filter(user=user)
    print(notes)
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)



# class UserView(APIView):
#     def get(self, request):
#         print(request)
#         token = request.COOKIES.get('jwt')
#         if not token:
#             raise AuthenticationFailed('Unauthenticated!')
#         try:
#             payload = jwt.decode(token, 'secret', algorithms=['HS256'])
#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed('Unauthenticated')
#         user = CustomUser.objects.get(id=payload['id'])
#         serializer = UserSerializer(user)
#         return Response(serializer.data)


# @api_view(['POST'])
# def UserView(request):
#     serializer = UserSerializer(data=request.data)
#     if serializer.is_valid():
#         response = serializer.save()
#         print(type(response))
#         print(response)
#         return Response(response)
#     else:
#         return Response(serializer.errors)


# class CompanyView(generics.ListAPIView, generics.CreateAPIView,
#                 generics.RetrieveAPIView,generics.UpdateAPIView):
#     queryset = Company.objects.all()
#     serializer_class = CompanySerializer
#     def perform_create(self,serializer):
#         serializer=serializer.save()
#         print(f"serializer is {serializer}")
#         return serializer

#     def get(self, request, *args, **kwargs):
#         pk = kwargs.get("pk")
#         if pk is None:
#             return self.list(request, *args, **kwargs)
#         else:
#             return self.retrieve(request, *args, **kwargs)

#     def post(self, request,*args,**kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         new_serializer_data=self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(new_serializer_data)


# class Stakeholders(generics.ListAPIView,generics.CreateAPIView):
#     queryset=Stakeholders.objects.all()
#     serializer_class=StakeholdersSerializer
#     def get(self,request,*args,**kwargs):
#         return self.list(request,*args,**kwargs)

#     def post(self,request,*args,**kwargs):
#         return self.create(request,*args,**kwargs)

# class LoginView(APIView):
#     def create_access_token(email):
#         return jwt.encode({
#             'email': email,
#             'exp': datetime.datetime.utcnow()+datetime.timedelta(minutes=60),
#             'iat': datetime.datetime.utcnow()
#         }, 'secret', algorithm='HS256')

#     def create_refresh_token(email):
#         return jwt.encode({
#             'email': email,
#             'exp': datetime.datetime.utcnow()+datetime.timedelta(days=7),
#             'iat': datetime.datetime.utcnow()
#         }, 'secret', algorithm='HS256')

#     def post(self, request):

#         # def create_access_token(email):
#         #     return jwt.encode({
#         #     'email': email,
#         #     'exp': datetime.datetime.utcnow()+datetime.timedelta(minutes=60),
#         #     'iat': datetime.datetime.utcnow()
#         # }, 'secret', algorithm='HS256')

#         # def create_refresh_token(email):
#         #     return jwt.encode({
#         #         'email': email,
#         #         'exp': datetime.datetime.utcnow()+datetime.timedelta(days=7),
#         #         'iat': datetime.datetime.utcnow()
#         #     }, 'secret', algorithm='HS256')

#         email = request.data['email']
#         password = request.data['password']
#         user = CustomUser.objects.filter(email=email).first()
#         if user is None:
#             raise AuthenticationFailed("user not exist")
#         if not user.check_password(password):
#             raise AuthenticationFailed("password isn't correct")

#         access_token = jwt.encode({
#             'email': email,
#             'exp': datetime.datetime.utcnow()+datetime.timedelta(days=1),
#             'iat': datetime.datetime.utcnow()
#         }, 'secret', algorithm='HS256')

#         refresh_token = jwt.encode({
#             'email': email,
#             'exp': datetime.datetime.utcnow()+datetime.timedelta(days=7),
#             'iat': datetime.datetime.utcnow()
#         }, 'secret', algorithm='HS256')

#         print({access_token})
#         response = Response()
#         response.set_cookie(key='jwt', value=access_token, httponly=True)
#         response.data = {
#             'roles': [2001, 5150],
#             'access': access_token,
#             'refresh': refresh_token
#         }
#         return response

