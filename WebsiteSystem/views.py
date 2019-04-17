from django.shortcuts import render
from .models import Sponsor, Image, Team , Event, NewsFeed, FAQ , Highlight, Achievement
from .serializers import SponsorSerializer, EventSerializer, NewsFeedSerializer, ImageSerializer, FAQSerializer ,HighlightSerializer, TeamSerializer, GroupSerializer, AchievementSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.core.paginator import Paginator
from django.contrib.auth.models import Group, User
from ProfileSystem.models import Profile
import jwt
from RT_Website_19.settings import SECRET_KEY
from rest_framework.authentication import get_authorization_header
from AuthenticationSystem.models import Error
from ProfileSystem.views import get_user_ID, log_errors
from pinax.eventlog.models import log

def TokenVerify(request):
    try:
        auth = get_authorization_header(request).split()
        token=auth[1]
        secret= SECRET_KEY # the secret key from the settings
        jwt.decode(token , secret)
        return True
    except:
        return False

def BackEndPermissionVerifier(request):
    auth = get_authorization_header(request).split()
    token=auth[1]
    secret= SECRET_KEY # the secret key from the settings
    payload = jwt.decode(token , secret)
    if payload['position'] == 'IT -SeniorOfficer' :
        return True
    else :
        return False

        
        

# 0: to remove image form team
# 1: to remove achievement form team
# 2: to remove image form event
# 3: to remove image form highlight
# 4: to remove image form newsfeed
class RemoveFromView(APIView):
    def get(self, request, type,first_id, second_id):
        
        if TokenVerify(request) and BackEndPermissionVerifier(request) :
            if(type == 0):
                Team.objects.get(id = first_id).image.remove(Image.objects.get(id = second_id))
                Image.objects.get(id = second_id).delete()
            if(type == 1):
                Team.objects.get(id = first_id).achievement.remove(Achievement.objects.get(id = second_id))
                Image.objects.get(id = second_id).delete()
            if(type == 2):
                Event.objects.get(id = first_id).image.remove(Image.objects.get(id = second_id))
                Image.objects.get(id = second_id).delete()
            if(type == 3):
                Highlight.objects.get(id = first_id).image.remove(Image.objects.get(id = second_id))
                Image.objects.get(id = second_id).delete()
            if(type == 4):
                NewsFeed.objects.get(id = first_id).image.remove(Image.objects.get(id = second_id))
                Image.objects.get(id = second_id).delete()
            return Response("deleted", status=status.HTTP_201_CREATED)
        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)

