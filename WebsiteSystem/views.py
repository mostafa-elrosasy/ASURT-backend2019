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

# 0: to remove image form team
# 1: to remove achievement form team
class RemoveFromView(APIView):
    def get(self, request, type,first_id, second_id):
        if(type == 0):
            Team.objects.get(id = first_id).image.remove(Image.objects.get(id = second_id))
        if(type == 1):
            Team.objects.get(id = first_id).achievement.remove(Achievement.objects.get(id = second_id))
        return Response("deleted", status=status.HTTP_201_CREATED)
class SponsorGetView (APIView):
    def get(self,request):
            sponsors= Sponsor.objects.all()
            serializer= SponsorSerializer(sponsors, many= True)
            return Response(serializer.data)

class SponsorPostView (APIView):
    def post(self, request): 
        serializer= SponsorSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SponsorDelView (APIView): 
    def delete(self, request,pk):
        try:
            sponsors = Sponsor.objects.get(id=pk)
        except sponsors.DoesNotExist:
            raise Http404
        sponsors.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)

class AllHighlights (APIView):
    #Function to view all highlights using URL : /api/highlight/all/
    def get(self, request):
        try:
            Highlights = Highlight.objects.all()
            serializer = HighlightSerializer(Highlights, many = True)
            return Response(serializer.data)
        except Exception:
            return Response("Error ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Highlights (APIView):
    #Function to add a new highlight using URL : /api/highlight/
    def post(self, request):
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
    #Function to edit an already existing highlight using URL : /api/highlight/
    def put(self,request):
        image = {}
        id = request.GET.get('id', '')
        Highlights = Highlight.objects.filter(id = id).first()
        image["image"]=request.data["image"]
        if(image["image"]!=""):
            image = ImageSerializer(data = image)
            if image.is_valid():
                image.save()
                request.data["image"]= [Image.objects.last().id]
                print(request.data["image"])
            else:
                return Response("image error")
        else:
            request.data["image"]= [Highlights.image.first().id]
        serializer= HighlightSerializer(Highlights, data= request.data)
        if serializer.is_valid():
            serializer.validated_data["image"]= request.data["image"]
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #Function to delete a highlight using URL : /api/highlight/
    def delete (self, request):
        try:
            id = request.GET.get('id', '')
            Highlight.objects.filter(id = id).delete()
            return Response("Deleted successfully", status=status.HTTP_200_OK)
        except:
            return Response("Error ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ActiveHighlights (APIView):
    #Function to get active Highlights using url : /api/highlight/active/
    def get(self, request):
        try:
            Highlights = Highlight.objects.filter(active = "True")
            serializer = HighlightSerializer(Highlights, many = True)
            return Response(serializer.data)
        except Exception:
            return Response("Error ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AllEvents (APIView):
    #Function to view all events using URL : /api/events/all/
    def get(self, request):
        try:
            Events = Event.objects.all()
            serializer = EventSerializer(Events, many = True)
            return Response(serializer.data)
        except Exception:
            return Response("Error ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Events (APIView):
    #Function to add a new event using URL : /api/events/
    def post(self, request):
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
    #Function to edit an already existing event using URL : /api/events/
    def put(self,request):
        image = {}
        id = request.GET.get('id', '')
        Events = Event.objects.filter(id = id).first()
        image["image"]=request.data["image"]
        print("*****************************************")
        if(image["image"] != ""):
            image=ImageSerializer(data= image)
            if image.is_valid():
                image.save()
                teams.image.add(Image.objects.last().id)
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

    #Function to delete an event using URL : /api/events/
    def delete(self, request):
        try:
            id = request.GET.get('id', '')
            Event.objects.filter(id = id).delete()
            return Response("Deleted successfully", status=status.HTTP_200_OK)
        except:
            return Response("Error ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ActiveEvents (APIView):
    #Function to get active events using url : /api/events/active/

    def get(self, request):
        try:
            Events = Event.objects.filter(status = "True")
            serializer = EventSerializer(Events, many = True)
            return Response(serializer.data)
        except Exception:
            return Response("Error ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TeamView (APIView):
    def get (self,request):
        teams= Team.objects.all()
        serializer= TeamSerializer(teams, many= True)
        return Response(serializer.data)

    def post (self, request):
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
    
    def delete (self, request, pk):
        try:
            teams = Team.objects.get(id=pk)
            print(teams.achievement.all())
            for i in teams.achievement.all():
                Achievement.objects.filter(id=i.id).delete()
        except teams.DoesNotExist:
            raise Http404
        teams.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)

class NewsFeedView(APIView):
    def get(self, request, page_number):
        data={}
        news = NewsFeed.objects.all()
        pages = Paginator(news, 2)
        page = pages.page(page_number)
        serializer = NewsFeedSerializer(page, many= True)
        data["num_pages"]=pages.num_pages
        data["articles"]= serializer.data
        return Response(data)

class EditNewsFeedView(APIView):
    def put(self,request, id):
        image = {}
        news = NewsFeed.objects.filter(id = id).first()
        image["image"]=request.data["image"]
        if(image["image"]!=""):
            image = ImageSerializer(data = image)
            if image.is_valid():
                image.save()
                request.data["image"]= [Image.objects.last().id]
                print(request.data["image"])
            else:
                return Response("image error")
        else:
            request.data["image"]= [news.image.first().id]
        serializer= NewsFeedSerializer(news, data= request.data)
        if serializer.is_valid():
            serializer.validated_data["image"]= request.data["image"]
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request, id):
        try:
            news = NewsFeed.objects.filter(id = id).delete()
            return Response("Deleted successfully", status=status.HTTP_200_OK)
        except:
            return Response("Error ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class PostNewsFeedView(APIView):   
    def post(self, request):
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

class FAQView(APIView):
    def get(self,request):
        Faqs=FAQ.objects.all()
        serializer = FAQSerializer(Faqs, many= True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def post(self,request):
        serializer = FAQSerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request):
        try:
            id = request.GET.get('id', '')
            if FAQ.objects.filter(id = id) is not None:
                FAQ.objects.filter(id = id).delete()
                return Response("Deleted successfully", status=status.HTTP_200_OK)
        except:
            return Response("Error ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AllUsers(APIView):
    def get(self,requset):

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

class UserView(APIView):
    def get(self,request,id):
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
    def put(self,request,id):
        user = User.objects.get(pk = id)
        updated_group = Group.objects.get(name = request.data['group'])
        user_groups = User.groups.through.objects.get(user=user)
        user_groups.group = updated_group
        user_groups.save()
        return self.update(request)
    
class GroupsView(APIView):
    def get(self,request):
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many= True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
