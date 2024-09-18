from rest_framework.decorators import api_view
from .serializer import UserSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets

class UserViewSet(viewsets.ModelViewSet):
    queryset= User.objects.all()
    serializer_class = UserSerializer
    

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])

    if not user.check_password(request.data['password']):
        return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
    
    #Prevent multiple sessions
    if Token.objects.filter(user=user).exists():
       return Response({"error": "User is already logged in on another device."}, status=status.HTTP_403_FORBIDDEN)
    
    # Invalidate any existing token for the user
    Token.objects.filter(user=user).delete()
    

    token, created = Token.objects.get_or_create(user=user)
    serializer= UserSerializer(instance=user)

    return Response({"token":token.key,"user":serializer.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
def register(request):
    serializer =  UserSerializer(data = request.data)

    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=serializer.data['username'])
        user.set_password(serializer.data['password'])
        user.save()

        token = Token.objects.create(user=user)
        return Response({'token': token.key, "user": serializer.data}, status=status.HTTP_201_CREATED)
    

    return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):

       user = request.user
       try: 
            token = Token.objects.get(user= user)
            token.delete()
            return Response({'detail':"Successfully logged out."}, status=status.HTTP_200_OK)
       except Token.DoesNotExist:
            return Response({"error": "Token not found."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    serializer = UserSerializer(instance=request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)
    # return Response("You are login with {}".format(request.user.username), status=status.HTTP_200_OK)



