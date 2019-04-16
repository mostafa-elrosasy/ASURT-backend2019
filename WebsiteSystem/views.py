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

def TokeyVerify(request):
    try:
        auth = get_authorization_header(request).split()
        token=auth[1]
        secret= SECRET_KEY # the secret key from the settings
        jwt.decode(token , secret)
        return True
    except:
        return False
# 0: to remove image form team
# 1: to remove achievement form team
# 2: to remove image form event
# 3: to remove image form highlight
# 4: to remove image form newsfeed
class RemoveFromView(APIView):
    def get(self, request, type,first_id, second_id):
        x = TokeyVerify(request)
        if x == True :
            if(type == 0):
                Team.objects.get(id = first_id).image.remove(Image.objects.get(id = second_id))
            if(type == 1):
                Team.objects.get(id = first_id).achievement.remove(Achievement.objects.get(id = second_id))
            if(type == 2):
                Event.objects.get(id = first_id).image.remove(Image.objects.get(id = second_id))
            if(type == 3):
                Highlight.objects.get(id = first_id).image.remove(Image.objects.get(id = second_id))
            if(type == 4):
                NewsFeed.objects.get(id = first_id).image.remove(Image.objects.get(id = second_id))
            return Response("deleted", status=status.HTTP_201_CREATED)
        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)



class SponsorGetView (APIView):
    def get(self,request):
        x = TokeyVerify(request)
        if x == True :
            sponsors= Sponsor.objects.all()
            serializer= SponsorSerializer(sponsors, many= True)
            return Response(serializer.data)
        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)

class SponsorPostView (APIView):
    def post(self, request): 
        x = TokeyVerify(request)
        if x == True :
            serializer= SponsorSerializer(data= request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)

class SponsorDelView (APIView): 
    def delete(self, request,pk):
        x = TokeyVerify(request)
        if x == True :
            try:
                sponsors = Sponsor.objects.get(id=pk)
            except sponsors.DoesNotExist:
                raise Http404
            sponsors.delete()
            return Response(status= status.HTTP_204_NO_CONTENT)
        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)

class AllHighlights (APIView):
    #Function to view all highlights using URL : /api/highlight/all/
    def get(self, request):
        x = TokeyVerify(request)
        if x == True :
            try:
                Highlights = Highlight.objects.all()
                serializer = HighlightSerializer(Highlights, many = True)
                return Response(serializer.data)
            except Exception:
                return Response("Error ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)

class Highlights (APIView):
    def get(self, request,id):
        x = TokeyVerify(request)
        if x == True :
            try:
                Highlights = Highlight.objects.filter(id = id)
                serializer = HighlightSerializer(Highlights, many = True)
                return Response(serializer.data)
            except Exception:
                return Response("Error ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)
    #Function to add a new highlight using URL : /api/highlight/
    def post(self, request):
        x = TokeyVerify(request)
        if x == True :
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
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)
    #Function to edit an already existing highlight using URL : /api/highlight/
    def put(self ,request ,id):
        x = TokeyVerify(request)
        if x == True :
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
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)
    #Function to delete a highlight using URL : /api/highlight/
    def delete (self, request, id):
        x = TokeyVerify(request)
        if x == True :
            try:
                Highlight.objects.filter(id = id).delete()
                return Response("Deleted successfully", status=status.HTTP_200_OK)
            except:
                return Response("Error ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)

class ActiveHighlights (APIView):
    #Function to get active Highlights using url : /api/highlight/active/
    def get(self, request):
        x = TokeyVerify(request)
        if x == True :
            try:
                Highlights = Highlight.objects.filter(active = "True")
                serializer = HighlightSerializer(Highlights, many = True)
                return Response(serializer.data)
            except Exception:
                return Response("Error ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)

class AllEvents (APIView):
    #Function to view all events using URL : /api/events/all/
    def get(self, request):
        x = TokeyVerify(request)
        if x == True :
            try:
                Events = Event.objects.all()
                serializer = EventSerializer(Events, many = True)
                return Response(serializer.data)
            except Exception:
                return Response("Error ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)


class Events (APIView):
    #Function to add a new event using URL : /api/events/
    def post(self, request):
        x = TokeyVerify(request)
        if x == True :
            try:
                auth = get_authorization_header(request).split()
                print("############")
                token=auth[1]
                print ("*********************")
                secret= SECRET_KEY # the secret key from the settings
                jwt.decode(token , secret)
            except:
                return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)
            #to be able to send images , we must first check if image is valid , then save that image , and we will then obtain it from the
            #image table
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
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)
    #Function to edit an already existing event using URL : /api/events/
    def put(self ,request ,id):
        x = TokeyVerify(request)
        if x == True :
            try:
                auth = get_authorization_header(request).split()
                print("############")
                token=auth[1]
                print ("*********************")
                secret= SECRET_KEY # the secret key from the settings
                jwt.decode(token , secret)
            except:
                return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)
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
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)

    #Function to delete an event using URL : /api/events/
    def delete(self , request ,id):
        x = TokeyVerify(request)
        if x == True :
            try:
                auth = get_authorization_header(request).split()
                print("############")
                token=auth[1]
                print ("*********************")
                secret= SECRET_KEY # the secret key from the settings
                jwt.decode(token , secret)
            except:
                return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                Event.objects.filter(id = id).delete()
                return Response("Deleted successfully", status=status.HTTP_200_OK)
            except:
                return Response("Error ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)

class ActiveEvents (APIView):
    #Function to get active events using url : /api/events/active/

    def get(self, request):
        x = TokeyVerify(request)
        if x == True :
            try:
                Events = Event.objects.filter(status = "True")
                serializer = EventSerializer(Events, many = True)
                return Response(serializer.data)
            except Exception:
                return Response("Error ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)

class TeamView (APIView):
    def get (self,request):
        x = TokeyVerify(request)
        if x == True :
            teams= Team.objects.all()
            serializer= TeamSerializer(teams, many= True)
            return Response(serializer.data)
        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)

    def post (self, request):
        try:
            auth = get_authorization_header(request).split()
            print("############")
            token=auth[1]
            print ("*********************")
            secret= SECRET_KEY # the secret key from the settings
            jwt.decode(token , secret)
        except:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)
        serializer= TeamSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
        else:
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

        return Response(serializer.data, status= status.HTTP_201_CREATED)