class SponsorGetView (APIView):
    def get(self,request):
        try:
            id =get_user_ID(request)
            sponsors= Sponsor.objects.all()
            serializer= SponsorSerializer(sponsors, many= True)
            log(user=User.objects.filter(id=id).first(), action="Viewed all sponsors",)
            return Response(serializer.data)
        except Exception as ex:
            log_errors(str(ex),id)
            return Response("An error has happened!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class SponsorPostView (APIView):
    def post(self, request): 
        if TokenVerify(request) and BackEndPermissionVerifier(request) :
            try:
                id =get_user_ID(request)
                serializer= SponsorSerializer(data= request.data)
                if serializer.is_valid():
                    serializer.save()
                    log(user=User.objects.filter(id=id).first(), action="Added a sponsor",)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    log(user=User.objects.filter(id=id).first(),action="Tried to add a sponsor",)
                    return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as ex:
                log_errors(str(ex),id)
                return Response("An error has happened!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)

class SponsorDelView (APIView): 
    def delete(self, request,pk):
        if TokenVerify(request) and BackEndPermissionVerifier(request) :
            try:
                I =get_user_ID(request)
                if Sponsor.objects.get(id=pk) is not None:
                    Sponsor.objects.get(id=pk).delete()
                    log(user=User.objects.filter(id=I).first(), action="Deleted a sponsor",)
                    return Response("Deleted successfully!", status=status.HTTP_200_OK)
            except Exception as ex:
                log_errors(str(ex),I)
                return Response("An error has happened!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)

class AllHighlights (APIView):
    #Function to view all highlights using URL : /api/highlight/all/
    def get(self, request):
        try:
            id =get_user_ID(request)
            Highlights = Highlight.objects.all()
            serializer = HighlightSerializer(Highlights, many = True)
            log(user=User.objects.filter(id=id).first(), action="Viewed all highlights",)
            return Response(serializer.data)
        except Exception as ex:
            log_errors(str(ex),id)
            return Response("Error ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Highlights (APIView):
    def get(self, request,id):
        try:
            I =get_user_ID(request)
            Highlights = Highlight.objects.filter(id = id)
            serializer = HighlightSerializer(Highlights, many = True)
            log(user=User.objects.filter(id=I).first(), action="Viewed a highlight",)
            return Response(serializer.data)
        except Exception as ex:
            log_errors(str(ex),I)
            return Response("Error ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    #Function to add a new highlight using URL : /api/highlight/
    def post(self, request):
        if TokenVerify(request) and BackEndPermissionVerifier(request) :
            try:
                id =get_user_ID(request)
                image = {}
                image["image"]=request.data["image"]
                image = ImageSerializer(data = image)
                if image.is_valid():
                    image.save()
                else:
                    return Response("image error")
                serializer = HighlightSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.validated_data["image"]= [Image.objects.last().id]
                    serializer.save()
                    log(user=User.objects.filter(id=id).first(),action="Added a highlight",)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    log(user=User.objects.filter(id=id).first(),action="Tried to add a highlight",)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as ex:
                log_errors(str(ex),id)
                return Response("Error ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)
    #Function to edit an already existing highlight using URL : /api/highlight/
    def put(self ,request ,id):
        if TokenVerify(request) and BackEndPermissionVerifier(request) :
            try:
                I =get_user_ID(request)
                image = {}
                highlights = Highlight.objects.filter(id = id).first()
                image["image"]=request.data["image"]
                if(image["image"] != ""):
                    image=ImageSerializer(data= image)
                    if image.is_valid():
                        image.save()
                        highlights.image.add(Image.objects.last().id)
                    else:
                        return Response(image.errors)
                else:
                    request.data.pop('image',None)

                serializer= HighlightSerializer(highlights, data= request.data)
                if serializer.is_valid():
                    serializer.save()
                    log(user=User.objects.filter(id=I).first(), action="Updated a highlight",)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    log(user=User.objects.filter(id=I).first(), action="Tried to update a highlight",)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as ex:
                log_errors(str(ex),I)
                return Response("Error ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)
    #Function to delete a highlight using URL : /api/highlight/
    def delete (self, request, id):
        if TokenVerify(request) and BackEndPermissionVerifier(request) :
            try:
                I =get_user_ID(request) #get id
                Highlight.objects.filter(id = id).delete()
                log(user=User.objects.filter(id=I).first(), action="Deleted a highlight",)
                return Response("Deleted successfully", status=status.HTTP_200_OK)
            except Exception as ex:
                log_errors(str(ex),I)
                return Response("Error ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)

class ActiveHighlights (APIView):
    #Function to get active Highlights using url : /api/highlight/active/
    def get(self, request):
        try:
            id =get_user_ID(request)
            Highlights = Highlight.objects.filter(active = "True")
            serializer = HighlightSerializer(Highlights, many = True)
            log(user=User.objects.filter(id=id).first(), action="Viewed active highlight",)
            return Response(serializer.data)
        except Exception as ex:
            log_errors(str(ex),id)
            return Response("Error ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AllEvents (APIView):
    #Function to view all events using URL : /api/events/all/
    def get(self, request):
        try:
            id =get_user_ID(request)
            Events = Event.objects.all()
            serializer = EventSerializer(Events, many = True)
            log(user=User.objects.filter(id=id).first(), action="Viewed all events",)
            return Response(serializer.data)
        except Exception as ex:
            log_errors(str(ex),id)
            return Response("Error ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Events (APIView):
    def get(self, request, id):
        event = Event.objects.get(id= id)
        serializer = EventSerializer(event)
        return Response(serializer.data, status = status.HTTP_200_OK)
    #Function to add a new event using URL : /api/events/
    def post(self, request):
        if TokenVerify(request) and BackEndPermissionVerifier(request) :
            #to be able to send images , we must first check if image is valid , then save that image , and we will then obtain it from the
            #image table
            try:
                id =get_user_ID(request)
                image = {}
                image["image"]=request.data["image"]
                image = ImageSerializer(data = image)
                if image.is_valid():
                    image.save()
                else:
                    return Response("image error")
                serializer = EventSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.validated_data["image"]= [Image.objects.last().id]
                    serializer.save()
                    log(user=User.objects.filter(id=id).first(),action="Added an event",)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    log(user=User.objects.filter(id=id).first(),action="Tried to add an event",)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as ex:
                log_errors(str(ex),id)
                return Response("An error has happened! ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)
    #Function to edit an already existing event using URL : /api/events/
    def put(self ,request ,id):
        if TokenVerify(request) and BackEndPermissionVerifier(request) :
            try:
                I =get_user_ID(request)
                image = {}
                Events = Event.objects.filter(id = id).first()
                image["image"]=request.data["image"]
                if(image["image"] != ""):
                    image=ImageSerializer(data= image)
                    if image.is_valid():
                        image.save()
                        Events.image.add(Image.objects.last().id)
                    else:
                        return Response(image.errors)
                else:
                    request.data.pop('image',None)

                serializer= EventSerializer(Events, data= request.data)
                if serializer.is_valid():
                    serializer.save()
                    log(user=User.objects.filter(id=I).first(), action="Updated an event",)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    log(user=User.objects.filter(id=I).first(), action="Tried to update an event",)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as ex:
                log_errors(str(ex),I)
                return Response("An error has happened! ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)

    #Function to delete an event using URL : /api/events/
    def delete(self , request ,id):
        if TokenVerify(request) and BackEndPermissionVerifier(request) :
            try:
                I =get_user_ID(request)
                Event.objects.filter(id = id).delete()
                log(user=User.objects.filter(id=I).first(), action="Deleted an event",)
                return Response("Deleted successfully", status=status.HTTP_200_OK)
            except Exception as ex:
                log_errors(str(ex),I)
                return Response("An error has happened! ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)

class ActiveEvents (APIView):
    #Function to get active events using url : /api/events/active/

    def get(self, request):
        try:
            id =get_user_ID(request)
            Events = Event.objects.filter(status = "True")
            serializer = EventSerializer(Events, many = True)
            log(user=User.objects.filter(id=id).first(), action="Viewed active events",)
            return Response(serializer.data)
        except Exception as ex:
            log_errors(str(ex),id)
            return Response("Error ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TeamView (APIView):
    def get (self,request):
        try:
            id =get_user_ID(request)
            teams= Team.objects.all()
            serializer= TeamSerializer(teams, many= True)
            log(user=User.objects.filter(id=id).first(), action="Viewed the teams",)
            return Response(serializer.data)
        except Exception as ex:
            log_errors(str(ex),id)
            return Response("An error has happened! ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post (self, request):
        if TokenVerify(request) and BackEndPermissionVerifier(request) :
            try:
                id =get_user_ID(request)
                serializer= TeamSerializer(data= request.data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    log(user=User.objects.filter(id=id).first(),action="Tried to add a team",)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                teams = Team.objects.last()
                #achievement = {}  #name of the obj (JSON)-----DICTIONARY
                achievement=request.data["achievement"]  #field inside the dic , put data inside it key=value
                for single_achievement in achievement :
                    single_achievement = AchievementSerializer(data = single_achievement)
                    if single_achievement.is_valid():
                        single_achievement.save()
                        teams.achievement.add(Achievement.objects.last())
                    else:
                        return Response("achievement error ")
                image = request.data["image"]
                for single_image in image:
                    single_image = ImageSerializer(data = single_image)
                    if single_image.is_valid():
                        single_image.save()
                        teams.image.add(Image.objects.last())
                    else:
                        return Response("image error")
                log(user=User.objects.filter(id=id).first(),action="Added a team",)
                return Response(serializer.data, status= status.HTTP_201_CREATED)
            except Exception as ex:
                    log_errors(str(ex),id)
                    return Response("An error has happened! ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else :
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)

class TeamEditView (APIView):
    def put (self, request, pk):
        if TokenVerify(request) and BackEndPermissionVerifier(request) :
            try:
                I =get_user_ID(request)
                teams = Team.objects.filter(id = pk).first()
                achievement= request.data["achievement"]
                if(achievement != ""):
                    achievement=AchievementSerializer(data= achievement)
                    if achievement.is_valid():
                        achievement.save()
                        teams.achievement.add(Achievement.objects.last().id)
                    else:
                        return Response("achievement error")
                else:
                    request.data.pop('achievement',None)

                image = {}
                image["image"]=request.data["image"]
                if(image["image"] != ""):
                    image=ImageSerializer(data= image)
                    if image.is_valid():
                        image.save()
                        teams.image.add(Image.objects.last().id)
                    else:
                        return Response(image.errors)
                else:
                    request.data.pop('image',None)

                serializer= TeamSerializer(teams, data= request.data)
                if serializer.is_valid():
                    serializer.save()
                    log(user=User.objects.filter(id=I).first(), action="Updated a team",)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    log(user=User.objects.filter(id=I).first(), action="Tried to update a team",)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as ex:
                log_errors(str(ex),I)
                return Response("An error has happened! ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)
    

    def get (self,request,pk):
        try:
            I =get_user_ID(request)
            teams = Team.objects.filter(id = pk).first()
            serializer= TeamSerializer(teams)
            log(user=User.objects.filter(id=I).first(), action="Viewed the teams",)
            return Response(serializer.data)
        except Exception as ex:
            log_errors(str(ex),I)
            return Response("An error has happened! ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete (self, request, pk):
        if TokenVerify(request) and BackEndPermissionVerifier(request) :
            try:
                I =get_user_ID(request)
                teams = Team.objects.get(id=pk)
                print(teams.achievement.all())
                for i in teams.achievement.all():
                    Achievement.objects.filter(id=i.id).delete()
                if teams is not None:
                    teams.delete()
                    log(user=User.objects.filter(id=I).first(), action="Deleted a team",)
                    return Response("Deleted successfully!", status=status.HTTP_200_OK)
            except Exception as ex:
                log_errors(str(ex),I)
                return Response("An error has happened! ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)

class NewsFeedView(APIView):
    def get(self, request, page_number):
        try:
            id =get_user_ID(request)
            data={}
            news = NewsFeed.objects.all().order_by('-date')
            news.reverse()
            pages = Paginator(news, 5)
            page = pages.page(page_number)
            serializer = NewsFeedSerializer(page, many= True)
            data["num_pages"]=pages.num_pages
            data["articles"]= serializer.data
            log(user=User.objects.filter(id=id).first(), action="Viewed the newsfeed",)
            return Response(data)
        except Exception as ex:
            log_errors(str(ex),id)
            return Response("An error has happened! ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EditNewsFeedView(APIView):
    def get(sef, request, id):
        news = NewsFeed.objects.get(id= id)
        serializer = NewsFeedSerializer(news)
        return Response(serializer, status = status.HTTP_200_OK)
    def put(self,request, id):
        if TokenVerify(request) and BackEndPermissionVerifier(request) :
            try:
                I =get_user_ID(request)
                image = {}
                news = NewsFeed.objects.filter(id = id).first()
                image["image"]=request.data["image"]
                if(image["image"] != ""):
                    image=ImageSerializer(data= image)
                    if image.is_valid():
                        image.save()
                        news.image.add(Image.objects.last().id)
                    else:
                        return Response(image.errors)
                else:
                    request.data.pop('image',None)

                serializer= NewsFeedSerializer(news, data= request.data)
                if serializer.is_valid():
                    serializer.save()
                    log(user=User.objects.filter(id=I).first(), action="Updated a newsfeed",)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    log(user=User.objects.filter(id=I).first(), action="Tried to update newfeed",)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as ex:
                log_errors(str(ex),I)
                return Response("An error has happened! ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request, id):
        x = TokenVerify(request)
        if x == True :
            try:
                I =get_user_ID(request)
                news = NewsFeed.objects.filter(id = id).delete()
                log(user=User.objects.filter(id=I).first(), action="Deleted a newsfeed",)
                return Response("Deleted successfully", status=status.HTTP_200_OK)
            except Exception as ex:
                log_errors(str(ex),I)
                return Response("An error has happened! ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)
    
class PostNewsFeedView(APIView):   
    def post(self, request):
        if TokenVerify(request) and BackEndPermissionVerifier(request) :
            try:
                id =get_user_ID(request)
                image = {}
                image["image"]=request.data["image"]
                image = ImageSerializer(data = image)
                if image.is_valid():
                    image.save()
                else:
                    return Response("image error")
                serializer= NewsFeedSerializer(data= request.data)
                if serializer.is_valid():
                    serializer.validated_data["image"]= [Image.objects.last().id]
                    serializer.save()
                    log(user=User.objects.filter(id=id).first(),action="Added a newsfeed",)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    log(user=User.objects.filter(id=id).first(),action="Tried to add a newsfeed",)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as ex:
                log_errors(str(ex),id)
                return Response("An error has happened! ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)

class FAQView(APIView):
    def get(self,request):
        try:
            id =get_user_ID(request)
            Faqs=FAQ.objects.all()
            serializer = FAQSerializer(Faqs, many= True)
            log(user=User.objects.filter(id=id).first(), action="Viewed the FAQ",)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            log_errors(str(ex),id)
            return Response("An error has happened! ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self,request):
        if TokenVerify(request) :
            try:
                id =get_user_ID(request)
                serializer = FAQSerializer(data=request.data)
                if (serializer.is_valid()):
                    serializer.save()
                    log(user=User.objects.filter(id=id).first(),action="Added FAQ",)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    log(user=User.objects.filter(id=id).first(),action="Tried to add FAQ",)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as ex:
                log_errors(str(ex),id)
                return Response("An error has happened! ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else :
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)
    
class DeleteFaqView(APIView):
    def delete(self,request,id):
        if TokenVerify(request) :
            try:
                I =get_user_ID(request)
                if FAQ.objects.filter(id = id) is not None:
                    FAQ.objects.filter(id = id).delete()
                    log(user=User.objects.filter(id=I).first(), action="Deleted a FAQ",)
                    return Response("Deleted successfully", status=status.HTTP_200_OK)
            except Exception as ex:
                log_errors(str(ex),I)
                return Response("An error has happened! ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)

class AllUsers(APIView):
    def get(self,request):
        if TokenVerify(request) and BackEndPermissionVerifier(request) :
            try:
                I =get_user_ID(request)
                profiles = Profile.objects.all()
                user_list = []
                user_dictionary = {} #key + value
                for i in profiles:
                    user_dictionary ["id"] = i.user.id
                    user_dictionary ["email"] = i.user.email
                    user_dictionary ["name"] = i.name
                    user_dictionary ["phone"] = i.mobile
                    user_dictionary ["college_id"] = i.college_id
                    user_dictionary ["group"] = i.user.groups.all().first().name
                    user_list.append(user_dictionary)
                log(user=User.objects.filter(id=I).first(), action="Viewed all users",)
                return Response(user_list)
            except Exception as ex:
                log_errors(str(ex),I)
                return Response("An error has happened! ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)

class UserView(APIView):
    def get(self,request,id):
        if TokenVerify(request) and BackEndPermissionVerifier(request) :
            try:
                I =get_user_ID(request)
                # TargetUser = User.objects.filter(id = id).first()
                profile = Profile.objects.filter(user = id).first()
                user_dictionary = {}
                user_dictionary["name"] = profile.name
                user_dictionary["phone"] = profile.mobile
                user_dictionary["college_id"] = profile.college_id
                user_dictionary["email"] = profile.user.email
                user_dictionary["group"] = profile.user.groups.all().first().name
                log(user=User.objects.filter(id=I).first(), action="Viewed one user",)
                return Response(user_dictionary)
            except Exception as ex:
                log_errors(str(ex),I)
                return Response("An error has happened! ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,id):
        if TokenVerify(request) and BackEndPermissionVerifier(request) :
            try:
                I = get_user_ID(request)
                user = User.objects.get(pk = id)
                updated_group = Group.objects.get(name = request.data['group'])
                updated_group.user_set.add(user)
                # user_groups.save()
                log(user=User.objects.filter(id=I).first(), action="Updated a user",)
                return Response("User Group Permissions SUccessfully Updated" , status=status.HTTP_202_ACCEPTED)
            except Exception as ex:
                log_errors(str(ex),I)
                return Response("An error has happened! ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)
    
class GroupsView(APIView):
    def get(self,request):
        if TokenVerify(request):
            try:
                id =get_user_ID(request)
                groups = Group.objects.all()
                serializer = GroupSerializer(groups, many= True)
                log(user=User.objects.filter(id=id).first(), action="Viewed the groups",)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as ex:
                log_errors(str(ex),id)
                return Response("An error has happened! ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)