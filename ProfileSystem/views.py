from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Profile, User, Error
from .serializers import ProfileSerializer
import base64
from django.core.files.base import ContentFile
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import get_authorization_header
import jwt
from RT_Website_19.settings import SECRET_KEY
from pinax.eventlog.models import log
import datetime

def log_errors(ex,id):
    now = datetime.datetime.now()
    user= User.objects.filter(id=id).first()
    error = Error(user= user,error=ex, time = now)
    error.save()


# The function is used to get the ID of the user who sent the token
# by decoding the Jwt. Parameter: the request, Returns: user ID
def get_user_ID(request):
    try:
        auth = get_authorization_header(request).split()
        token=auth[1]
        secret= SECRET_KEY # the secret key from the settings
        payload= jwt.decode(token,secret)
        return payload['user_id']
    except Exception as ex:
        log_errors(str(ex),1)
        return Response("An error has happened!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class View_Profile(APIView):

# This function returns a JSON that contains the profile data of the user
# that sent the request, it accepts GET requests
    def get(self, request):
        try:
            id =get_user_ID(request)
            # checks if the user doesn't have an account
            if( not (Profile.objects.filter(user=id).exists())):
                return Response("This user doesn't have a profile yet", status=status.HTTP_400_BAD_REQUEST)
            profiles= Profile.objects.filter(user=id)
            serializer= ProfileSerializer(profiles,many=True)
            # Stores "View Profile" activity in the database
            log(user=User.objects.filter(id=id).first(), action="Viewed Profile",)
            return Response(serializer.data)
        except TypeError as ex:
            log_errors(str(ex),1)
            return Response("The jwt token isn't correct", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as ex:
            log_errors(str(ex),id)
            return Response("An error has happened!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# This function is used to create new profiles for registered users, it accepts POST requests
    def post(self, request):
        try:
            json_data=request.data
            if(request.data["national_front"] =="" or request.data["national_back"] == ""):
                return Response("The national ID images can't be  blank", status=status.HTTP_400_BAD_REQUEST)
            # gets the ID of the user that sent the request
            id =get_user_ID(request)
            if(not(User.objects.filter(id=id).exists)):
                log_errors(str(ex),1)
                return Response("An error has happened!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            # checks if this user already has a profile
            if(Profile.objects.filter(user=id).exists()):
                return Response("This user already has a profile", status=status.HTTP_400_BAD_REQUEST)
            json_data['user']=id
            serializer = ProfileSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                # Stores "Create Profile" activity in the database
                log(user=User.objects.filter(id=id).first(), action="Created Profile",)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            log(user=User.objects.filter(id=id).first(),action="Tried to Create Profile",)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except TypeError as ex:
            log_errors(str(ex),1)
            return Response("The jwt token isn't correct", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as ex:
            log_errors(str(ex),id)
            return Response("An error has happened!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# This class is used to edit the user's profile data. When accessed whith GET request it
# returns the profile data of the user who made the request. When accessed with POST request
# it gets the new data from the user to edit his profile
    def put(self, request):
        try:
            json_data=request.data
            if(request.data["national_front"]=="" or request.data["national_back"] == ""):
                return Response("The national ID images can't be  blank", status=status.HTTP_400_BAD_REQUEST)
            # gets the ID of the user that sent the request
            id =get_user_ID(request)
            if(not(User.objects.filter(id=id).exists)):
                log_errors(str(ex),1)
                return Response("An error has happened!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            # checks if the user doesn't have an account
            if( not (Profile.objects.filter(user=id).exists())):
                return Response("This user doesn't have a profile yet", status=status.HTTP_400_BAD_REQUEST)
            profiles=Profile.objects.filter(user=id).first()
            serializer = ProfileSerializer(profiles,data=request.data)
            if serializer.is_valid():
                serializer.save()
                # Stores "Edit Profile" activity in the database
                log(user=User.objects.filter(id=id).first(), action="Edited Profile",)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            log(user=User.objects.filter(id=id).first(),action="Tried to edit Profile",)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except TypeError as ex:
            log_errors(str(ex),1)
            return Response("The jwt token isn't correct", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as ex:
            log_errors(str(ex),id)
            return Response("An error has happened!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