class TeamEditView (APIView):
    def put (self, request, pk):
        x = TokeyVerify(request)
        if x == True :
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
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete (self, request, pk):
        x = TokeyVerify(request)
        if x == True :
            try:
                teams = Team.objects.get(id=pk)
                print(teams.achievement.all())
                for i in teams.achievement.all():
                    Achievement.objects.filter(id=i.id).delete()
            except teams.DoesNotExist:
                raise Http404
            teams.delete()
            return Response(status= status.HTTP_204_NO_CONTENT)

        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)

class NewsFeedView(APIView):
    def get(self, request, page_number):
        x = TokeyVerify(request)
        if x == True :
            data={}
            news = NewsFeed.objects.all()
            pages = Paginator(news, 2)
            page = pages.page(page_number)
            serializer = NewsFeedSerializer(page, many= True)
            data["num_pages"]=pages.num_pages
            data["articles"]= serializer.data
            return Response(data)
        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)

class EditNewsFeedView(APIView):
    def put(self,request, id):
        x = TokeyVerify(request)
        if x == True :
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
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request, id):
        x = TokeyVerify(request)
        if x == True :
            try:
                news = NewsFeed.objects.filter(id = id).delete()
                return Response("Deleted successfully", status=status.HTTP_200_OK)
            except:
                return Response("Error ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)
    
class PostNewsFeedView(APIView):   
    def post(self, request):
        x = TokeyVerify(request)
        if x == True :
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
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)

class FAQView(APIView):
    def get(self,request):
        x = TokeyVerify(request)
        if x == True :
            Faqs=FAQ.objects.all()
            serializer = FAQSerializer(Faqs, many= True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)
    def post(self,request):
        x = TokeyVerify(request)
        if x == True :
            serializer = FAQSerializer(data=request.data)
            if (serializer.is_valid()):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id):
        x = TokeyVerify(request)
        if x == True :
            try:
                if FAQ.objects.filter(id = id) is not None:
                    FAQ.objects.filter(id = id).delete()
                    return Response("Deleted successfully", status=status.HTTP_200_OK)
            except:
                return Response("Error ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)

class AllUsers(APIView):
    def get(self,requset):
        x = TokeyVerify(request)
        if x == True :
            profiles = Profile.objects.all()
            user_list = []
            user_dictionary = {} #key + value

            for i in profiles:
                puser= User.objects.filter(username=i.user).first()
                user_dictionary ["id"] = puser.id
                user_dictionary ["email"] = puser.email
                user_dictionary ["name"] = i.name
                user_dictionary ["phone"] = i.mobile
                user_dictionary ["college_id"] = i.college_id
                user_dictionary ["group"] = puser.groups.all().first().name
                user_list.append(user_dictionary)
            # response["users"]=user_list
            # serializer = UserSerializer(user_list, many = True)
            return Response(user_list)

        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    def get(self,request,id):
        x = TokeyVerify(request)
        if x == True :
            profile = Profile.objects.filter(id = id).first()
            user = User.objects.filter(username = profile.user).first()
            user_dictionary = {}
            user_dictionary["name"] = Profile.name
            user_dictionary["phone"] = Profile.mobile
            user_dictionary["college_id"] = Profile.college_id
            user = User.objects.filter(username = profile.user)
            user_dictionary["email"] = User.email
            user_dictionary["group"] = user.groups.all().first().name
            return Response(user_dictionary)

        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)
    def put(self,request,id):
        x = TokeyVerify(request)
        if x == True :
            user = User.objects.get(pk = id)
            updated_group = Group.objects.get(name = request.data['group'])
            user_groups = User.groups.through.objects.get(user=user)
            user_groups.group = updated_group
            user_groups.save()
            return self.update(request)

        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)
    
class GroupsView(APIView):
    def get(self,request):
        x = TokeyVerify(request)
        if x == True :
            groups = Group.objects.all()
            serializer = GroupSerializer(groups, many= True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response({"Token Validation": "False"}, status=status.HTTP_400_BAD_REQUEST)
        
